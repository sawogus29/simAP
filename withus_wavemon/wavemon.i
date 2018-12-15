%module wavemon

%{
#include "wavemon.h"
#include <setjmp.h>
%}
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

%extend AP{
	const AP __getitem__(int i){
		return $self[i];
	}
}
