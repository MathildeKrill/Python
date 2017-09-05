'''
Created on 7 Aug 2017

@author: yuliavoevodskaya
'''

from os import listdir
from os.path import isfile, expanduser
import codecs, shutil, os.path, string, re

def get_file_as_list(file_path):
    with codecs.open(file_path, encoding='utf-8') as file_opened:
        file_content_list = file_opened.readlines()
    return file_content_list

def remove_path(line):
    return line.replace("] http://www.yu51a5.com/wp-content/uploads/", "]")

allowed_chars=string.ascii_letters + string.digits+"_"
def replace_special_characters(line):
    if not("<h3>" in line):
        return line
    line = line.replace("<h3>", "")
    line = line.replace("</h3>", "")
    name_a = "".join([l for l in line])
    name_a = name_a.replace("í", "i")
    name_a = name_a.replace("á", "a")
    name_a = name_a.replace("é", "e")
    name_a = name_a.replace(" ", "_")
    name_a = name_a.replace("\n", "")
    name_a = "".join([l for l in name_a if l in allowed_chars])            
    line = "[yu_h a=\"" + name_a + "\"]" + line[:-1] + "[/yu_h]\n"
    return line

def modify_file_by_line(file_path, modif_func):
    file_content_list = get_file_as_list(file_path = file_path)
    
    for nb_line in range(len(file_content_list)):
        file_content_list[nb_line] = modif_func(line = file_content_list[nb_line])
            
    with codecs.open(file_path, 'w', encoding='utf-8') as the_file:
        the_file.writelines(file_content_list)
        
def get_filenames(dir_path):
    files_or_directories = [f_or_d for f_or_d in listdir(dir_path) if not f_or_d.startswith('.')]
    only_files = [f.lower() for f in files_or_directories if isfile(os.path.join(dir_path, f))]
    only_directories = [d.lower() for d in files_or_directories if os.path.isdir(os.path.join(dir_path, d))]
    return only_directories, only_files

def get_file_extension(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension

# recursively get all file extensions
def get_all_filenames(dir_path):
    directories, filenames = get_filenames(dir_path = dir_path)
    filename_array = [f for f in filenames]
    filename_array_with_dirs = [os.path.join(dir_path, f) for f in filenames]
    file_stats = [os.stat(f) for f in filename_array_with_dirs]
    for sub_dir_path in directories:
        sub_dir_path_full = os.path.join(dir_path, sub_dir_path)
        subfolder_all_filenames, subfolder_all_filenames_with_dirs, subfolder_file_stats = get_all_filenames(dir_path = sub_dir_path_full)
        filename_array += [f for f in subfolder_all_filenames]
        filename_array_with_dirs += [f for f in subfolder_all_filenames_with_dirs]
        file_stats += [f for f in subfolder_file_stats]
    return filename_array, filename_array_with_dirs, file_stats

# recursively get all file extensions
def get_all_extensions(dir_path):
    directories, filenames = get_filenames(dir_path = dir_path)
    all_extensions = set(get_file_extension(filename) for filename in filenames)
    for sub_dir_path in directories:
        subfolder_all_extensions = get_all_extensions(dir_path = os.path.join(dir_path,sub_dir_path))
        all_extensions.update(subfolder_all_extensions)
    return all_extensions

# recursively get all useful and redundant files
def get_all_redundant_files(dir_path):
    directories, filenames = get_filenames(dir_path = dir_path)
    
    filenames.sort(reverse=True)
    filenames_to_keep = []    
    filenames_to_delete = []
    filenames_extensions = []
    pattern = re.compile("^$")      
    for _filename in filenames:
        if ((len(filenames_to_keep) == 0) or (pattern.match(_filename) is None)):
            filename_to_keep, extension_to_keep = os.path.splitext(_filename)
            pattern = re.compile("^" + filename_to_keep + "-([0-9]+)x([0-9]+)." + extension_to_keep + "$")
            filenames_to_keep.append(_filename)
            filenames_extensions.append([filename_to_keep, extension_to_keep])
        else:
            filenames_to_delete.append(_filename)
    all_extensions = set(get_file_extension(filename) for filename in filenames)
    # print(("-([0-9]+)x([0-9]+)(" + all_extensions_regex + ")$"))
    pattern = re.compile("^(.+)-([0-9]+)x([0-9]+)(" + "|".join(all_extensions) + ")$")
    
    more_files_to_delete = []    
    for _filename in filenames_to_keep:
        if (not (pattern.match(_filename) is None)):
            dot_position = _filename.rfind('.')
            dash_position = _filename.rfind('-')
            parent_filename = _filename[:dash_position]+_filename[dot_position:]
            if (parent_filename in filenames_to_keep):
                more_files_to_delete.append(_filename)
            else:
                print(_filename)
    filenames_to_delete += more_files_to_delete

    for sub_dir_path in directories:
        subfolder_filenames_to_delete = get_all_redundant_files(dir_path = os.path.join(dir_path, sub_dir_path))
        filenames_to_delete += subfolder_filenames_to_delete
        
    return [os.path.join(dir_path, _filename) for _filename in filenames_to_delete]

def remove_path_before(key_word, path_to_clean):
    s = path_to_clean.find(key_word)
    return path_to_clean[s + len(key_word):]

if __name__ == '__main__':
       
    file_path = expanduser('~/Documents/Sites/wordpress-yu51a5/horsemen.txt')
    file_content_list = get_file_as_list(file_path = file_path)        
    file_content = "".join(file_content_list)
    
    dir_path = expanduser('~/Documents/Sites/Pages/uploads/')
#     filenames_to_delete = get_all_redundant_files(dir_path)
#     for e in filenames_to_delete:
#         os.remove(e)
#     print(len(filenames_to_delete))
    filename_array, filename_array_with_dirs, file_stats = get_all_filenames(dir_path = dir_path)
    filename_array_all = zip(filename_array, filename_array_with_dirs, file_stats)
    filename_array_all = [f for f in filename_array_all]
    print(type(filename_array_all))
    filename_array_all.sort(key = lambda f:f[0])
    look_for = []
    for i in range(len(filename_array_all) - 1):
        if (filename_array_all[i][0] == filename_array_all[i + 1][0]):
            for j in [i, i+1]:
                print(remove_path_before('uploads/', filename_array_all[j][1]))
                # print(filename_array_all[j][2])
            look_for +=[remove_path_before('uploads/', filename_array_all[j][1]) for j in [i, i+1]]
            
    for fn in look_for:
        str = "found " + fn
        if not(file_content.lower().find(fn) >= 0):
            str = "not " + str
            print (str)
            
        

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
