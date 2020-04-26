'''
Created on 1 Jun 2017

@author: yuliavoevodskaya
'''
from math import sqrt

GR = 0.5 * (sqrt(5.0) - 1.0);

def find_gr_centre():
    x1 = 0.0
    y1 = 0.0
    x2 = 1.0 + GR
    y2 = 1.0
    for _ in range(100):
        dx = x2 - x1
        dy = y2 - y1
        x1 += dx / (1.0 + GR)
        y1 += dy * GR
        x2 -= dx * GR * GR /(1.0 + GR)
        y2 -= dy * GR * GR * GR
    print x1, x2, y1, y2
    print (x1 * GR) / y1 - 1
    print ((3.0 * GR + 4.0) / 5.0) / x1 - 1.0
    print 1.0 + GR
    r1 = (sqrt(x1 * x1 + (1.0 - y1) * (1.0 - y1)))
    r2 = (sqrt(y1 * y1 + (1.0 - x1) * (1.0 - x1)))
    r3 = (sqrt((x1 - 1.0 - GR) * (x1 - 1.0 - GR) + (GR - y1) * (GR - y1)))
    print r1, r2, r3, (r1/r2)/(1.0 + GR) - 1.0, (r2/r3)/(1.0 + GR) - 1.0
    print r1 * r1 + r2 * r2 - 2.0
    print (r3 * r3 + r2 * r2) / (GR * GR) - 2.0 
        
if __name__ == '__main__':
    find_gr_centre()
    print 'done'