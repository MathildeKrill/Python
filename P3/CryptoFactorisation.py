'''
Created on 16 Sep 2015

@author: yuliavoevodskaya
'''
def large_power(base_, pow_):
    result = 1
    base_pow_2_pow = base_
    while pow_ > 0: 
        if pow_ % 2:
            result = (result * base_pow_2_pow) 
        pow_ = pow_ >> 1
        base_pow_2_pow = (base_pow_2_pow * base_pow_2_pow)
    return result

def large_power_mod(base_, pow_, mod_):
    result = 1
    base_pow_2_pow = base_ % mod_
    while pow_ > 0: 
        if pow_ % 2:
            result = (result * base_pow_2_pow) % mod_
        pow_ = pow_ >> 1
        base_pow_2_pow = (base_pow_2_pow * base_pow_2_pow) % mod_
    return result

def long_sqrt(inp_, guess, max_iter = 20):
    for _ in range(max_iter):
        diff = long(guess * guess - inp_) / long(2 * guess)
        if (diff * diff) <= 1:
            break
        guess -= diff
    while ((guess - 1) * (guess - 1) - inp_) >= 0:
        guess -= 1
    while (guess * guess - inp_) < 0:
        guess += 1
    assert ((guess - 1) * (guess - 1) - inp_) < 0 and (guess * guess - inp_) >= 0
    return guess
        
if __name__ == '__main__':
    
    N1 = 179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581
    root_N1 = long_sqrt(inp_ = N1, guess = long(1.43 * large_power(10, 154)))
    root_N11 = long_sqrt(inp_ = (root_N1 * root_N1 - N1), guess = (6 * large_power(10, 76)))
    p = root_N1 - root_N11
    q = root_N1 + root_N11
    assert 0 == N1 - p * q
    print 'p1 = ', p
    
    phi_N = (p - 1) * (q - 1) 
    e = 65537
    phi_N_mult = 1
    while ((phi_N_mult * phi_N + 1) % e):
        phi_N_mult += 1
    d = ((phi_N_mult * phi_N + 1) / e)
    CT = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540
    PT = large_power_mod(CT, d, N1)
    assert large_power_mod(PT, e, N1) == CT
    strPT = format(PT, 'x')
    ind_00 = strPT.find('00')
    msg_hex = strPT[ind_00+2 :] 
    print 'msg_hex', msg_hex.decode("hex")
    
    N3 = 720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929
    root_N3 = long_sqrt(inp_ = N3 * 24, guess = long(5 * large_power(10, 154)))
    sq3 = (root_N3 * root_N3 - (N3 * 24))
    root_N31 = long_sqrt(inp_ = (root_N3 * root_N3 - (N3 * 24)), guess = long(6 * large_power(10, 76))) 
    p3 = (root_N3 - root_N31) / 6
    q3 = (root_N3 + root_N31) / 4
    assert 0 == (N3) - p3 * q3
    print 'p3 = ', p3 
    
    N2 = 648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877
    root_N2 = long_sqrt(inp_ = N2, guess = long(8 * large_power(10, 153)))
    root_N2_init = root_N2
    while (root_N2 - root_N2_init) < 1024 * 1024 * 2:
        root_N21 = long_sqrt(inp_ = (root_N2 * root_N2 - N2), guess = (6 * large_power(10, 76)))
        if (root_N2 * root_N2 - root_N21 * root_N21 - N2) == 0:
            p2 = root_N2 - root_N21
            q2 = root_N2 + root_N21
            assert N2 - (p2 * q2) == 0
            print 'p2', p2
            break
        root_N2 += 1
        