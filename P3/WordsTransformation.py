import enchant
from functools import total_ordering
from string import ascii_lowercase
from operator import pos
dictEng = enchant.Dict("en_US")
ascii_lowercase_reversed = [ascii_lowercase[i] for i in range(len(ascii_lowercase)-1, -1, -1)]

@total_ordering
class WordWithPath:
    def __init__(self, newWord, ancestor = None):
        self.word = newWord
        if ancestor == None:
            self.path = []
        else:
            self.path = [ancestor.word] + ancestor.path
    def __eq__(self, other):
        if (other == None):
            return False
        return (self.word == other.word)
    def __lt__(self, other):
        return (self.word < other.word)
    def reversePath(self):
        return [self.path[i] for i in range(len(self.path)-1, -1, -1)]                        

#find all words that are 1 letter different            
def findNextWords(wordWithPath):
    w = wordWithPath.word
    result = []
    # all words before w
    for pos in range(len(w)):
        originalLetter = w[pos]
        for c in ascii_lowercase:
            w = w[:pos] + c + w[pos+1:] 
            if c == originalLetter:
                break
            if dictEng.check(w):
                result.append(WordWithPath(w, wordWithPath))
    
    for pos in range(len(w)-1, -1, -1):
        originalLetter = w[pos]
        for c in ascii_lowercase:
            if c <= originalLetter:
                continue
            w = w[:pos] + c + w[pos+1:] 
            if dictEng.check(w):
                result.append(WordWithPath(w, wordWithPath))
        w = w[:pos] + originalLetter + w[pos+1:]
   
    return result         
        

def mergeSortedLists(list1, list2):
    i1 = 0; i2 = 0
    result = []
    while (True):
        if (i1 < len(list1)) and (i2 < len(list2)):
            if (list1[i1] < list2[i2]):
                result.append(list1[i1]); i1 = i1+1
            else: 
                result.append(list2[i2]); i2 = i2+1
        elif (i1 < len(list1)):
            result.append(list1[i1]); i1 = i1+1
        elif (i2 < len(list2)):
            result.append(list2[i2]); i2 = i2+1
        else:
            return result
        
def mergeManySortedLists(allLists):
    if len(allLists) == 1:
        return allLists[0]
    i = 0
    newAllLists = []
    while (2*i) < len(allLists):
        if (2*i+1) < len(allLists):
            newAllLists.append(mergeSortedLists(allLists[2*i], allLists[2*i+1])) 
        else:
            newAllLists.append(allLists[2*i])
        i = i+1
    allLists = [] # clear memory
    return mergeManySortedLists(allLists = newAllLists)

def findOverlaps(list1, list2):
    result = []
    i1 = 0; i2 = 0
    while (i1 < len(list1)) and (i2 < len(list2)):
        if (list1[i1] == list2[i2]):
            result.append((list1[i1], list2[i2]))
            i1 = i1+1; i2 = i2+1
        elif (list1[i1] < list2[i2]):
            i1 = i1+1
        else:
            i2 = i2+1
    return result

def removeOverlaps(listToClean, listReference):
    i1 = 0; i2 = 0
    while (i1 < len(listToClean)) and (i2 < len(listReference)):
        if (listToClean[i1] == listReference[i2]):
            del listToClean[i1]
            i2 = i2+1
        elif (listToClean[i1] < listReference[i2]):
            i1 = i1+1
        else:
            i2 = i2+1    

def searchInSortedList(sortedList, searchee):
    lowerBound = 0
    upperBound = len(sortedList)-1
    while (lowerBound < upperBound):
        mid = int(round((lowerBound+upperBound)/2))
        if (sortedList[mid] == searchee):
            return mid
        if (sortedList[mid] < searchee):
            lowerBound = mid+1
        else:
            upperBound = mid-1 
        if (lowerBound == upperBound):
            if (sortedList[lowerBound] == searchee):
                return lowerBound        
    return None

def findChain(leftWord, rightWord):
    leftSet = [WordWithPath(leftWord)]; leftEdge = [WordWithPath(leftWord)]
    rightSet = [WordWithPath(rightWord)]; rightEdge = [WordWithPath(rightWord)]     
    for j in range(10):
        newLeftEdge = mergeManySortedLists([findNextWords(w) for w in leftEdge])
        leftSet = mergeSortedLists(leftEdge, leftSet)
        removeOverlaps(listToClean = newLeftEdge, listReference = leftSet)
        leftEdge = newLeftEdge
        
        print [n.word for n in newLeftEdge]
        
        overlaps = findOverlaps(leftEdge, rightEdge)
        if len(overlaps)>0:
            return overlaps
        newRightEdge = mergeManySortedLists([findNextWords(w) for w in rightEdge])
        rightSet = mergeSortedLists(rightEdge, rightSet)
        removeOverlaps(listToClean = newRightEdge, listReference = rightSet)
        rightEdge = newRightEdge
        
        print [n.word for n in newRightEdge]
         
        overlaps = findOverlaps(leftEdge, rightEdge)
        if len(overlaps)>0:
            return overlaps      
       
    return []


if __name__ == '__main__':
    halfChains = findChain("man", "air")
    for h1, h2 in halfChains:
        c = h1.reversePath() + [h1.word] + h2.path
        print c
    