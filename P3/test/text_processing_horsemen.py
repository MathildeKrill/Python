'''
Created on 7 Aug 2017

@author: yuliavoevodskaya
'''

from os import listdir
from os.path import isfile, expanduser
import codecs, shutil, os.path, string, re


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

def get_filenames(dir_path):
    files_or_directories = [f_or_d for f_or_d in listdir(dir_path) if not f_or_d.startswith('.')]
    only_files = [f.lower() for f in files_or_directories if isfile(os.path.join(dir_path, f))]
    only_directories = [d.lower() for d in files_or_directories if os.path.isdir(os.path.join(dir_path, d))]
    return only_directories, only_files

# recursively do something
def run_function_recursively(dir_path, recursive_func, **kwargs):
    directories, _ = get_filenames(dir_path = dir_path)
    recursive_func(dir_path = dir_path, **kwargs)
    for sub_dir_path in directories:
        recursive_func(dir_path = os.path.join(dir_path, sub_dir_path), **kwargs)

# do something on all files of a directory
def do_on_all_files(dir_path, file_func, **kwargs):
    _, filenames = get_filenames(dir_path = dir_path)
    for filename in filenames:
        file_func(file_path = os.path.join(dir_path, filename), **kwargs)  
        
# recursively do something
def run_function_recursively_on_files(dir_path, recursive_func_for_files, **kwargs):
    def recursive_func(dir_path, **kwargs):
        do_on_all_files(dir_path = dir_path, file_func = recursive_func_for_files, **kwargs)
        
    run_function_recursively(dir_path = dir_path, recursive_func = recursive_func, **kwargs)
    
# do something on all lines of a file
my_encoding = 'utf-8'
def do_on_all_lines(file_path, line_func, **kwargs):
    
    with codecs.open(file_path, encoding = my_encoding) as file_opened:
        file_content_list = file_opened.readlines()
    
    for nb_line in range(len(file_content_list)):
        result_per_line = line_func(line = file_content_list[nb_line], **kwargs)
        if result_per_line is not None:
            file_content_list[nb_line] = result_per_line
            
    with codecs.open(file_path, 'w', encoding = my_encoding) as the_file:
        the_file.writelines(file_content_list)
 
# recursively do something on all lines of all files of a directory
def run_function_recursively_on_lines(dir_path, recursive_func_for_lines, **kwargs):
    def recursive_func(file_path, **kwargs):
        do_on_all_lines(file_path = file_path, line_func = recursive_func_for_lines, **kwargs)
        
    run_function_recursively_on_files(dir_path = dir_path, recursive_func_for_files = recursive_func, **kwargs)    

def get_file_extension(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension

# get file info
def get_file_info(file_path, filename_array, filename_array_with_dirs, file_stats):
    filename_array += [os.path.basename(file_path)]
    filename_array_with_dirs += [file_path]
    file_stats += [os.stat(file_path)]

# recursively get all file extensions
def get_all_extensions(dir_path):
    def add_file_extensions(file_path, all_extensions):
        all_extensions.add(get_file_extension(filename = file_path))

    all_extensions = set()
    run_function_recursively_on_files(dir_path = dir_path, recursive_func_for_files = add_file_extensions, all_extensions = all_extensions)
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

def find_files_with_identicaln_names_in_different_folders(dir_path):
    filename_array = []; filename_array_with_dirs = []; file_stats = [];
    run_function_recursively_on_files(dir_path = dir_path, 
                                      recursive_func_for_files = get_file_info,
                                      filename_array = filename_array, 
                                      filename_array_with_dirs = filename_array_with_dirs, 
                                      file_stats = file_stats)

    filename_array_all = zip(filename_array, filename_array_with_dirs, file_stats)
    filename_array_all = [f for f in filename_array_all]    
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
            
def count_occurances(line, counts):
    for key in counts.keys():
        counts[key] += line.count(key)
        
def replace_substr(line, old_substr, new_substr):
    result = line.replace(old_substr, new_substr)
    return result

def print_if_found(line, substring):
    if substring in line:
        print(line)

if __name__ == '__main__':
       
    file_path = expanduser('~/Documents/Sites/wordpress-yu51a5/horsemen.txt')
    
#     dir_path = expanduser('~/Documents/Sites/Pages/uploads copy/')
#     exts = get_all_extensions(dir_path = dir_path)
#     for e in exts:
#         print(e)
#         
#     filename_array = []; filename_array_with_dirs = []; file_stats = [];
#     run_function_recursively_on_files(dir_path = dir_path, 
#                                       recursive_func_for_files = get_file_info,
#                                       filename_array = filename_array, 
#                                       filename_array_with_dirs = filename_array_with_dirs, 
#                                       file_stats = file_stats)
#     for s in file_stats:
#         print(s)
        
#     filenames_to_delete = get_all_redundant_files(dir_path)
#     for e in filenames_to_delete:
#         os.remove(e)
#     print(len(filenames_to_delete))

    dir_path = expanduser('~/Documents/Sites/wordpress-yu51a5/')
    # run_function_recursively_on_lines(dir_path = dir_path, recursive_func_for_lines = replace_substr, old_substr = "http://www.yu51a5.com/wp-content/uploads/durers-rhino1.jpg", new_substr = "durers-rhino1.jpg")
    run_function_recursively_on_lines(dir_path = dir_path, recursive_func_for_lines = print_if_found, substring = "??")
    print("done")
        
#     
#     # move used images
#     images_path = expanduser('~/Downloads/')
#     only_files = [f.lower() for f in listdir(images_path) if isfile(os.path.join(images_path, f))]
#     only_image_files = [f for f in only_files if (f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif'))]
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
