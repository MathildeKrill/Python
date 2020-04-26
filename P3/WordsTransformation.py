#import enchant
from functools import total_ordering
from string import ascii_lowercase

@total_ordering
class WordWithPath:
    dictEng = enchant.Dict("en_US")
    
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
    
    #for the result outputting
    def concatenatePath(self, rhs):
        result = [self.path[i] for i in range(len(self.path)-1, -1, -1)] + [self.word] + rhs.path
        return result
    
    @staticmethod
    def checkWord(w):
        return WordWithPath.dictEng.check(w)
    
    #find all words that are 1 letter different            
    def findNextWords(self):
        w = self.word #a shortcut
        result = []
        # all words before w
        for pos in range(len(w)):
            originalLetter = w[pos]
            for c in ascii_lowercase:
                w = w[:pos] + c + w[pos+1:] 
                if c == originalLetter:
                    break
                if WordWithPath.dictEng.check(w):
                    result.append(WordWithPath(w, self))
        
        for pos in range(len(w)-1, -1, -1):
            originalLetter = w[pos]
            for c in ascii_lowercase:
                if c <= originalLetter:
                    continue
                w = w[:pos] + c + w[pos+1:] 
                if WordWithPath.dictEng.check(w):
                    result.append(WordWithPath(w, self))
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
                result.append(list2[i2])
                if (list1[i1] == list2[i2]): # avoid duplicates
                    i1 = i1+1
                i2 = i2+1
            continue
        elif (i1 < len(list1)):
            result += list1[i1:]
        elif (i2 < len(list2)):
            result += list2[i2:]
        return result
        
def mergeManySortedLists(allLists):
    if len(allLists) == 0:
        return []
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
    allLists = []# clear memory
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

def findChain(leftWord, rightWord, maxTreeDepth):
    errors = ''
    if len(leftWord) != len(rightWord):
        errors = ("Lengths of the left word, '" + leftWord 
                         + "', and the right word, '" + rightWord + "' do not match. ")
    if not WordWithPath.checkWord(leftWord):
        errors += "Left word, '" + leftWord + "', is not in the dictionary. "
    if not WordWithPath.checkWord(rightWord):
        errors += "Right word, '" + rightWord + "', is not in the dictionary. "
    if errors != '':
        raise ValueError(errors)
    if (leftWord == rightWord):
        return [WordWithPath(leftWord), WordWithPath(rightWord)]
    
    leftAllNodes = [WordWithPath(leftWord)]; leftLeaves = [WordWithPath(leftWord)]
    rightAllNodes = [WordWithPath(rightWord)]; rightLeaves = [WordWithPath(rightWord)]     
    for _ in range(maxTreeDepth):
        newLeftLeaves = mergeManySortedLists([w.findNextWords() for w in leftLeaves])
        leftAllNodes = mergeSortedLists(leftLeaves, leftAllNodes)
        removeOverlaps(listToClean = newLeftLeaves, listReference = leftAllNodes)
        leftLeaves = newLeftLeaves        
        overlaps = findOverlaps(leftLeaves, rightLeaves)
        if len(overlaps)>0:
            break
        
        newRightLeaves = mergeManySortedLists([w.findNextWords() for w in rightLeaves])
        rightAllNodes = mergeSortedLists(rightLeaves, rightAllNodes)
        removeOverlaps(listToClean = newRightLeaves, listReference = rightAllNodes)
        rightLeaves = newRightLeaves        
        overlaps = findOverlaps(leftLeaves, rightLeaves)
        if len(overlaps)>0:
            break      
       
    return [h1.concatenatePath(h2) for h1, h2 in overlaps] 


if __name__ == '__main__':
    allPaths = findChain("rough", "poach", 10)
    for p in allPaths:
        print p
    allPaths = findChain("man", "spa", 10)
    for p in allPaths:
        print p
    allPaths = findChain("tree", "fled", 10)
    for p in allPaths:
        print p
    allPaths = findChain("ree", "fled", 10)
    for p in allPaths:
        print p
    allPaths = findChain("zree", "fled", 10)
    for p in allPaths:
        print p
    