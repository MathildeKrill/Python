# PROBLEM: you are given numbers 1, 2, 3, ..., N-1, N
# you can place +, - or nothing between these numbers 
# placing nothing means concatenation, e.g. ... + 13 14 - ... will mean ... + 1314 - ...
# find all combinations of (+, -, '') that will yield a given target (100)

import datetime

targetTotalGLOBAL = 100
combinationNumberGLOBAL = 0
combinationsEvaluatedGLOBAL = 0
    
def combinationNumber(flash = False):
    global combinationNumberGLOBAL, combinationsEvaluatedGLOBAL
    if flash:
        print "Combination quantity : " + str(combinationNumberGLOBAL)
        combinationNumberGLOBAL = 0
        print "Combinations evaluated : " + str(combinationsEvaluatedGLOBAL)
        combinationsEvaluatedGLOBAL = 0
    else:
        combinationNumberGLOBAL = combinationNumberGLOBAL + 1
        return 'Combination ' + str(combinationNumberGLOBAL)

def onesZerosToChars(oneOrZero):
    if (oneOrZero == -1):
        return '-'
    if (oneOrZero == 0):
        return ''
    if (oneOrZero == 1):
        return '+'
    raise ValueError(str(oneOrZero) + ' is out of range')    

def printEqualityAsString(onesZerosArray, result):
    numbers = range(1, len(onesZerosArray)+1)
    resultAsArray = [onesZerosToChars(onesZerosArray[i-1]) +str(i) for i in numbers]
    s = combinationNumber() + ' : '+''.join(resultAsArray) + '=' + str(result)
    #print  s

def evaluate(onesZerosArray):
    global combinationsEvaluatedGLOBAL
    combinationsEvaluatedGLOBAL = combinationsEvaluatedGLOBAL + 1
    numberSoFar = 1 # assume that the sign before 1 is " " or, equivalently, "+"
    totalSoFar = 0
    previousMultiplier = 1
    currentNumber = 1
    for oz in onesZerosArray:
        currentNumber = currentNumber + 1
        if (oz != -1) and (oz != 0) and (oz != 1):
            raise ValueError(str(oz) + ' is out of range')    
        if oz == 0:
            numberSoFar = numberSoFar * 10 + currentNumber
        else:
            totalSoFar = totalSoFar + previousMultiplier * numberSoFar
            previousMultiplier = oz
            numberSoFar = currentNumber
    # flush the last number
    totalSoFar = totalSoFar + previousMultiplier * numberSoFar
    return totalSoFar

def printIfTargetHit(onesZerosArray): # considering signs toggling to halve eval time
    total = evaluate(onesZerosArray)
    if total == targetTotalGLOBAL:
        printEqualityAsString( [0]+onesZerosArray, targetTotalGLOBAL)
    if ((-1) * total) == targetTotalGLOBAL: # toggling the signs
        printEqualityAsString([-1] + [-1*oz for oz in onesZerosArray], targetTotalGLOBAL)

def embeddedLoopsFixed():
    possibleSigns = [-1,0,1]
    signs = [None for _ in range(15)]
    for s1 in possibleSigns:
        signs[0] = s1 
        for s2 in possibleSigns:
            signs[1] = s2 
            for s3 in possibleSigns:
                signs[2] = s3 
                for s4 in possibleSigns:
                    signs[3] = s4 
                    for s5 in possibleSigns:
                        signs[4] = s5 
                        for s6 in possibleSigns:
                            signs[5] = s6 
                            for s7 in possibleSigns:
                                signs[6] = s7 
                                for s8 in possibleSigns:
                                    signs[7] = s8 
                                    for s9 in possibleSigns:
                                        signs[8] = s9 
                                        for s10 in possibleSigns:
                                            signs[9] = s10 
                                            for s11 in possibleSigns:
                                                signs[10] = s11 
                                                for s12 in possibleSigns:
                                                    signs[11] = s12 
                                                    for s13 in possibleSigns:
                                                        signs[12] = s13 
                                                        for s14 in possibleSigns:
                                                            signs[13] = s14 
                                                            for s15 in possibleSigns:
                                                                signs[14] = s15 
                                                                printIfTargetHit(signs)
                                    
def triadicIteraction(signsQty):
    signs = [None for _ in range(signsQty)]
    comb = int(3**signsQty-1)
    while (comb >= 0):
        combCopy = comb
        for n in range(signsQty):
            signs[n] = 1-combCopy%3 # [0,1,2] -> [1,0,-1], correct range for signs
            combCopy = combCopy//3
        printIfTargetHit(signs)
        comb = comb - 1
        
def recursiveIteration(signsQty):
    def recursiveIterationInner(signs, newSign, currentOrder):
        if (currentOrder >= 0):
            signs[currentOrder] = newSign
        if currentOrder == (len(signs) - 1):
            printIfTargetHit(signs)
        else:
            recursiveIterationInner(signs,-1, currentOrder+1)
            recursiveIterationInner(signs, 0, currentOrder+1)
            recursiveIterationInner(signs, 1, currentOrder+1)
    recursiveIterationInner(signs = [None for _ in range(signsQty)], newSign = None, currentOrder = -1)
    
def runCombinationCheckingMethod(fun, args, kwargs = {}):    
    nowGlobal = datetime.datetime.now()
    fun(*args, **kwargs)
    print 'Method name: ' + str(fun)
    combinationNumber(flash = True)
    timeSpan = datetime.datetime.now() - nowGlobal
    print "Time elapsed : " + str(timeSpan)
            
if __name__ == '__main__':
    runCombinationCheckingMethod(embeddedLoopsFixed, (), {})
    runCombinationCheckingMethod(recursiveIteration, [], {'signsQty' : 15})
    runCombinationCheckingMethod(triadicIteraction, [], {'signsQty' : 15})
    
    # OUTPUT (my machine is quite weak)
#     Method name: <function embeddedLoopsFixed at 0x01DE3C70>
#     Combination quantity : 16560
#     Time elapsed : 0:01:27.489000
#     Method name: <function recursiveIteration at 0x01DE3D70>
#     Combination quantity : 16560
#     Time elapsed : 0:01:40.458000
#     Method name: <function triadicIteraction at 0x01DE3CB0>
#     Combination quantity : 16560
#     Time elapsed : 0:03:08.165000
    