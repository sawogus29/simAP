/*
 * wavemon - a wireless network monitoring aplication
 *
 * Copyright (c) 2001-2002 Jan Morgenstern <jan@jm-music.de>
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
#include "iw_if.h"

/* GLOBALS */
static struct scan_result sr;
static pthread_t scan_thread;

/**
 * Sanitize and format single scan entry as a string.
 * @cur: entry to format
 * @buf: buffer to put results into
 * @buflen: length of @buf
 */

void fmt_scan_entry(struct scan_entry *cur)
{
	if (cur->bss_signal) {
		float sig_qual, sig_qual_max;

		if (cur->bss_signal_qual) {
			/* BSS_SIGNAL_UNSPEC is scaled 0..100 */
			sig_qual     = cur->bss_signal_qual;
			sig_qual_max = 100;
		} else {
			if (cur->bss_signal < -110)
				sig_qual = 0;
			else if (cur->bss_signal > -40)
				sig_qual = 70;
			else
				sig_qual = cur->bss_signal + 110;
			sig_qual_max = 70;
		}
		cur->bss_signal_qual=(1E2 * sig_qual)/ sig_qual_max;
	} else if (cur->bss_signal_qual) {
		cur->bss_signal_qual=cur->bss_signal_qual;
	}

/*	if (cur->bss_capa & WLAN_CAPABILITY_ESS) {
		if (cur->bss_sta_count || cur->bss_chan_usage > 2) {
			if (cur->bss_sta_count)
				 len += snprintf(buf + len, buflen - len, " %u sta", cur->bss_sta_count);
			if (cur->bss_chan_usage > 2)*/ /* 1% is 2.55 */
}
void scr_aplst_init(wirelessSearch* ws)
{
	struct scan_entry *cur;
  int maxEntryNum=0, i=0;
	AP *tmp;

	init_scan_list(&sr);
	pthread_create(&scan_thread, NULL, do_scan, &sr);
	pthread_join(scan_thread, NULL);

	pthread_mutex_lock(&sr.mutex);
	if(sr.num.entries >10){
		maxEntryNum=10;
		ws->entryNum=10;
	}
	else{
		maxEntryNum=sr.num.entries;
		ws->entryNum=maxEntryNum;
	}
	ws->twoGig=0;
	ws->fiveGig=0;
	for (cur = sr.head; i<maxEntryNum; cur = cur->next, i++) {
		fmt_scan_entry(cur);
		tmp=&(ws->APlist[i]);
		strcpy(tmp->mac, ether_ntoa(&(cur->ap_addr)));
		tmp->freq=cur->freq;
		if(tmp->freq<3000){
			ws->twoGig++;
		}
		else{
			ws->fiveGig++;
		}
		tmp->chan=cur->chan;
		tmp->has_key=cur->has_key;
		tmp->tsf=cur->tsf;
		tmp->last_seen=cur->last_seen;
		tmp->bss_signal=cur->bss_signal;
		tmp->bss_signal_qual=cur->bss_signal_qual;
		tmp->bss_sta_count=cur->bss_sta_count;
		tmp->bss_chan_usage=cur->bss_chan_usage;
		if(!strcmp(cur->essid, "")){
			strcpy(tmp->essid, "<hidden ESSID>");
		}
		else{
			strcpy(tmp->essid, cur->essid);
		}
	}
	pthread_mutex_unlock(&sr.mutex);

}

void scr_aplst_fini(void)
{
	free_scan_list(sr.head);
	free(sr.channel_stats);
}
