import sys
import random
import copy
import json
import os
from configs.standard import *

def generate_sge_individual():
    decimal_genome = [[] for key in GRAMMAR.get_non_terminals()]
    size_of_gene = GRAMMAR.count_number_of_options_in_production()
    start_symbol = GRAMMAR.start_rule[0]
    tree_depth = GRAMMAR.recursive_individual_creation(decimal_genome, start_symbol, size_of_gene, 0)
    return decimal_genome, tree_depth

model = {
            'generate': generate_sge_individual,
            'mutate': lambda current_gene, max_gene: random.choice([i for i in xrange(max_gene)])
}

def generate_random_individual():
    genotype, tree_depth = model['generate']()
    return {'genotype': genotype, 'fitness': None, 'tree_depth' : tree_depth}


def generate_initial_population():
    for i in range(POPULATION_SIZE):
        yield generate_random_individual()


def evaluate(ind, eval_func):
    mapping_values = [0 for i in ind['genotype']]
    phen, tree_depth = GRAMMAR.mapping(ind['genotype'], mapping_values)
    quality, other_info = eval_func.evaluate(phen)
    if ADD_PHENOTYPE_TO_JSON_OBJECT:
        ind['phenotype'] = phen
    ind['fitness'] = quality
    ind['other_info'] = other_info
    ind['mapping_values'] = mapping_values
    ind['tree_depth'] = tree_depth


def choose_indiv(population):
    pool = random.sample(population, TOURNAMENT)
    pool.sort(key=lambda i: i['fitness'])
    return copy.deepcopy(pool[0])


def crossover(p1, p2):
    xover_p_value = 0.5
    mask = [random.random() for i in xrange(GRAMMAR.count_number_of_non_terminals())]
    genotype = []
    gen_size = len(p1['genotype'])
    mapping_values = []
    for index, prob in enumerate(mask):
        if prob < xover_p_value:
            genotype.append(p1['genotype'][index][ : ])
        else:
            genotype.append(p2['genotype'][index][ : ])
    mapping_values = [0] * gen_size
    _ ,tree_depth = GRAMMAR.mapping(genotype, mapping_values)
    return {'genotype': genotype, 'fitness': None, 'mapping_values' : mapping_values, 'tree_depth' : tree_depth}


def mutate(p):
    p = copy.deepcopy(p)
    p['fitness'] = None
    size_of_genes = GRAMMAR.count_number_of_options_in_production()
    mutable_genes = [index for index, nt in enumerate(GRAMMAR.get_non_terminals()) if size_of_genes[nt] != 1 and len(p['genotype'][index]) > 0]
    #print p['genotype']
    #print mutable_genes
    for at_gene in mutable_genes:
        nt = list(GRAMMAR.get_non_terminals())[at_gene]
        temp = p['mapping_values']
        mapped = temp[at_gene]
        for position_to_mutate in xrange(0, mapped):
            #print PROB_MUTATION(mapped)
            if random.random() < PROB_MUTATION(mapped):
                #print "Mutate"
                #print position_to_mutate
                #print p['genotype'][at_gene][0]
                current_value = p['genotype'][at_gene][position_to_mutate]
                #print "Tree depth: " + str(p['tree_depth'])
                choices = []
                if p['tree_depth'] >= GRAMMAR.max_depth:
                    #print nt
                    choices = GRAMMAR.non_recursive_options[nt]
                else:
                    choices = range(0, size_of_genes[nt])
                    choices.remove(current_value)
                if len(choices) == 0:
                    choices = range(0, size_of_genes[nt])
                p['genotype'][at_gene][position_to_mutate] = random.choice(choices)
    return p


def prepare_dumps(experience_name):
    os.makedirs('dumps/%s/run_%d' % (experience_name, RUN))


def save(population, it, experience_name):
    to_save = []
    app = to_save.append
    for ind in population:
        cp_ind = {}
        for key, value in ind.iteritems():
            if key != 'genotype':
                cp_ind[key] = value
        app(cp_ind)
    c = json.dumps(to_save)
    open('dumps/%s/run_%d/iteration_%d.json' % (experience_name, RUN, it), 'w').write(c)


def save_progress_report(progress_report, experience_name):
    open('dumps/%s/run_%d/progress_report.csv' % (experience_name, RUN), 'w').write(progress_report)


def evolutionary_algorithm(grammar = "", exp_name = "", eval_func = ""):
    global GRAMMAR
    experience_name = exp_name
    GRAMMAR = grammar
    random.seed(SEED)
    stats = ""
    progress_report = "Generation,Best,Mean\n"
    prepare_dumps(experience_name)
    if len(sys.argv) > 2:
        population = json.load(open(sys.argv[2]))
        it = int(sys.argv[2].split(".")[0].split("_")[-1])
    else:
        population = list(generate_initial_population())
        it = 0
    for it in range(it, NUMBER_OF_ITERATIONS):
        for i in population:
            if i['fitness'] == None:
                evaluate(i, eval_func)
        population.sort(key = lambda x: x['fitness'])
        best = population[0]
        if 'test_error' in best['other_info']:
            stats = "" + str(it) + "," + str(best['fitness']) + "," + str((float(sum([ind['fitness'] for ind in population])) / float(POPULATION_SIZE))) + "," + str(best['tree_depth']) + "," + str(best['other_info']['test_error'])
        else:
            stats = "" + str(it) + "," + str(best['fitness']) + "," + str((float(sum([ind['fitness'] for ind in population])) / float(POPULATION_SIZE))) + "," + str(best['tree_depth'])
        print stats#, best['phenotype']
        progress_report += stats + "\n"

        if it in sampling_snap:
            save(population, it, experience_name)
        new_population = population[:ELITISM]

        while len(new_population) < POPULATION_SIZE:
            if random.random() < PROB_CROSSOVER:
                p1 = choose_indiv(population)
                p2 = choose_indiv(population)
                ni = crossover(p1, p2)
            else:
                ni = choose_indiv(population)
            ni = mutate(ni)
            new_population.append(ni)
        population = new_population
    save_progress_report(progress_report, experience_name)
