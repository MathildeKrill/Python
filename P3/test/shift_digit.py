'''
Created on 30 Jul 2017

Find all numbers such that, when the number is written in base-adic format 
and the last digit is moved in front of the number, it increases factor-fold

@author: yuliavoevodskaya
'''

from decimal import Decimal
import decimal 
import sys
import os, cv2 #,  opencv


MAX_POWER = 100
MAX_ERROR = 1E-16

def _is_not_0(error):
    return (error > MAX_ERROR) or (error < (-MAX_ERROR))

def _print_int(name_of_i, i):
    print(name_of_i + ' = ' + ('{:' + str(MAX_POWER + 2) + '.0f}').format(i))

def find_a_b(base, factor, pow, errors):
    _base = Decimal(base)
    _factor = Decimal(factor)
    _a = Decimal(Decimal(pow - _factor)/Decimal(_base * _factor - Decimal(1)))
    a_error = _a - _a.quantize(Decimal(1.0)); # non-integer part
    if _is_not_0(error = a_error):
        print('ERROR WITH ' + _print_int('pow', pow) + _print_int('factor', factor) + _print_int('base', base))
    a = Decimal(0)
    b = Decimal(0)
    for _ in range(1, base):
        b += Decimal(1)
        a += _a
        ab = Decimal(a * _base + b)
        ba = Decimal(a + pow * b)
        error = Decimal(ba - _factor * ab)
        if a >= pow : # should never happen
            errors.append('ERROR overflow WITH ' + _print_int('a', a) + _print_int('b', b) + _print_int('pow', pow))
        if _is_not_0(error):  # should never happen
            errors.append('ERROR WITH ' + _print_int('a', a) + _print_int('b', b) + _print_int('ba - factor * ab', error))
        _print_int('a', a) 
        for k, v in {'b' : b, 'ab' : ab, 'ba' : ba}.items():
            _print_int(k, v)

if __name__ == '__main__':
    
    print(sys.version)
    print(sys.executable)
    print(cv2.__version__)
    
    print("all done")
