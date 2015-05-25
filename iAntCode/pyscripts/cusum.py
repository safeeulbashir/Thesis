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

GREEN='#3CB371'
RED='#DC143C'

# Reference implmentation and algorithm:
# http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectCUSUM.ipynb

def plot_sliding_window(x, threshold, drift, gp, gn,plus_alarms,minus_alarms):
    """Plot results of the detect_cusum function"""
    _, (ax1) = plt.subplots(1, 1, figsize=(8, 6))
    gp1=np.asarray(gp)
    x1=np.asarray(x)
    t = range(x1.size)
    ax1.plot(t, x, 'b-', lw=2)
    if len(plus_alarms):
        ax1.plot(plus_alarms, x1[plus_alarms], '^', mfc=GREEN, mec=GREEN, ms=10,
                 label='Positive Change Points')	
        ax1.legend(loc='best', framealpha=.5, numpoints=1)
    if len(minus_alarms):
        ax1.plot(minus_alarms, x1[minus_alarms], 'v', mfc=RED, mec=RED, ms=10,
                 label='Negetive Change Points')	
        ax1.legend(loc='best', framealpha=.5, numpoints=1)
    ax1.set_xlim(-.01*x1.size, x1.size*1.01-1)
    ax1.set_xlabel('Sliding window', fontsize=14)
    ax1.set_ylabel('Seeds in window', fontsize=14)
    ymin, ymax = x1[np.isfinite(x1)].min(), x1[np.isfinite(x1)].max()
    yrange = ymax - ymin if ymax > ymin else 1
    ax1.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CUSUM plotter')
    parser.add_argument('-w', '--window', action='store', dest='window_size', type=int)
    parser.add_argument('-m', '--movement', action='store', dest='slide_movement',type=int)
    parser.add_argument('-l', '--length', action='store', dest='length', type=int)
    parser.add_argument('-p', '--pile', action='store', dest='pile', type=int)
    parser.add_argument('-t', '--threshold', action='store', dest='threshold', type=float)
    parser.add_argument('-d', '--drift', action='store', dest='drift', type=float)
    parser.add_argument('foodfile', action='store')

    args = parser.parse_args()

    length = 3600
    if args.length:
        length = args.length

    window_size = 60
    if args.window_size:
        window_size = args.window_size

    slide_movement = 10
    if args.slide_movement:
        slide_movement = args.slide_movement

    pile = 1
    if args.pile:
        pile = args.pile

    drift = 1
    if args.drift:
        drift = args.drift
        
    threshold = 1
    if args.threshold:
        threshold = 1
        
    key_types = {'Distribution Type': int,
     'Ant ID': int,
     'Pile ID': int,
     'Y-Position': float,
     'Collection Time': int,
     'X-Position': float}
    
    with open(args.foodfile, 'r') as csvfile:
        reader = csv.DictReader(csvfile.readlines(), delimiter="\t")
        
    reader = list(reader)
    data = {}
    for key in key_types:
        data[key] = []
        for row in reader:
            data[key].append(key_types[key](row[key]))
    
    dist_types = set(data['Distribution Type'])

    
    collection_times = {}
    sliding_windows = {}
    for d in dist_types:
        collection_times[d] = np.zeros(length)
        sliding_windows[d] = []
    
    for d, t in zip(data['Distribution Type'], data['Collection Time']):
        if t >= 0:
            t = t / 16
            collection_times[d][t] += 1
    
    for i in xrange(0, int(length / slide_movement)):
        slmax = min(length,window_size + i * slide_movement)
        for d in dist_types:
            sl = collection_times[d][(i*slide_movement):slmax]
            sliding_windows[d].append(np.sum(sl))
    
    # CUSUM starts here
    s = []
    gp = [0]
    gm = [0]
    x = sliding_windows[pile] # For Changing Sliding Windows
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

    # First figure is figure with full timescale
    plt.figure()
    offsets = map(lambda x: x * slide_movement, np.arange(len(x)))
    plt.bar(offsets,x,slide_movement,color='b',ec='none', alpha=0.4)
    for p in plus_alarms:
        plt.plot(p * slide_movement, x[p], marker='^', mec=GREEN, color=GREEN, ms=10)
    for m in minus_alarms:
        plt.plot(m * slide_movement, x[m], marker='v', mec=GREEN, color=RED, ms=10)
    plt.axis([0, length, 0, np.max(x) +1])
    plt.xlabel("Time (s)")
    plt.ylabel("Seeds in window")
    plt.show()

    # second figure is figure with only sliding window locations
    plot_sliding_window(x, threshold, drift,gp, gm,plus_alarms,minus_alarms)
    
    # Third plot is of mins and max values
    plt.figure()
    plt.plot(gp, label='positive', color=GREEN)
    plt.plot(gm, label='negative', color=RED)
    plt.legend(loc='best')
    plt.xlabel("Sliding Window")
    plt.ylabel("CUSUM value")
    plt.show()
    
    
