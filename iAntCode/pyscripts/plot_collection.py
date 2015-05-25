import sys
import glob
import os
import argos_util
import re
import matplotlib.pyplot as plt
import numpy as np
import argparse
import numpy as np
import seaborn as sns
import csv
sns.set_palette("husl")
sns.set(style="whitegrid")

key_types = {'Distribution Type': int,
 'Ant ID': int,
 'Pile ID': int,
 'Y-Position': float,
 'Collection Time': int,
 'X-Position': float}

print sys.argv[1]
with open(sys.argv[1], 'r') as csvfile:
    reader = csv.DictReader(csvfile.readlines(), delimiter="\t")
reader = list(reader)
data = {}
for key in key_types:
    data[key] = []
    for row in reader:
        data[key].append(key_types[key](row[key]))

minutes = range(np.max(data['Collection Time'])/ 16 / 60 + 1)

cumulative_sums = {}

for i, t in enumerate(data['Collection Time']):
    if t != -1:
        t = t / 16 / 60
        id = data["Distribution Type"][i]
        if id not in cumulative_sums:
            cumulative_sums[id] = np.zeros(len(minutes))
        for m in minutes:
            if m >= t:
                cumulative_sums[id][m] += 1

plt.figure()
plt.hold(True)
for id in sorted(cumulative_sums.keys()):
    plt.plot(minutes, cumulative_sums[id], label=str(id))
plt.xlabel('time (min)')
plt.ylabel('seeds collected')
plt.legend(loc='best')
plt.show()