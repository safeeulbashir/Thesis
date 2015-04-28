import sys
import glob
import os
import argos_util
import re
import matplotlib.pyplot as plt
import numpy as np
import argparse
import numpy as np
import csv

# Reference implmentation and algorithm:
# http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectCUSUM.ipynb

def _plot(x, threshold, drift, gp, gn,plus_alarms,minus_alarms):
    """Plot results of the detect_cusum function, see its help."""

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        _, (ax1) = plt.subplots(1, 1, figsize=(8, 6))
	gp1=np.asarray(gp)
	x1=np.asarray(x)
        t = range(x1.size)
        ax1.plot(t, x, 'b-', lw=2)
	if len(plus_alarms):
            ax1.plot(plus_alarms, x1[plus_alarms], '^', mfc='g', mec='g', ms=10,
                     label='Positive Change Points')	
            ax1.legend(loc='best', framealpha=.5, numpoints=1)
	if len(minus_alarms):
            ax1.plot(minus_alarms, x1[minus_alarms], 'v', mfc='r', mec='r', ms=10,
                     label='Negetive Change Points')	
            ax1.legend(loc='best', framealpha=.5, numpoints=1)
                
	ax1.set_xlim(-.01*x1.size, x1.size*1.01-1)
        ax1.set_xlabel('Sliding Window #', fontsize=14)
        ax1.set_ylabel('Seed Collection Rate', fontsize=14)
        ymin, ymax = x1[np.isfinite(x1)].min(), x1[np.isfinite(x1)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax1.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
        plt.tight_layout()
        plt.show()
key_types = {'Distribution Type': int,
 'Ant ID': int,
 'Pile ID': int,
 'Y-Position': float,
 'Collection Time': int,
 'X-Position': float}

with open(sys.argv[1], 'r') as csvfile:
    reader = csv.DictReader(csvfile.readlines(), delimiter="\t")
reader = list(reader)
data = {}
for key in key_types:
    data[key] = []
    for row in reader:
        data[key].append(key_types[key](row[key]))

dist_types = set(data['Distribution Type'])

length = 3600

collection_times = {}
sliding_windows = {}
for d in dist_types:
    collection_times[d] = np.zeros(length)
    sliding_windows[d] = []

for d, t in zip(data['Distribution Type'], data['Collection Time']):
    if t >= 0:
        t = t / 16
        collection_times[d][t] += 1

window_size = 60
slide_movement = 10

for i in xrange(0, int(length / slide_movement)):
    slmax = min(length,window_size + i * slide_movement)
    for d in dist_types:
        sl = collection_times[d][(i*slide_movement):slmax]
        sliding_windows[d].append(np.sum(sl))


s = []
gp = [0]
gm = [0]
x = sliding_windows[1] # For Changing Sliding Windows
drift = 1
threshold = 1
plus_alarms = []
minus_alarms = []
for i in xrange(0, len(x)):
    s.append(x[i] - x[i-1])
    gp.append(max(0, gp[i] + s[i] - drift))
    gm.append(max(0, gm[i] - s[i] - drift))
    if gp[i+1] > threshold or gm[i+1] > threshold:
        if gp[i+1] > threshold:
            print "Plus Alarm at", i
            plus_alarms.append(i)
        else:
            print "Minus Alarm at", i
            minus_alarms.append(i)
            
        gp[i+1] = 0
        gm[i+1] = 0

	
#print len(x)
_plot(x, threshold, drift,gp, gm,plus_alarms,minus_alarms)


