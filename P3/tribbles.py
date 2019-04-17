'''
Created on 20 Mar 2019

@author: yuliavoevodskaya
'''

import random, math, codecs, os.path

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

def get_tribbles_survival_probability_growth(nb_paths, prob_choose_mountains, prob_rain, nb_children, init_population, nb_generations, no_voids):
    
    nb_extint = 0.
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
            population_growth_rate = math.log(population / (nb_children * init_population)) / nb_generations
            total_population_growth_log += population_growth_rate
            total_population_growth_log_sqr += population_growth_rate * population_growth_rate
    variance = (total_population_growth_log_sqr 
            - total_population_growth_log * total_population_growth_log / nb_paths) / (nb_paths - 1)
         
    return [1.0 - (nb_extint / nb_paths), 
            total_population_growth_log / nb_paths, 
            math.sqrt(max(variance, 0.0) / nb_paths), variance ]
 
def write_to_file(file_path, file_content, my_encoding='utf-8'):
    with codecs.open(file_path, 'w', encoding=my_encoding) as the_file:
        the_file.writelines(file_content)
    
def array_to_line(an_array, separator='|'):
    result = separator.join([str(x) for x in an_array]) + '\n'
    return result

if __name__ == '__main__':
    file_path = os.path.expanduser('~/Documents/Sites/wordpress-yu51a5/tribbles.numbers.txt')
    title_line = ['nb children', 'prob rain', 'prob to choose mountains', 
                                           'prob population survival', 'growth rate', 'growth rate std dev', 'growth rate var']
    file_contents = [array_to_line(title_line)]
    for nb_children in (2, 3, 5, 8):
        for percentage_rains in range(1, 5, 99):
            for percentage_choose_mountains in (1, 2, percentage_rains - 1, percentage_rains, percentage_rains + 1, 98, 99):
                new_line = [nb_children, percentage_rains / 100.0, percentage_choose_mountains / 100.0]
                try:
                    survival_prob_growth = get_tribbles_survival_probability_growth(
                                                      nb_paths=10000, 
                                                      prob_choose_mountains=percentage_choose_mountains / 100.0, 
                                                      prob_rain=percentage_rains / 100.0, 
                                                      nb_children=nb_children, 
                                                      init_population=4000, 
                                                      nb_generations=300,
                                                      no_voids=True)
                    new_line += survival_prob_growth
                except:
                    print(new_line)
                file_contents.append(array_to_line(new_line))                
        write_to_file(file_path=file_path, file_content=file_contents)
    