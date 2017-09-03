'''
Created on 7 Aug 2017

@author: yuliavoevodskaya
'''

from os import listdir
from os.path import isfile, expanduser
import codecs, shutil, os.path, string, re

if __name__ == '__main__':
       
    doc_path = expanduser('~/Documents/Sites/wordpress-yu51a5/horsemen.txt')
    with codecs.open(doc_path, encoding='utf-8') as file_opened:
        file_content_list = file_opened.readlines()        
    file_content = "".join(file_content_list)

#     # how many images
#     print(file_content.count("[yu_image"))
#     print(file_content.count("[yu_caption"))
#     
#     # move used images
#     images_path = expanduser('~/Downloads/')
#     only_files = [f.lower() for f in listdir(images_path) if isfile(os.path.join(images_path, f))]
#     only_image_files = [f for f in only_files if (f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png'))]
# 
#     new_images_folder = expanduser('~/Desktop/Used wordpress files/')        
#     files_found = [filename for filename in only_image_files if "/" + filename + "[" in file_content]
#     for f in files_found:
#         print(f)
#         shutil.move(os.path.join(images_path, f), os.path.join(new_images_folder, f))
        
#     file_content = "".join(file_content_list) 
#     occurances = {}
#     for tag in ["sourcename=\"", "sourcehrf=\""]:
#         occurances_iter = re.finditer(tag+"[^\"]+\"", file_content)
#         occurances[tag] = [file_content[m.start()+len(tag): m.end()-1].lower() for m in occurances_iter if (m.start() > 0 and m.end() > 0)]
#         occurances[tag].sort()
#         for o in occurances[tag]:
#             print(o)
#         print(len(occurances[tag]))
        #input("Press Enter to continue...")
        
#     allowed_chars=string.ascii_letters + string.digits+"_"
    for nb_line in range(len(file_content_list)):
        line = file_content_list[nb_line]
        line = line.replace("] http://www.yu51a5.com/wp-content/uploads/", "]")
        file_content_list[nb_line] = line
#         if ("<h3>" in line):
#             line = line.replace("<h3>", "")
#             line = line.replace("</h3>", "")
#             name_a = "".join([l for l in line])
#             name_a = name_a.replace("í", "i")
#             name_a = name_a.replace("á", "a")
#             name_a = name_a.replace("é", "e")
#             name_a = name_a.replace(" ", "_")
#             name_a = name_a.replace("\n", "")
#             name_a = "".join([l for l in name_a if l in allowed_chars])            
#             line = "[yu_h a=\"" + name_a + "\"]"+line[:-1]+"[/yu_h]\n" 
#             file_content_list[nb_line] = line
#             
    with codecs.open(doc_path, 'w', encoding='utf-8') as the_file:
        the_file.writelines(file_content_list)
             
        
#     lines_with_17 = [line for line in file_content_list if (("\"#" in line))]
#     for line in lines_with_17:
#         print(line)
#         file_content = "".join(file_content_list).lower()          
#         files_not_found = [filename for filename in only_image_files if filename not in file_content]
     
#     
#     print(len(files_not_found))
#     
#     new_images_folder = expanduser('~/Desktop/Used wordpress files/')   
#     for f in files_not_found:
#         print(f)
#         shutil.move(os.path.join(images_path, f), os.path.join(new_images_folder, f))
#     