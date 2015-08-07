
def _find_longest_subsequence(seq_short, seq_long):
    resultSoFar = [[] for _ in seq_short]
    index_long_seq = -1
    for elem_long_seq in seq_long:
        index_long_seq += 1
        #top element - separate treatment
        previous_element = resultSoFar[0]
        if seq_short[0] == elem_long_seq:
            resultSoFar[0] = [(0, index_long_seq, elem_long_seq)]
        # else: propagate previous result
        for index_short_seq in xrange(1, len(seq_short)):
            previous_element_cached = resultSoFar[index_short_seq]
            if seq_short[index_short_seq] == elem_long_seq:
                resultSoFar[index_short_seq] = previous_element + [(index_short_seq, index_long_seq, elem_long_seq)]
            elif len(resultSoFar[index_short_seq]) < len(resultSoFar[index_short_seq-1]):
                resultSoFar[index_short_seq] = resultSoFar[index_short_seq-1]
            previous_element = previous_element_cached
    return resultSoFar

def find_longest_subsequence(seq_1, seq_2):
    if (not seq_1) or (not seq_2):
        return []
    if len(seq_1) <= len(seq_2):
        candidates = _find_longest_subsequence(seq_short = seq_1, seq_long = seq_2)
    else:
        candidates = _find_longest_subsequence(seq_short = seq_2, seq_long = seq_1)  
    result = candidates[0]
    for candidate in candidates:
        if len(candidate) > len(result):
            result = candidate
    print "Longest subsequence of '", seq_1, "' and '" + seq_2 + "' is "+ ''.join(r[2] for r in result)
    return result

if __name__ == '__main__':
    find_longest_subsequence('0s', '0ss0')
    find_longest_subsequence('0', '0')
    find_longest_subsequence('0', '00')
    find_longest_subsequence('0000', '0000')
    sseq2 = find_longest_subsequence("testing123testing", "thisisatest")
    assert(''.join(e[2] for e in sseq2) == "tsitest")