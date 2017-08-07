'''
Created on 7 Aug 2017

@author: yuliavoevodskaya
'''

from os import listdir
from os.path import isfile, expanduser
import codecs, shutil, os.path

if __name__ == '__main__':
    images_path = expanduser('~/Desktop/')
    only_files = [f.lower() for f in listdir(images_path) if isfile(os.path.join(images_path, f))]
    only_image_files = [f for f in only_files if (f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png'))]
       
    doc_path = expanduser('~/Documents/Sites/wordpress-yu51a5/horsemen.txt')
    with codecs.open(doc_path, encoding='utf-8') as file_opened:
        file_content_list = file_opened.readlines()
        file_content = "".join(file_content_list).lower()          
        files_not_found = [filename for filename in only_image_files if filename not in file_content]
    
    print(len(files_not_found))
    
    new_images_folder = expanduser('~/Desktop/Not used wordpress files/')   
    for f in files_not_found:
        print(f)
        shutil.move(os.path.join(images_path, f), os.path.join(new_images_folder, f))
    