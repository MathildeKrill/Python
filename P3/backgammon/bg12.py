'''
Created on 19 Jun 2018

@author: yuliavoevodskaya
'''

import random

def roll():
    return (random.randint(1, 6), random.randint(1, 6))

def bear_off(number_2, number_1):

if __name__ == '__main__':
    random.seed() # random numbers generator initialisation with a random seed
    roll()
    pass