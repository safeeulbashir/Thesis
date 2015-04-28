import sys
import glob
import os
import argos_util
import re
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import argparse
import numpy as np

def plot_fitness(files):
    number_re = re.compile(r'\d+')
    populations = {}
    for genfile in files:
        gen_number = int(number_re.findall(os.path.basename(genfile))[0])
        populations[gen_number] = argos_util.read_pop_from_csv(genfile)

    gens = range(len(populations.keys()))

    max_fitness = []
    mean_fitness = []
    min_fitness = []

    for g in gens:
        fitvals = []
        for p in populations[g]:
            fitvals.append(float(p["fitness"]))
        max_fitness.append(np.max(fitvals))
        mean_fitness.append(np.mean(fitvals))
        min_fitness.append(np.min(fitvals))
    matplotlib.rcParams.update({'font.size': 16})
    plt.plot(gens, max_fitness, 'r', label="max")
    plt.plot(gens, mean_fitness, 'k', label="mean")
    plt.plot(gens, min_fitness, 'g', label="min")
    plt.legend(loc='lower right')
    plt.xlabel("generation")
    plt.ylabel("fitness (seeds collected)")
    plt.savefig("fitness.pdf")
    plt.show()

def plot_param_vs_fitness(param, files, threshold=0):
    number_re = re.compile(r'\d+')
    populations = {}
    for genfile in files:
        gen_number = int(number_re.findall(os.path.basename(genfile))[0])
        populations[gen_number] = argos_util.read_pop_from_csv(genfile)

    gens = range(len(populations.keys()))

    fitness = []
    paramvals = []

    threshold = float(threshold)
    for g in gens:
        for p in populations[g]:
            if float(p["fitness"]) > threshold:
                fitness.append(float(p["fitness"]))
                paramvals.append(float(p[param]))

    paramvals = np.array(paramvals)
    fitness = np.array(fitness)
    matplotlib.rcParams.update({'font.size': 16})
    plt.hist2d(paramvals, fitness, bins=20, cmap='Blues')
    plt.colorbar()
    plt.ylabel('fitness (seeds collected)')
    plt.xlabel(param)
    plt.savefig(param + "_heatmap.pdf")
    plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GA plotter')
    parser.add_argument('-f', '--fitness', action='store_true', dest='fitness', help='plot fitness')
    parser.add_argument('-p', '--param', action='store', dest='param', help='Param to plot')
    parser.add_argument('-t', '--threshold', action='store', dest='threshold', help='Param to plot')
    parser.add_argument('directory', action='store')

    args = parser.parse_args()

    directory = args.directory
    files = glob.glob(os.path.join(directory, "*.gapy"))

    threshold = 0
    if args.threshold:
        threshold = args.threshold

    if args.fitness:
        plot_fitness(files)

    if args.param:
        plot_param_vs_fitness(args.param, files, threshold)
