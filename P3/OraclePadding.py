import urllib2, math

TARGET = 'http://crypto-class.appspot.com/po?er='

def get_2hex(number):
    _2hex = hex(number)[2:]
    if len(_2hex) == 1:
        _2hex = '0' + _2hex
    return _2hex
        
def xor_hex(str1, str2):
    assert len(str1) == len(str2)
    result = "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(str1.decode('hex') , str2.decode('hex') )]).encode('hex')
    return result 

def query(q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            assert e.code == 404 or e.code == 403
            if e.code == 404 or e.code == 200:
                return True # good padding
            return False # bad padding

if __name__ == "__main__":   
    ciphertext = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
    guessed_bytes = '090909090909090909'
    for byte_number in range(len(guessed_bytes)/2, 48):
        byte_position = byte_number % 16 + 1
        block_number = int(math.floor(byte_number / 16))
        print 'block_number', block_number
        fake_padding = get_2hex(byte_position) * byte_position
        print 'fake_padding', '0' * (len(ciphertext) - len(fake_padding) - 32) + fake_padding
        for byte_guess in range(257):
            if byte_guess == 256:
                raise Exception("out of bounds")
            false_pad =  xor_hex(fake_padding, get_2hex(byte_guess) + guessed_bytes[ : len(guessed_bytes) - block_number * 32])
            full_false_pad = '0' * (len(ciphertext) - len(false_pad) - (1 + block_number) * 32) + false_pad + '0' * 32
            tweaked_ciphertext = xor_hex(full_false_pad, ciphertext[ : len(ciphertext) - block_number * 32])    
            good_padding = query(tweaked_ciphertext)
            if good_padding:
                guessed_bytes = get_2hex(byte_guess) + guessed_bytes
                print 'guessed_bytes', guessed_bytes, guessed_bytes.decode('hex')
                break
    