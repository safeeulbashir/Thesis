Using the pyscripts for argos
=============================

The argos code was modified to track when seeds were collected and from which
piles

Requirements
------------

The pyscripts require the python packages seaborn, numpy, matplotlib, and lxml

As CS machines seem to have broken python packages recommended way is
downloading miniconda from continuum software.

http://conda.pydata.org/miniconda.html

This is a bash installer where you install using:

    $ bash Miniconda-latest-Linux-x86_64.sh

Installation will ask where miniconda should be installed and if you want
to add it to your path.

If you don't want to add it to your path simple change your path to point
to the minconda bin for the terminal you are using e.g:

    $ export PATH=$HOME/<miniconda install location>/bin:$PATH

After minconda is installed you should be able to install dependencies:

    $ conda install numpy
    $ conda install matplotlib
    $ conda install lxml
    $ conda install seaborn

Now the scripts can be run with miniconda version of python.

Description of what files do
----------------------------

Utility file: argos_util.py allows grabbing parameters and creating
xml files from evolved data

Genetic Algorithm: ga.py runs the ga with specified settings

Plotting: cusum.py data_plotter.py many_heatmap.py param_bar_plot.py
descriptions in the following sections

argos_util.py
-------------

The argos util can be used to get the best parameters from a generation
or to print an xml file using the best parameters from a generation.

    usage: argos_util.py [-h] -f GEN_FILE [-a ALL] [-s SRADIUS] [-r ROBOTS]
                         [-l LENGTH] [-c] [--system SYSTEM]
    
    CPFA XML printer
    
    optional arguments:
      -h, --help            show this help message and exit
      -f GEN_FILE, --gen_file GEN_FILE
      -a ALL, --all ALL
      -s SRADIUS, --searchradius SRADIUS
      -r ROBOTS, --robots ROBOTS
      -l LENGTH, --length LENGTH
      -c, --create
      --system SYSTEM

Get best parameters:

    $ python pyscripts/argos_util.py -f <path to gen file>/gen_20.argos

For example:

    $ python pyscripts/argos_util.py -f saved_data/smallruns/1429311500_e_1_p_50_r_6_t_3600_k_4/gen_20.gapy
    Fitness: 183.75
    <CPFA pheromoneRate="0.147915435178" pheromoneDecayRate="0.113856834457" travelGiveupProbability="0.40573404851" siteFidelityRate="3.96060449485" informedSearchDecay="0.852988121856" searchRadius="1" searchStepSize="0.08" distanceTolerance="0.1" searchGiveupProbability="0" angleTolerance="22.5" maxRobotSpeed="16.0" uninformedSearchCorrelation="26.5223778359" fitness="183.75" seed="2272063782"/>

With the -a it will print all pararameters of the population in xml form

To create an xml file you use the same -f but also use -c for create

    $ python pyscripts/argos_util.py -c -f saved_data/smallruns/1429311500_e_1_p_50_r_6_t_3600_k_4/gen_20.gapy > output.argos

You can use the robots sradius and length to adjust those settings in the output argos file.

ga.py
-----

ga.py runs the ga using specified parameters, it expects iant controllers to be built and to be run from the directory containing build/ and experiments/. It will create a gapy_saves directory with the output from ga.py

    $ python pyscripts/ga.py -h
    usage: ga.py [-h] [-s SYSTEM] [-r ROBOTS] [-m MUT_RATE] [-e ELITES] [-g GENS]
                 [-p POP_SIZE] [-t TIME] [-k TESTS_PER_GEN]
    
    GA for argos
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SYSTEM, --system SYSTEM
      -r ROBOTS, --robots ROBOTS
      -m MUT_RATE, --mut_rate MUT_RATE
      -e ELITES, --elites ELITES
      -g GENS, --gens GENS
      -p POP_SIZE, --pop_size POP_SIZE
      -t TIME, --time TIME
      -k TESTS_PER_GEN, --tests_per_gen TESTS_PER_GEN

plot_collection.py
------------------

plot collections plots the collection (cumulative sums of iAntFoodPositions.txt file).

     $ python pyscripts/plot_collection.py iAntFoodPosition.txt

data_plotter.py
---------------

Data plotter plots data from whole runs. Specify a directory and type of plot.

    $ python pyscripts/data_plotter.py -h
    usage: data_plotter.py [-h] [-f] [-p PARAM] [-t THRESHOLD] directory
    
    GA plotter
    
    positional arguments:
      directory
    
    optional arguments:
      -h, --help            show this help message and exit
      -f, --fitness         plot fitness
      -p PARAM, --param PARAM
                            Param to plot
      -t THRESHOLD, --threshold THRESHOLD
                            Param to plot

Plot fitness of run:

     $ python pyscripts/dataplotter -f <path to save>/<gapy run directory>

Individual parameter 2dhist can be plotted using -p PARAM where PARAM matches the CPFA input in xml, e.g. pheromoneRate. A threshold fitness can be used to only plot those with THRESHOLD or greater fitness

     $ python pyscripts/data_plotter.py -p pheromoneRate -t 100 <path to save>/<gapy run directory>

many_heatmap.py
---------------

This is basically the same as `data_plotter.py` param plot but can plot many directories instead of just one gapy_save directory

    $ python pyscripts/many_heatmap.py -h
    usage: many_heatmap.py [-h] -p PARAM [-t THRESHOLD]
                           [directories [directories ...]]
    
    GA plotter
    
    positional arguments:
      directories
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PARAM, --param PARAM
                            Param to plot
      -t THRESHOLD, --threshold THRESHOLD
                            Param to plot

Example:

     $ python pyscripts/many_heatmap.py -p siteFidelityRate saved_data/gapy_saves/*



cusum.py
--------

plots CUSUM generated data of iAnt food data generated by modified argos code, creates 3 plots

    $ python pyscripts/cusum.py -h
    usage: cusum.py [-h] [-w WINDOW_SIZE] [-m SLIDE_MOVEMENT] [-l LENGTH]
                    [-p PILE] [-t THRESHOLD] [-d DRIFT]
                    foodfile
    
    CUSUM plotter
    
    positional arguments:
      foodfile
    
    optional arguments:
      -h, --help            show this help message and exit
      -w WINDOW_SIZE, --window WINDOW_SIZE
      -m SLIDE_MOVEMENT, --movement SLIDE_MOVEMENT
      -l LENGTH, --length LENGTH
      -p PILE, --pile PILE
      -t THRESHOLD, --threshold THRESHOLD
      -d DRIFT, --drift DRIFT

param_bar_plot.py
-----------------

Create a bar plot for our part 1 data