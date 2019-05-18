'''
Created on 20 Mar 2019

@author: yuliavoevodskaya
'''

import random, math, codecs, os.path, numpy
from math import log, exp

ZeroLimit = numpy.nextafter(numpy.nextafter(0, 1), 1)
def isZero(x):
    return (x < ZeroLimit) and (x > (-ZeroLimit))

def tribbles_one_path(prob_choose_mountains, prob_rain, nb_children, init_population, nb_generations, no_voids):
    
    population = init_population
    
    for _ in range(nb_generations):
        weather = random.random()
        population_mountains = round(population * prob_choose_mountains)
        if no_voids:
            if population_mountains < 1: # at least one tribble lives in the mountains
                population_mountains = 1
            if population_mountains > (population - 1): # at least one tribble lives in the valley
                population_mountains = population - 1
        if weather > prob_rain: 
            population = (population - population_mountains) * nb_children
        else: 
            population = population_mountains * nb_children
        # print(population)
    return population

def get_tribbles_survival_probability_growth_MC(nb_paths, prob_choose_mountains, prob_rain, nb_children, init_population, nb_generations, no_voids):
    
    nb_extint = 0.
    total_population_growth = 0.0
    total_population_growth_sqr = 0.0
    total_population_growth_log = 0.0
    total_population_growth_log_sqr = 0.0
    
    for _ in range(nb_paths):
        population = tribbles_one_path(prob_choose_mountains=prob_choose_mountains, 
                                       prob_rain=prob_rain, 
                                       nb_children=nb_children, 
                                       init_population=init_population, 
                                       nb_generations=nb_generations,
                                       no_voids=no_voids)
        if population < 1.0:
            nb_extint += 1.
        else:
            population_growth = population / (nb_children * init_population)
            total_population_growth += population_growth
            total_population_growth_sqr += population_growth * population_growth
            population_growth_rate = math.log(population_growth) / nb_generations
            total_population_growth_log += population_growth_rate
            total_population_growth_log_sqr += population_growth_rate * population_growth_rate
    variance=(total_population_growth_sqr 
            - total_population_growth * total_population_growth / nb_paths) / (nb_paths - 1) 
    variance_log = (total_population_growth_log_sqr 
            - total_population_growth_log * total_population_growth_log / nb_paths) / (nb_paths - 1)
         
    return [1.0 - (nb_extint / nb_paths), 
            total_population_growth / nb_paths, 
            math.sqrt(max(variance, 0.0) / nb_paths), 
            total_population_growth_log / nb_paths, 
            math.sqrt(max(variance_log, 0.0) / nb_paths)]
    
def get_tribbles_survival_probability_growth_CF(prob_choose_mountains, prob_rain, nb_children, nb_generations, thresholds_ES):
    expected_nb_tribbles_all_valley = (nb_children * (1. - prob_rain)) ** nb_generations
    expected_nb_tribbles = (nb_children * (prob_rain * prob_choose_mountains + (1 - prob_rain) * (1 - prob_choose_mountains))) ** nb_generations
    
    expected_variance_all_valley = nb_children ** (2 * nb_generations) * \
        ((1 - prob_rain) ** nb_generations - (1 - prob_rain) ** (2 * nb_generations))
         
    expected_variance = nb_children ** (2 * nb_generations) * \
        ((prob_rain * (prob_choose_mountains ** 2) + (1 - prob_rain) * ((1 - prob_choose_mountains) ** 2)) ** nb_generations \
           - ((prob_rain * prob_choose_mountains + (1 - prob_rain) * (1 - prob_choose_mountains))) ** (2 * nb_generations))
        
    expected_nb_tribbles_reduction = 1 - expected_nb_tribbles/expected_nb_tribbles_all_valley                        
    expected_variance_reduction = 1 - expected_variance / expected_variance_all_valley
    
    if isZero(prob_choose_mountains):
        expected_log_growth = -math.inf
    else:
        expected_log_growth = nb_generations * (log(nb_children) + prob_rain * log(prob_choose_mountains) \
                                                        + (1 - prob_rain) *  log(1 - prob_choose_mountains)) 
    
    result = [expected_nb_tribbles, expected_nb_tribbles_reduction, expected_variance, expected_variance_reduction, expected_log_growth]
    # initial values
    prob_number_sunny_days =  prob_rain ** nb_generations
    if isZero(prob_choose_mountains):
        nb_tribble_given_number_sunny_days = 0
    else:
        nb_tribble_given_number_sunny_days = (nb_children * prob_choose_mountains) ** nb_generations
        if isZero(nb_tribble_given_number_sunny_days):
            raise Exception('nb_tribble_given_number_sunny_days underflow')                            
    # initial cumul values
    cum_prob_number_sunny_days = 0.
    cum_expected_shortfall_before_norm = 0.
    # run
    ES_counter = 0
    ES_values = []
    for i in range(1, nb_generations+1):
        
        new_cum_prob_number_sunny_days = cum_prob_number_sunny_days + prob_number_sunny_days
        new_cum_expected_shortfall_before_norm = cum_expected_shortfall_before_norm + nb_tribble_given_number_sunny_days
        
        if ES_counter == len(thresholds_ES):
            break
        # add ES values - could be none, one or several
        while (new_cum_prob_number_sunny_days >= thresholds_ES[ES_counter]):
            scaling_factor = (thresholds_ES[ES_counter] - cum_prob_number_sunny_days) \
                                / (new_cum_prob_number_sunny_days - cum_prob_number_sunny_days)
            avg_cum_expected_shortfall_before_norm = (new_cum_expected_shortfall_before_norm * scaling_factor
                                                            + cum_expected_shortfall_before_norm * (1 - scaling_factor))
            ES_values.append(avg_cum_expected_shortfall_before_norm / (thresholds_ES[ES_counter] * expected_nb_tribbles_all_valley))
            ES_counter += 1
            if ES_counter == len(thresholds_ES):
                break
        
        # get ready for the next iteration
        prob_number_sunny_days *= ((nb_generations - i + 1.) / i) * ((1. - prob_rain) / prob_rain);
        if isZero(prob_choose_mountains):
            nb_tribble_given_number_sunny_days = 0
        else:
            nb_tribble_given_number_sunny_days *= (1. - prob_choose_mountains) / prob_choose_mountains
            #print(nb_tribble_given_number_sunny_days)
        
        cum_prob_number_sunny_days = new_cum_prob_number_sunny_days
        cum_expected_shortfall_before_norm = new_cum_expected_shortfall_before_norm
        
    result += ES_values
    return result
                
def write_to_file(file_path, file_content, my_encoding='utf-8'):
    with codecs.open(file_path, 'w', encoding=my_encoding) as the_file:
        the_file.writelines([(','.join([str(x) for x in an_array]) + '\n') for an_array in file_content])

if __name__ == '__main__':
    file_path = os.path.expanduser('~/Documents/Sites/wordpress-yu51a5/tribbles.csv')
    title_line = ['nb children', 'prob rain', 'prob mountains', 
                                          # 'prob population survival', 'growth', 'growth std dev', 'growth rate', 'growth rate std dev']
                    'expected nb tribbles', 'expected nb tribbles reduction', 'expected variance', 'expected variance reduction',
                    'log growth']
    #init_population=4000 
    nb_generations=100
    thresholds_ES=[0.001, 0.01, 0.05]
    title_line += ['normalized ES @ ' + str((1-tr) * 100) + '%' for tr in thresholds_ES]
    file_contents = [title_line]
    for nb_children in (2, 3, 5, 8):
        for percentage_rains in range(1, 10):
            values_percentage_choose_mountains = [0, 0.1, 1, 2]
            if percentage_rains > 2:
                values_percentage_choose_mountains += [percentage_rains, percentage_rains + 1]
            if percentage_rains == 2:
                values_percentage_choose_mountains += [3]
            values_percentage_choose_mountains += [20, 49]
            for percentage_choose_mountains in values_percentage_choose_mountains:
                new_line = [nb_children, percentage_rains / 100.0, percentage_choose_mountains / 100.0]
                result = get_tribbles_survival_probability_growth_CF(
                                prob_choose_mountains=percentage_choose_mountains / 100.0, 
                                prob_rain=percentage_rains / 100.0, 
                                nb_children=nb_children, 
                                nb_generations=nb_generations, 
                                thresholds_ES=thresholds_ES)
                new_line += result
#                 try:
#                     survival_prob_growth = get_tribbles_survival_probability_growth(
#                                                       nb_paths=10000, 
#                                                       prob_choose_mountains=percentage_choose_mountains / 100.0, 
#                                                       prob_rain=percentage_rains / 100.0, 
#                                                       nb_children=nb_children, 
#                                                       init_population=init_population, 
#                                                       nb_generations=nb_generations,
#                                                       no_voids=True)
#                     new_line += survival_prob_growth
#                 except:
#                     print(new_line)
                file_contents.append(new_line)                
        write_to_file(file_path=file_path, file_content=file_contents)
    