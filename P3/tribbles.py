'''
Created on 20 Mar 2019

@author: yuliavoevodskaya
'''

import random, math, codecs, os.path

def tribbles_one_path(prob_choose_mountains, prob_rain, nb_children, init_population, nb_generations):
    
    population = init_population
    
    for _ in range(nb_generations):
        weather = random.random()
        population_mountains = round(population * prob_choose_mountains)
        if weather > prob_rain: 
            population = (population - population_mountains) * nb_children
        else: 
            population = population_mountains * nb_children
        # print(population)
    return population

def get_tribbles_survival_probability_growth(nb_paths, prob_choose_mountains, prob_rain, nb_children, init_population, nb_generations):
    
    nb_extint = 0.
    total_population_growth_log = 0.0
    total_population_growth_log_sqr = 0.0
    
    for _ in range(nb_paths):
        population = tribbles_one_path(prob_choose_mountains = prob_choose_mountains, 
                                       prob_rain = prob_rain, 
                                       nb_children = nb_children, 
                                       init_population = init_population, 
                                       nb_generations = nb_generations)
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
 
def write_to_file(file_path, file_content, my_encoding = 'utf-8'):
    with codecs.open(file_path, 'w', encoding = my_encoding) as the_file:
        the_file.writelines(file_content)
           
def append_to_file(file_path, new_lines, my_encoding = 'utf-8'):
    with codecs.open(file_path, encoding = my_encoding) as file_opened:
        file_content_list = file_opened.readlines()
    write_to_file(file_path, file_content_list + new_lines, my_encoding = my_encoding)
    
def array_to_line(an_array, separator = '|'):
    result = '|'.join([str(x) for x in an_array]) + '\n'
    return result

if __name__ == '__main__':
    file_path = os.path.expanduser('~/Documents/Sites/wordpress-yu51a5/tribbles.txt')
    title_line = ['prob choose mountains', 'prob rain', 'nb children',
                                           'prob population survival', 'growth rate', 'growth rate std dev', 'growth rate var']
    file_contents = [array_to_line(title_line)]
    for percentage_choose_mountains in range(0, 101):
        for percentage_rains in range(0, 101):
            for nb_children in (2, 3, 5, 8):
                new_line = [percentage_choose_mountains / 100.0, percentage_rains / 100.0, nb_children]
                try:
                    survival_prob_growth = get_tribbles_survival_probability_growth(
                                                      nb_paths = 10000, 
                                                      prob_choose_mountains = percentage_choose_mountains / 100.0, 
                                                      prob_rain = percentage_rains / 100.0, 
                                                      nb_children = nb_children, 
                                                      init_population = 4000, 
                                                      nb_generations = 300)
                    new_line += survival_prob_growth
                except:
                    print(new_line)
                file_contents.append(array_to_line(new_line))
                
    write_to_file(file_path = file_path, file_content = file_contents)