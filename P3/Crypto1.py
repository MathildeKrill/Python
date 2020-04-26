import sys, gmpy2

MSGS = ("---  11 secret messages  ---", 'dhjded',  )

def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def random_(size=16):
    return open("/dev/urandom").read(size)

def encrypt(key, msg):
    c = strxor(key, msg)
    print msg, c
    print c.encode('hex')
    return c


if __name__ == '__main__':
    x = 1
    for po in range(11):
        x = (x * 32) % 19
        print x
#     n = 35
#     t = 1
#     p = 0
#     for p in range(n):
#         t = (2 * t) % n
#         p += 1
#         if t == 1:
#             print p
    
    n = 13
    for g in range(2, 13):
        result = [1, g]
        for pow_ in range(2, n-1):
            result.append((result[-1] * g) % n)
            if result[-1] == 1:
                break
        print g, len(result) == (n - 1), result
#     for a in range(19):
#         if (3 * a - 5) % 19 == 0:
#             print a
#     blocks = '20814804c1767293b99f1d9cab3bc3e7 ac1e37bfb15599e5f40eef805488281d'.split(' ')
#     IV_modif = strxor('Pay Bob 100$', 'Pay Bob 500$').encode("hex")
#     IV_modif +='0' * (len(blocks[0]) - len(IV_modif))
#     print IV_modif
#     print blocks[0], blocks[1]
#     print strxor(blocks[0].decode("hex"), IV_modif.decode("hex")).encode("hex"), blocks[1]
    
#     aes1 = '6f2584f0453f32f615c9afb7446b16f5'.decode("hex")
#     aes3 = '6f2584f0453f32f615c9afb7446b16f5'.decode("hex") 
#     10000000000000000000000000000000
#     aes4 = 'eeb42499241ad14af3de6aa96eacc48c'.decode("hex") 
#     20000000000000000000000000000000
#     y3__ = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'.decode("hex") 
#     print strxor(strxor(aes3, aes4), y3__).encode("hex")
#      
#     y1__ = '10000000000000000000000000000000'.encode("hex")
#     y2__ = '20000000000000000000000000000000'.encode("hex")
#     print strxor(aes1, y1__).encode("hex")
    
#     print 2
#     ciphertext = "09e1c5f70a65ac519458e7e53f36".decode("hex")
#     original = "attack at dawn"
#     print ciphertext, len(ciphertext), len(original), strxor(ciphertext, original), 'ok'
#     key = strxor(ciphertext, original)
#     print key
#     print strxor(key, "attack at dusk").encode('hex')
#     print ciphertext.encode('hex')
#     print strxor("                                ", "abcdefghijklmnopqrtsuvwxyz").encode('hex')
#     print ("abcdefghijklmnopqrtsuvwxyz").encode('hex')
#     
#     # is 
#     
#     key = random_(1024)
#     #print key
#     print 'ord("x")', ord("x"), "x".encode('hex'), 'ord("a")', ord("a"), "a".encode('hex'), ord("a") ^ ord("x"), '\n'
#     print ' '.join(format(ord(x), 'b') for x in ('a', 'x'))
#     ciphertexts = [encrypt(key, msg) for msg in MSGS]