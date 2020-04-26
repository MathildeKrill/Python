from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter
import inspect
import os 

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

class AESCipher:
    def __init__( self, key, mode ):
        """
        Requires hex encoded param as a key
        """
        assert(mode == AES.MODE_CBC or mode == AES.MODE_CTR) # others not tried
        self.key = key.decode("hex")
        self.mode = mode

    def encrypt( self, raw ):
        """
        Returns hex encoded encrypted value!
        """
        raw = pad(raw)
        iv = Random.new().read(AES.block_size);
        cipher = self.get_cipher(iv = iv)
        return ( iv + cipher.encrypt( raw ) ).encode("hex")
    
    def get_cipher(self, iv):
        if self.mode == AES.MODE_CTR:
            self.counter = Counter.new(128, initial_value=long(iv.encode("hex"), 16))
            cipher = AES.new(self.key, self.mode, iv, counter = self.counter)
        else:
            cipher = AES.new(self.key, self.mode, iv)
        return cipher

    def decrypt( self, enc ):
        """
        Requires hex encoded param to decrypt
        """
        enc = enc.decode("hex")
        iv = enc[:16]
        enc= enc[16:]
        cipher = self.get_cipher(iv = iv)
        result = cipher.decrypt( enc)
        if self.mode == AES.MODE_CBC:
            result = unpad(result)
        return result

if __name__== "__main__":

    this_file_name = os.path.abspath(inspect.getfile(inspect.currentframe())) 
    with open(this_file_name, 'r') as content_file:
        content = content_file.read()
        
    key_CBC = os.urandom(16).encode('hex')
    cipher_CBC = AESCipher(mode = AES.MODE_CBC, key = key_CBC)
    enc_CBC = cipher_CBC.encrypt(raw = content)    
    print 'enc_CBC\n\n', enc_CBC
    
    key_CTR = os.urandom(16).encode('hex')
    cipher_CTR = AESCipher(mode = AES.MODE_CTR, key = key_CTR)
    enc_CTR = cipher_CTR.encrypt(raw = enc_CBC)
    print '\nenc_CTR\n\n', enc_CTR
    
    dec_CTR = cipher_CTR.decrypt(enc = enc_CTR)
    print '\ndec_CTR\n\n', dec_CTR
    
    dec_CBC = cipher_CBC.decrypt(enc = enc_CBC)
    print '\ndec_CBC\n\n', dec_CBC