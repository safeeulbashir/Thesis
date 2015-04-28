from lxml import etree
import numpy as np
import copy
import csv
import argparse


LINUX_CONTROLLER_LIB = "build/controllers/libiAnt_controller.so"
MAC_CONTROLLER_LIB = "build/controllers/libiAnt_controller.dylib"
LINUX_LOOP_LIB = "build/loop_functions/libiAnt_loop_functions.so"
MAC_LOOP_LIB = "build/loop_functions/libiAnt_loop_functions.dylib"
ARGOS_XML_DEFAULT = '''<?xml version="1.0"?>
<argos-configuration>

    <framework>
        <system threads="0" />
        <experiment length="3600" ticks_per_second="16" random_seed="100" />
    </framework>

    <controllers>
        <iAnt_controller id="iAnt_c" library="build/controllers/libiAnt_controller.so">
            <actuators>
                <differential_steering implementation="default" />
            </actuators>
            <sensors>
                <footbot_proximity implementation="default" show_rays="false" />
                <positioning implementation="default" />
            </sensors>
            <params>
                <CPFA pheromoneRate="10"
                      pheromoneDecayRate="0.01"
                      travelGiveupProbability="0.95"
                      siteFidelityRate="10"
                      informedSearchDecay="0.01"
                      searchRadius="1"
                      searchStepSize="0.08"
                      distanceTolerance="0.1"
                      searchGiveupProbability="0.000001"
                      angleTolerance="22.5"
                      maxRobotSpeed="16.0"
                      uninformedSearchCorrelation="13.25" />
            </params>
        </iAnt_controller>
    </controllers>

    <loop_functions library="build/loop_functions/libiAnt_loop_functions.so"
                    label="iAnt_loop_functions">

        <simulation_settings variableSeed="0"
                             outputData="1"
                             nestPosition="0.0, 0.0"
                             nestRadius="0.5"
                             foodRadius="0.05"
                             foodItemCount="0"
                             foodDistribution="2" />

        <random_distribution_0/> <!-- no settings for this distribution -->
        <cluster_distribution_1  numberOfClusters="6"
                                 clusterWidthX="6"
                                 clusterLengthY="6"/>
        <powerLaw_distribution_2 powerRank="5" />

    </loop_functions>

    <arena size="20.0, 20.0, 0.0" center="0.0, 0.0, 0.0">
        <floor id="floor" source="loop_functions" pixels_per_meter="50" />
        <distribute>
            <position method="uniform" min="-1, -1, 0" max="1, 1, 0" />
            <orientation method="gaussian" mean="0, 0, 0" std_dev="360, 0, 0" />
            <entity quantity="1" max_trials="200">
                <foot-bot id="fb">
                    <controller config="iAnt_c" />
                </foot-bot>
            </entity>
        </distribute>
    </arena>

    <physics_engines>
        <dynamics2d id="dyn2d" />
    </physics_engines>

    <media>
        <led id="leds" />
    </media>

</argos-configuration>
'''


CPFA_LIMITS = {
    "pheromoneRate": (0, 20),
    "pheromoneDecayRate": (0, 1),
    "travelGiveupProbability": (0, 1),
    "siteFidelityRate": (0, 20),
    "informedSearchDecay": (0, 1),
    "searchGiveupProbability": (0, 1),
    "uninformedSearchCorrelation": (0, 359)
}


def default_argos_xml(robots, time, system="linux"):
    xml = etree.fromstring(ARGOS_XML_DEFAULT)
    xml.find("arena").find("distribute").find(
        "entity").attrib["quantity"] = str(robots)
    exp_att = xml.find("framework").find("experiment").attrib
    exp_att.update({"length": str(time)})

    if system == "linux":
        return xml
    elif system == "darwin":
        xml.find("controllers").find(
            "iAnt_controller").attrib["library"] = MAC_CONTROLLER_LIB
        xml.find("loop_functions").attrib["library"] = MAC_LOOP_LIB
        return xml
    else:
        return None


def uniform_rand_argos_xml(robots, time, system="linux"):
    xml = default_argos_xml(robots, time, system)
    cpfa = {}
    for key in CPFA_LIMITS:
        cpfa[key] = str(np.random.uniform(CPFA_LIMITS[key][0], CPFA_LIMITS[key][1]))
    set_cpfa(xml, cpfa)
    return xml


def get_cpfa(argos_xml):
    return argos_xml.find("controllers").find(
        "iAnt_controller").find("params").find("CPFA").attrib


def set_cpfa(argos_xml, cpfa_update):
    attrib = argos_xml.find("controllers").find(
        "iAnt_controller").find("params").find("CPFA").attrib
    attrib.update(cpfa_update)


def set_seed(argos_xml, seed):
    attrib = argos_xml.find("framework").find("experiment").attrib
    attrib.update({"random_seed": str(int(seed))})


def mutate_cpfa(argos_xml, probability):
    cpfa = get_cpfa(argos_xml)
    for key in CPFA_LIMITS:
        if np.random.uniform() > probability:
            val = float(cpfa[key])
            val += np.random.normal(0, 0.05)
            if val > CPFA_LIMITS[key][1]:
                val = CPFA_LIMITS[key][1]
            elif val < CPFA_LIMITS[key][0]:
                val = CPFA_LIMITS[key][0]
            cpfa[key] = str(val)
    set_cpfa(argos_xml, cpfa)


def uniform_crossover(p1_xml, p2_xml, system="linux"):
    p1_cpfa = copy.deepcopy(get_cpfa(p1_xml))
    # Initialize child to parent 2 cpfa
    child_cpfa = copy.deepcopy(get_cpfa(p2_xml))
    from_p1 = False
    for key in CPFA_LIMITS:
        if from_p1:
            child_cpfa[key] = p1_cpfa[key]
        from_p1 = not from_p1
    parent_time = p1_xml.find("framework").find("experiment").attrib["length"]
    parent_robots = p1_xml.find("arena").find("distribute").find(
        "entity").attrib["quantity"]
    child = default_argos_xml(system=system, time=parent_time, robots=parent_robots)
    set_cpfa(child, child_cpfa)
    return child

def read_pop_from_csv(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def xml_string_cpfa_chunk(cpfa):
    xml = default_argos_xml(6, 3600)
    cpfa_xml = xml.find("controllers").find(
        "iAnt_controller").find("params").find("CPFA")
    cpfa_xml.attrib.update(cpfa)
    return etree.tostring(cpfa_xml)

def create_argos_from_cpfa(cpfa, searchRadius, robots, length, system):
    xml = default_argos_xml(robots, length, system)
    cpfa_xml = xml.find("controllers").find(
        "iAnt_controller").find("params").find("CPFA")
    cpfa_xml.attrib.update(cpfa)
    cpfa_xml.attrib["searchRadius"] = searchRadius
    return etree.tostring(xml, pretty_print=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CPFA XML printer')
    parser.add_argument('-f', '--gen_file', action='store', dest='gen_file', required=True)
    parser.add_argument('-a', '--all', action='store', dest='all')
    parser.add_argument('-s', '--searchradius', action='store', dest='sradius')
    parser.add_argument('-r', '--robots', action="store", dest="robots")
    parser.add_argument('-l', '--length', action='store', dest='length')
    parser.add_argument('-c', '--create', action="store_true", dest="create")
    parser.add_argument('--system', action='store', dest='system')

    args = parser.parse_args()

    gen_file = args.gen_file
    robots='6'
    length='3600'
    sradius='1'
    system='linux'

    pop = read_pop_from_csv(gen_file)
    
    if args.create:
        if args.length:
            length=args.length
        if args.sradius:
            sradius=args.sradius
        if args.robots:
            robots=args.robots
        if args.system:
            system = args.system
        print create_argos_from_cpfa(pop[0], sradius, robots, length, system)
    elif args.all:
        for p in pop:
            print "Fitness:", p["fitness"]
            print xml_string_cpfa_chunk(p)
    else:
        print "Fitness:", pop[0]["fitness"]
        print xml_string_cpfa_chunk(pop[0])
