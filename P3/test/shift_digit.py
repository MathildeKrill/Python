'''
Created on 30 Jul 2017

Find all numbers such that, when the number is written in base-adic format 
and the last digit is moved in front of the number, it increases factor-fold

@author: yuliavoevodskaya
'''

from decimal import Decimal
import decimal 

MAX_POWER = 100
MAX_ERROR = 1E-16

def _print_float(name_of_f, f):
    return name_of_f + ' = ' + ('{:' +str(MAX_POWER + 2) + '.8f}').format(f)

def _print_int(name_of_i, i):
    return name_of_i + ' = ' + ('{:' +str(MAX_POWER + 2) + '.0f}').format(i)

def find_a_b(base, factor, pow):
    _a = Decimal(Decimal(pow - factor)/Decimal(base * factor - Decimal(1)))
    a = Decimal(0)
    b = Decimal(0)
    for _ in range(1, base):
        b += Decimal(1)
        a += _a
        ab = Decimal(a * base + b)
        ba = Decimal(a + pow * b)
        error = Decimal(ba - factor * ab)
        if a >= pow : # should never happen
            print 'ERROR overflow WITH ' + _print_float('a', a) + _print_int('b', b) + _print_int('pow', pow)
        if error * error > (MAX_ERROR * MAX_ERROR):  # should never happen
            print 'ERROR WITH ' + _print_float('a', a) + _print_int('b', b) + _print_float('ba - factor * ab', error)
#         print _print_float('a', a) 
#         for k, v in {'b' : b, 'ab' : ab, 'ba' : ba}.items():
#             print  _print_int(k, v)

if __name__ == '__main__':
    base = Decimal(10)
    factor = Decimal(2)
    
    pow = Decimal(1)
    decimal.getcontext().prec = MAX_POWER + 2
    res_so_far = 1
    for i in range(MAX_POWER):
        if res_so_far == factor:
            print 'POWER = ' + str(i)
            find_a_b(base = base, factor = factor, pow = pow)
        res_so_far = (res_so_far * base) % (base * factor -1)
        pow *= base
    
