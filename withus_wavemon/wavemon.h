/*
 * wavemon - a wireless network monitoring aplication
 *
 * Copyright (c) 2001-2002 Jan Morgenstern <jan@jm-music.de>
 * Copyright (c) 2009      Gerrit Renker <gerrit@erg.abdn.ac.uk>
 *
 * wavemon is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2, or (at your option) any later
 * version.
 *
 * wavemon is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along
 * with wavemon; see the file COPYING.  If not, write to the Free Software
 * Foundation, 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <assert.h>
#include <errno.h>
#include <err.h>
#include <time.h>
#include <sys/time.h>
#include <sys/ioctl.h>

#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdbool.h>

#include "llist.h"

#define CFNAME	".wavemonrc"
typedef struct {
	char	mac[17];
	char essid[34];
	int freq;
	int	chan;
	int	has_key:1;
	int	last_seen;
	int tsf;
	int	bss_signal;
	int	bss_signal_qual;
	int	bss_sta_count;
	int bss_chan_usage;
} AP;

typedef struct {
	int entryNum;
	int twoGig;
	int fiveGig;
  AP APlist[10];
} wirelessSearch;

wirelessSearch* umalloc(void);
void ufree(wirelessSearch* w);
void ap_scan(wirelessSearch* _ws);
void terminate();

/* Minimum SSID length */
#define MAX_ESSID_LEN		16

/*
 * Symbolic names of actions to take when crossing thresholds.
 * These actions invoke the corresponding ncurses functions.
 */

enum threshold_action {
	TA_DISABLED,
	TA_BEEP,
	TA_FLASH,
	TA_BEEP_FLASH
};
/*
 * Symbolic names for scan sort order comparison.
 */
enum scan_sort_order {
	SO_CHAN,
	SO_SIGNAL,
	SO_MAC,
	SO_ESSID,
	SO_OPEN,
	SO_CHAN_SIG,
	SO_OPEN_SIG
};

/*
 * Global in-memory representation of current wavemon configuration state
 */
extern struct wavemon_conf {
	int	if_idx;			/* Index into interface list */

	int	stat_iv,
		info_iv;

	int	sig_min, sig_max,
		noise_min, noise_max;

	int	lthreshold,
		hthreshold;

	int	slotsize,
		meter_decay;

	/* Boolean values */
	int	cisco_mac,		/* Cisco-style MAC addresses */
		override_bounds,	/* override autodetection */
		scan_sort_asc;		/* direction of @scan_sort_order */

	/* Enumerated values */
	int	scan_sort_order,	/* channel|signal|open|chan/sig ... */
		lthreshold_action,	/* disabled|beep|flash|beep+flash */
		hthreshold_action;	/* disabled|beep|flash|beep+flash */
} conf;

/*
 * Initialisation & Configuration
 */
extern void getconf();

/* Configuration items to manipulate the current configuration */
struct conf_item {
	char	*name,		/* name for preferences screen */
		*cfname;	/* name for ~/.wavemonrc */

	enum {			/* type of parameter */
		t_int,		/* @v.i is interpreted as raw value */
		t_list,		/* @v.i is an index into @list */
		t_sep,		/* dummy, separator entry */
		t_func		/* void (*fp) (void) */
	} type;

	union {			/* type-dependent container for value */
		int	*i;	/* t_int and t_list index into @list  */
		void (*fp)();	/* t_func */
	} v;

	char	**list;		/* t_list: NULL-terminated array of strings */
	int	*dep;		/* dependency */

	double	min,		/* value boundaries */
		max,
		inc;		/* increment for value changes */

	char	*unit;		/* name of units to display */
};

extern void scr_aplst_init(wirelessSearch* ws);
extern void scr_aplst_fini(void);

/*
 *	Wireless interfaces
 */
extern const char *conf_ifname(void);
extern void conf_get_interface_list(void);
extern void iw_get_interface_list(char** if_list, size_t max_entries);

/*
 *	Error handling
 */
extern bool has_net_admin_capability(void);
extern void err_msg(const char *format, ...);
extern void err_quit(const char *format, ...);
extern void err_sys(const char *format, ...);

/*
 *	Helper functions
 */
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

static inline void (*xsignal(int signo, void (*handler)(int)))(int)
{
	struct sigaction old_sa, sa = { .sa_handler = handler, .sa_flags = 0 };

	if (sigemptyset(&sa.sa_mask) < 0 || sigaction(signo, &sa, &old_sa) < 0)
		err_sys("xsignal(%d) failed", signo);
	return old_sa.sa_handler;
}

static inline size_t argv_count(char **argv)
{
	int cnt = 0;

	assert(argv != NULL);
	while (*argv++)
		cnt++;
	return cnt;
}

static inline int argv_find(char **argv, const char *what)
{
	int cnt = argv_count(argv), len, i;

	assert(what != NULL);
	for (i = 0, len = strlen(what); i < cnt; i++)
		if (strncasecmp(argv[i], what, len) == 0)
			return i;
	return -1;
}

static inline void str_tolower(char *s)
{
	for (; s && *s; s++)
		*s = tolower(*s);
}

/* Check if @str is printable (compare iw_essid_escape()) */
static inline bool str_is_ascii(char *s)
{
	if (!s || !*s)
		return false;
	for (; *s; s++)
		if (!isascii(*s) || iscntrl(*s))
			return false;
	return true;
}

/* number of digits needed to display integer part of @val */
static inline int num_int_digits(const double val)
{
	return 1 + (val > 1.0 ? log10(val) : val < -1.0 ? log10(-val) : 0);
}

static inline int max(const int a, const int b)
{
	return a > b ? a : b;
}

static inline bool in_range(int val, int min, int max)
{
	return min <= val && val <= max;
}

static inline int clamp(int val, int min, int max)
{
	return val < min ? min : (val > max ? max : val);
}

/* SI units -- see units(7) */
static inline char *byte_units(const double bytes)
{
	static char result[0x100];

	if (bytes >= 1 << 30)
		sprintf(result, "%0.2lf GiB", bytes / (1 << 30));
	else if (bytes >= 1 << 20)
		sprintf(result, "%0.2lf MiB", bytes / (1 << 20));
	else if (bytes >= 1 << 10)
		sprintf(result, "%0.2lf KiB", bytes / (1 << 10));
	else
		sprintf(result, "%.0lf B", bytes);

	return result;
}

/* Integer units - similar to %g for float. */
static inline char *int_counts(uint32_t count)
{
	static char result[0x100];

	if (count < 1000)
		sprintf(result, "%u", count);
	else if (count < 1000000)
		sprintf(result, "%uk", count/1000);
	else
		sprintf(result, "%.lg", (double)count);

	return result;
}

/**
 * Compute exponentially weighted moving average
 * @mavg:	old value of the moving average
 * @sample:	new sample to update @mavg
 * @weight:	decay factor for new samples, 0 < weight <= 1
 */
static inline double ewma(double mavg, double sample, double weight)
{
	return mavg == 0 ? sample : weight * mavg + (1.0 - weight) * sample;
}

/* map 0.0 <= ratio <= 1.0 into min..max */
static inline double map_val(double ratio, double min, double max)
{
	return min + ratio * (max - min);
}

/* map minv <= val <= maxv into the range min..max (no clamping) */
static inline double map_range(double val, double minv, double maxv,
			       double min, double max)
{
	return map_val((val - minv) / (maxv - minv), min, max);
}

/* map val into the reverse range max..min */
static inline int reverse_range(int val, int min, int max)
{
	assert(min <= val && val <= max);
	return max - (val - min);
}
