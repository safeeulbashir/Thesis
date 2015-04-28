import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def_random = np.mean([184,177,161,171,182])
def_cluster = np.mean([208,212,177,205,199])
def_power = np.mean([200,214,189,197,201])

pher_random = np.mean([179,180,156,186,170])
pher_cluster = np.mean([202,205,176,208,216])
pher_power = np.mean([193,200,202,202,196])

site_random = np.mean([184,220,199,170,201])
site_cluster = np.mean([205,196,177,206,192])
site_power = np.mean([193,207,184,183,198])

bar_width=0.25
index = np.arange(3)

default = (def_random, def_cluster, def_power)

pher = (pher_random, pher_cluster,pher_power)

site = (site_random, site_cluster, site_power)

fig, ax = plt.subplots()

opacity = 0.4

rects1 = plt.bar(index, default, bar_width,
                 alpha=opacity,
                 color='b',
                 label="default")

rects2 = plt.bar(index+bar_width, pher, bar_width,
                 alpha=opacity,
                 color='r',
                 label="no site fidelity")

rects3 = plt.bar(index+bar_width+bar_width, site, bar_width,
                 alpha=opacity,
                 color='g',
                 label="no pheromone")

matplotlib.rcParams.update({'font.size': 16})

plt.xlabel('Distribution Type')
plt.ylabel('Seeds Collected (mean)')
plt.xticks(index + 1.5*bar_width, ('random', 'cluster', 'power law'))
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('param_bar.pdf')
plt.show()


def_random = np.mean([184,177,161,171,182])
def_cluster = np.mean([208,212,177,205,199])
def_power = np.mean([200,214,189,197,201])

pher_random = np.mean([169,177,176,169,195])
pher_cluster = np.mean([200,205,176,205,178])
pher_power = np.mean([202,200,195,199,201])

site_random = np.mean([171,173,168,183,180])
site_cluster = np.mean([208,214,177,201,212])
site_power = np.mean([184,194,195,205,188])

bar_width=0.25
index = np.arange(3)

default = (def_random, def_cluster, def_power)

pher = (pher_random, pher_cluster,pher_power)

site = (site_random, site_cluster, site_power)

fig, ax = plt.subplots()

opacity = 0.4

rects1 = plt.bar(index, default, bar_width,
                 alpha=opacity,
                 color='b',
                 label="default")

rects2 = plt.bar(index+bar_width, pher, bar_width,
                 alpha=opacity,
                 color='r',
                 label="no site fidelity")

rects3 = plt.bar(index+bar_width+bar_width, site, bar_width,
                 alpha=opacity,
                 color='g',
                 label="no pheromone")

matplotlib.rcParams.update({'font.size': 16})

plt.xlabel('Distribution Type')
plt.ylabel('Seeds Collected (mean)')
plt.xticks(index + 1.5*bar_width, ('random', 'cluster', 'power law'))
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('param_bar_old.pdf')
plt.show()
