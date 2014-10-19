def binomialCoefficient(n, m):
    if (n-m) < m:
        return binomialCoefficient(n, n-m)
    result = 1.0
    for i in range(0, m): #0 inclusive, n+1 non inclusive
        result *= (n-i)
    for i in range(2, m+1): #m+1 inclusive, n+1 non inclusive
        result /= (i)
    return result

def probChooseQtyCardsGivenDenomination(qtyCardsDenomination, qtyCardsTotal, 
                                        qtySelectedDenomination, qtySelectedTotal): 
    return (binomialCoefficient(qtySelectedTotal, qtySelectedDenomination) 
           * binomialCoefficient(qtyCardsTotal - qtySelectedTotal, qtyCardsDenomination - qtySelectedDenomination)
           / binomialCoefficient(qtyCardsTotal, qtyCardsDenomination))

# we assume that deckDefinition starts with the biggest denomination
def findDistributionCards(deckDefinition, numberCardsToDraw):
    
    # initial value if howManyCardsRemain is the cards quantity
    totalNbCards = 0
    for _, cardsQuantity in deckDefinition:
        totalNbCards += cardsQuantity
    
    # while exploring the tree of possibilities, build an array (per level of tree)
    # which elements are, for each node at this level, 
    # 1. how many cards have already been drawn, 
    # 2. what is the sum of the points of these cards
    # 3. what is the probability to reach this node     
    nbDrawnCardsSoFar_sumValues_Probabilities = [[0, 0, 1.0]]
    for cardDenomination, qtyCardsDenomination in deckDefinition[:-1]: # -1 because we exclude the last element
        new_nbDrawnCardsSoFar_sumValues_Probabilities = []
        for nbDrawnCardsSoFar, sumValues, probability in nbDrawnCardsSoFar_sumValues_Probabilities:
            nbCardsRemainToDraw = numberCardsToDraw - nbDrawnCardsSoFar
            maxNbCanBeDrawn = min(qtyCardsDenomination, nbCardsRemainToDraw)
            for nbDrawnCardsOfThisDenomination in range(0, maxNbCanBeDrawn+1): # up to maxNbCanBeDrawn inclusive
                probToDrawThisNumberOfCards = probChooseQtyCardsGivenDenomination(
                                                    qtyCardsDenomination, totalNbCards, 
                                                    nbDrawnCardsOfThisDenomination, nbCardsRemainToDraw);
                new_nbDrawnCardsSoFar_sumValues_Probabilities.append([
                                                nbDrawnCardsSoFar + nbDrawnCardsOfThisDenomination, 
                                                sumValues + nbDrawnCardsOfThisDenomination * cardDenomination, 
                                                probability*probToDrawThisNumberOfCards]) 
        nbDrawnCardsSoFar_sumValues_Probabilities = new_nbDrawnCardsSoFar_sumValues_Probabilities
        totalNbCards -= qtyCardsDenomination
        
    # we rely on the fact that numberCardsToDraw < number of cards of the  last denomination
    resultDistribution = []
    last_denomination = deckDefinition[-1][0]
    for nbDrawnCardsSoFar, sumValues, probability in new_nbDrawnCardsSoFar_sumValues_Probabilities:        
        nbOfCardsOfTheLastDenomination = numberCardsToDraw - nbDrawnCardsSoFar
        resultDistribution.append([sumValues + last_denomination * nbOfCardsOfTheLastDenomination, probability])
           
    return resultDistribution    

if __name__ == '__main__':
    distribution = findDistributionCards(deckDefinition =  [[1, 4], [2, 4], [3, 4], [4, 4]], 
                                         numberCardsToDraw  = 2)
    cumulativeProbability = 0.0
    for sumValues, probability in distribution:
        if sumValues >= 8:
            cumulativeProbability += probability  
    
    print cumulativeProbability
    
    distribution = findDistributionCards(deckDefinition = [[1, 7], [2, 74], [3, 13], [4, 9]], 
                                         numberCardsToDraw  = 6)
    cumulativeProbability = 0.0
    for sumValues, probability in distribution:
        if sumValues >= 13:
            cumulativeProbability += probability
    print cumulativeProbability