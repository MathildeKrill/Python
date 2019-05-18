'''
Created on 20 Mar 2019

@author: yuliavoevodskaya
'''

import math, codecs, os.path, numpy

ZeroLimit = numpy.nextafter(numpy.nextafter(0, 1), 1) # a "static" constant 
def isZero(x):
    return (x < ZeroLimit) and (x > (-ZeroLimit))
    
def get_tribbles_survival_probability_growth_CF(prob_choose_mountains, prob_rain, nb_children, nb_generations, thresholds_ES):
    
    # analytic formulae
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
        expected_log_growth = nb_generations * (math.log(nb_children) + prob_rain * math.log(prob_choose_mountains) \
                                                        + (1 - prob_rain) *  math.log(1 - prob_choose_mountains)) 
    
    result = [expected_nb_tribbles, expected_nb_tribbles_reduction, expected_variance, expected_variance_reduction, expected_log_growth]
    
    # from now to the end of the function - ES computation
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
        
        cum_prob_number_sunny_days = new_cum_prob_number_sunny_days
        cum_expected_shortfall_before_norm = new_cum_expected_shortfall_before_norm
        
    result += ES_values
    return result
                
def write_to_file(file_path, file_content, my_encoding='utf-8'):
    with codecs.open(file_path, 'w', encoding=my_encoding) as the_file:
        the_file.writelines([(','.join([str(x) for x in an_array]) + '\n') for an_array in file_content])

if __name__ == '__main__':
    file_path = os.path.expanduser('~/Documents/Sites/wordpress-yu51a5/tribbles.csv')
    nb_generations=100
    thresholds_ES=[0.001, 0.01, 0.05]
    title_line=['nb children', 'prob rain', 'prob mountains', 
                    'expected nb tribbles', 'expected nb tribbles reduction', 'expected variance', 'expected variance reduction',
                    'log growth'] + ['normalized ES @ ' + str((1 - tr) * 100) + '%' for tr in thresholds_ES]
    file_contents = [title_line]
    for nb_children in (2, 3, 5, 8):
        for percentage_rains in range(1, 10):
            # compile values_percentage_choose_mountains
            values_percentage_choose_mountains = [0, 0.1, 1, 2]
            if percentage_rains > 2:
                values_percentage_choose_mountains += [percentage_rains, percentage_rains + 1]
            if percentage_rains == 2:
                values_percentage_choose_mountains += [3]
            values_percentage_choose_mountains += [20, 49]
            
            #run
            for percentage_choose_mountains in values_percentage_choose_mountains:
                new_line = [nb_children, percentage_rains / 100.0, percentage_choose_mountains / 100.0]
                result = get_tribbles_survival_probability_growth_CF(
                                prob_choose_mountains=percentage_choose_mountains / 100.0, 
                                prob_rain=percentage_rains / 100.0, 
                                nb_children=nb_children, 
                                nb_generations=nb_generations, 
                                thresholds_ES=thresholds_ES)
                new_line += result
                file_contents.append(new_line)                
    write_to_file(file_path=file_path, file_content=file_contents)
    