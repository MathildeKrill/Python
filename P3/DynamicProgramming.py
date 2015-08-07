def GetFootballProbabilities(probabiliryFirstTeamWinsOneGame, numberWins):
    probabilities = [[-1 for _ in range(numberWins+1)] for _ in range(numberWins+1)]
    for smallIndex in range(numberWins-1, -1, -1):
        probabilities[numberWins][smallIndex] = 1.0
        probabilities[smallIndex][numberWins] = 0.0  
    for bigIndex in range(numberWins-1, -1, -1):
        probabilities[bigIndex][bigIndex] = (probabiliryFirstTeamWinsOneGame * probabilities[bigIndex+1][bigIndex]
            + (1.0-probabiliryFirstTeamWinsOneGame) * probabilities[bigIndex][bigIndex+1])
        for smallIndex in range(bigIndex-1, -1, -1):
            print smallIndex, bigIndex
            probabilities[smallIndex][bigIndex] = (probabiliryFirstTeamWinsOneGame * probabilities[smallIndex+1][bigIndex]
                + (1.0-probabiliryFirstTeamWinsOneGame) * probabilities[smallIndex][bigIndex+1])                        
            probabilities[bigIndex][smallIndex] = (probabiliryFirstTeamWinsOneGame * probabilities[bigIndex+1][smallIndex]
                + (1.0-probabiliryFirstTeamWinsOneGame) * probabilities[bigIndex][smallIndex+1])
            
    return probabilities

if __name__ == '__main__':
    probabilities = GetFootballProbabilities(probabiliryFirstTeamWinsOneGame = 0.5, numberWins = 10)
    print '{r|' + '|'.join('l' for _ in range(11)) + '} \hline'
    print '&' + '&'.join(str(r) + 'W' for r in range(11)) + '\\\\ \hline'
    i=0
    for row in probabilities:
        print str(i) + 'W&' + '&'.join(("%.3f" % r) for r in row) + '\\\\ \hline'
        i=i+1