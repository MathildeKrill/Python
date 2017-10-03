'''
Created on 11 Sep 2017

@author: yuliavoevodskaya
'''
from os import listdir
from os.path import isfile, expanduser
import codecs, os.path, time

def get_filenames(dir_path, lower = True):
    files_or_directories = [f_or_d for f_or_d in listdir(dir_path) if not f_or_d.startswith('.')]
    only_files = [f for f in files_or_directories if isfile(os.path.join(dir_path, f))]
    only_directories = [d for d in files_or_directories if os.path.isdir(os.path.join(dir_path, d))]
    if (lower):
        only_files = [f.lower() for f in only_files]
        only_directories = [d.lower() for d in only_directories]       
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
one_line = 'one_line'
FILENAME = None

def get_FILENAME():
    return FILENAME
        
def do_on_all_lines(file_path, line_func, **kwargs):
    global FILENAME
    FILENAME = file_path
    with codecs.open(file_path, encoding = my_encoding) as file_opened:
        file_content_list = file_opened.readlines()
        
    if not('one_line' in kwargs):   
        for nb_line in range(len(file_content_list)):
            result_per_line = line_func(line = file_content_list[nb_line], **kwargs)
            if result_per_line is not None:
                file_content_list[nb_line] = result_per_line
        with codecs.open(file_path, 'w', encoding = my_encoding) as the_file:
            the_file.writelines(file_content_list)
    else:
        one_line = "".join(file_content_list)
        line_func(line = one_line, **kwargs)
    FILENAME = None
 
# recursively do something on all lines of all files of a directory
def run_function_recursively_on_lines(dir_path, recursive_func_for_lines, **kwargs):
    def recursive_func(file_path, **kwargs):
        do_on_all_lines(file_path = file_path, line_func = recursive_func_for_lines, **kwargs)
        
    run_function_recursively_on_files(dir_path = dir_path, recursive_func_for_files = recursive_func, **kwargs)

if __name__ == '__main__':
    pass