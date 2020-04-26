'''
Created on 6 Sep 2015

@author: yuliavoevodskaya
'''
import Crypto.Hash.SHA256
import os


if __name__ == '__main__':
    
    size_block = 1024
     
    for filename in ['6 - 1 - Introduction (11 min)-2', '6 - 2 - Generic birthday attack (16 min)']:
        full_filename =  (os.path.expanduser("~/Downloads/" + filename + ".mp4"))
        chunks = []
        with open(full_filename, "rb") as file_:
            while True:
                chunk = file_.read(size_block)
                if chunk:
                    chunks.append(chunk)
                else:
                    break
        
        current_hash = ''
        for chunk in chunks[::-1]:  
            to_hash = chunk + current_hash.decode('hex')
            sha256 = Crypto.Hash.SHA256.new(data = to_hash)
            current_hash = sha256.hexdigest()
            #print 'current_hash', current_hash
            
        print current_hash
        print current_hash == '03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8'
