PYTHON_INC = -I/usr/include/python3.6
CFLAGS	 ?= -O2 -Wall -pthread -I/usr/include/libnl3

all: wavemon.py _wavemon.so

_wavemon.so: wavemon.o wavemon_wrap.o iw_scan.o iw_nl80211.o iw_if.o scan_scr.o conf.o llist.o utils.o error.o
	ld -shared wavemon.o wavemon_wrap.o iw_scan.o iw_nl80211.o iw_if.o scan_scr.o conf.o llist.o utils.o error.o -o $@ -lm  -lnl-genl-3 -lnl-3 -lnl-3

wavemon_wrap.c: wavemon.py
wavemon.py: wavemon.i wavemon.h llist.h
	swig -python wavemon.i


wavemon.o wavemon_wrap.o scan_scr.o conf.o llist.o: wavemon.c wavemon_wrap.c scan_scr.c conf.c llist.c
	gcc -fPIC -c wavemon.c wavemon_wrap.c scan_scr.c conf.c llist.c $(CFLAGS) $(PYTHON_INC)

iw_scan.o error.o: iw_scan.c error.c
	gcc -fPIC -c iw_scan.c error.c $(CFLAGS) $(PYTHON_INC)

iw_nl80211.o utils.o: iw_nl80211.c utils.c
	gcc -fPIC -c iw_nl80211.c utils.c $(CFLAGS) $(PYTHON_INC)

iw_if.o : iw_if.c
	gcc -fPIC -c iw_if.c $(CFLAGS) $(PYTHON_INC)

clean:
	rm -f wavemon_wrap.c wavemon.py
	rm -f wavemon.o wavemon_wrap.o iw_scan.o iw_scan_wrap.o iw_nl80211.o iw_nl80211_wrap.o iw_if.o iw_if_wrap.o scan_scr.o conf.o llist.o utils.o error.o _wavemon.so
