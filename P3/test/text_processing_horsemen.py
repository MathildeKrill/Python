'''
Created on 7 Aug 2017

@author: yuliavoevodskaya
'''

from os import listdir
from os.path import isfile, expanduser
import codecs, shutil, os.path, string, re, collections
from text_processing_bulk import run_function_recursively_on_lines, get_filenames, do_on_all_lines, get_FILENAME


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
    _, filenames = get_filenames(dir_path = dir_path)
    
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
    maybe_delete = [] 
    for _filename in filenames_to_keep:
        if (not (pattern.match(_filename) is None)):
            dot_position = _filename.rfind('.')
            dash_position = _filename.rfind('-')
            parent_filename = _filename[:dash_position]+_filename[dot_position:]
            if (parent_filename in filenames_to_keep):
                more_files_to_delete.append(_filename)
            else:
                maybe_delete.append(_filename)
    filenames_to_delete += more_files_to_delete
        
    return [os.path.join(dir_path, _filename) for _filename in filenames_to_delete], \
            [os.path.join(dir_path, _filename) for _filename in maybe_delete]

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
    if substring.lower() in line.lower():
        print(line)
        print("Found " + substring.lower() + " " + str(line.lower().count(substring.lower())) + " time(s)")

def find_special_filenames(dir_path_wp, dir_path_uploads):
    _, filenames = get_filenames(dir_path = dir_path_uploads)
    fn_chars = {" "}
    for f in filenames:
        for c in f:
            fn_chars.add(c)
    print(fn_chars)        
    all_c=[]
    for fn_char in fn_chars:
        all_c += [fn_char]
    all_c.sort()
    print(all_c)   
    
    special_filenames = [f for f in filenames if any([c in f for c in ['´', '̀', '́', '̈', 'а', 'в', 'е', 'и', 'к', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'я']])]
    for sf in special_filenames:
        run_function_recursively_on_lines(dir_path = dir_path_wp, recursive_func_for_lines = print_if_found, substring = sf)
    print(special_filenames)
    
def return_all_matches(line, pattern, result, one_line = None):       
    _result = re.findall(pattern, line, flags=0)
    for _r in _result:
        result.append(_r)
        
pattern_images = "(\[(yu_image|yu_caption)([^\[]+)\]([^\[]+)\[/(yu_image|yu_caption)\])"
param_names = ["caption", "id", "src", 'sourcename', 'sourcehrf', "folder_name"]
def return_all_images(line, result, one_line = None):       
    _result = []
    return_all_matches(result = _result, line = line, pattern = pattern_images, one_line = one_line)
    for _r in range(len(_result)):
        _detailed_result = {}
        _detailed_result['all'] = _result[_r][0]
        _detailed_result['params'] = _result[_r][2]
        _detailed_result['params_replaced'] = _result[_r][2]
        _detailed_result['filename'] = _result[_r][3].strip()
        for param_name in param_names:
            param_pattern = "(" + param_name + '\s*=\s*\"([^"]*)\")';
            _result_param = re.search(param_pattern, _result[_r][2], flags=0)
            if _result_param is not None:
                _detailed_result[param_name] = _result_param[2].strip()
                _detailed_result['params_replaced'] = _detailed_result['params_replaced'].replace(_result_param[0], '')
            else:
                _detailed_result[param_name] = None
        _detailed_result['page_name'] = os.path.basename(get_FILENAME())[:-4]
        if _detailed_result['folder_name'] is None:
            _detailed_result['folder_name'] = _detailed_result['page_name']
        result.append(_detailed_result)
            
        
def sort_count_occurances(a_list):
    result_dict = {}
    for _r in a_list:
        if _r in result_dict:
            result_dict[_r] += 1
        else:
            result_dict[_r] = 1
    result_dict = [[key, value] for key, value in result_dict.items()]

    result_dict.sort(key = lambda x:x[0])
    for r in result_dict:
        print(r)
        
    return result_dict


if __name__ == '__main__':
       
    file_path = expanduser('~/Documents/Sites/wordpress-yu51a5/horsemen.txt')
    dir_path_wp = expanduser('~/Documents/Sites/wordpress-yu51a5/')
    dir_path_uploads = expanduser('~/Documents/Sites/Pages/uploads/')
    dir_path_uploads5 = expanduser('~/Documents/Sites/Pages/uploads 5/')
    
#     _, filenames = get_filenames(dir_path = dir_path_uploads5)
#     _cover = [nu for nu in filenames if ("_cover." in nu)]
#     print("_cover: " + str(len(_cover)))
#     for b in _cover:
#         print(b)
    
#     filenames_to_delete, maybe_delete = get_all_redundant_files(dir_path = dir_path_uploads)
#     for e in filenames_to_delete:
#         os.remove(e)
#     for e in maybe_delete:
#         os.remove(e)
#     print(len(filenames_to_delete))

    # find_special_filenames(dir_path_wp, dir_path_uploads) 
    
#     run_function_recursively_on_lines(dir_path = dir_path_wp, recursive_func_for_lines = replace_substr, new_substr = "300px", old_substr = "225px")   
#     run_function_recursively_on_lines(dir_path = dir_path_wp, recursive_func_for_lines = replace_substr, new_substr = "200px", old_substr = "230px")   
#     run_function_recursively_on_lines(dir_path = dir_path_wp, recursive_func_for_lines = replace_substr, new_substr = "300px", old_substr = "317px")   
#     run_function_recursively_on_lines(dir_path = dir_path_wp, recursive_func_for_lines = replace_substr, new_substr = "200px", old_substr = "210px")   
#     run_function_recursively_on_lines(dir_path = dir_path_wp, recursive_func_for_lines = replace_substr, new_substr = "150px", old_substr = "140px")   
#     run_function_recursively_on_lines(dir_path = dir_path_wp, recursive_func_for_lines = replace_substr, new_substr = "150px\"", old_substr = "75px\"")   
#     
#     imgheights = []   
#     run_function_recursively_on_lines(dir_path = dir_path_wp, 
#                                       recursive_func_for_lines = return_all_matches,
#                                       pattern = "imgheight=\"([0-9]+)px\"", 
#                                       result = imgheights)
#     sort_count_occurances(a_list = [int(r) for r in imgheights])  
#     
    images_in_code = []
    run_function_recursively_on_lines(dir_path = dir_path_wp, 
                                      recursive_func_for_lines = return_all_images, result = images_in_code, one_line = True)
    images_in_code.sort(key = lambda i:i['filename'])
    print_one_more = False
    prev_record = {'filename' : None}
    dupe_filenames = set()
    for im in images_in_code:
        if (prev_record['filename'] == im['filename']) and (prev_record != im):
            dupe_filenames.add(prev_record['filename'])
        prev_record = im
    b = "";
    print(dupe_filenames)
     
    errors = []   
    for im in images_in_code:
        if not im["id"] != (not(im["src"])):
            errors.append(im['filename'] + ' id src mismatch ' + str(im))
        if im["sourcehrf"] and  (not(im["sourcename"])):
            errors.append(im['filename'] + ' id sourcehrf sourcename ' + str(im))
        if (not im["sourcename"]) != (not (not(im["src"]))) and im["sourcename"] is not None:
            errors.append(im['filename'] + ' id src sourcename ' + str(im))
    for e in errors:
        print(e)      
        
    ah = ['sotheb', 'bonham', 'christi', 'yogaoutlet']
    ah_herf = []
    auction_filenames = []    
    for im in images_in_code:
        if im["sourcehrf"]:
            for a in ah:
                if a in im["sourcehrf"].lower():
                    ah_herf.append(im["sourcehrf"])
                    auction_filenames.append(im['filename'])
    ah_herf.sort()
    for a in ah_herf:
        print(a)
    
    for_php = []    
    dont_do = (list(auction_filenames) + list(dupe_filenames))
    for im in images_in_code: 
        if im['filename'] in dont_do:
            continue
        params = [im['folder_name'] + "/" + im['filename']]
        if im["src"]:
            params.append(im["src"])
        else:
            params.append(im["sourcename"])
        if im["sourcehrf"]:
            params.append(im["sourcehrf"])
        else:
            params.append(im["id"])
        if im['caption']:
            params.append(im['caption'].replace('\n', '<br/>'))

        new_php = '    insert_into_images(' '"' +  '", \n                            "'.join(p for p in params if p is not None)  + '");'
        for_php.append(im['all'])
        for_php.append(im['params'])
        for_php.append(im['params_replaced'])
        for_php.append(new_php)
        
    for f in for_php:
        print(f)
         

        
 
    #images_in_code2 = list(set(images_in_code[2]))
    #images_in_code2.sort()
#      
#     _, filenames = get_filenames(dir_path = dir_path_uploads)
#     filenames = list(set([f.lower() for f in filenames]))
#     filenames.sort()
#      
#     filenames = collections.Counter(filenames)
#     images_in_code = collections.Counter(images_in_code)
#      
#     overlap = list((images_in_code & filenames).elements())
#     not_found = list((images_in_code - filenames).elements())
#     not_used = list((filenames - images_in_code).elements())
#  
#     not_used = [nu for nu in not_used if not(nu.endswith(".pdf")) and ("_cover." not in nu) and not (nu.startswith("arrow"))
#                     and (nu not in ("horsemen.jpg", "18519635_10154766867823869_761601479270985007_n.jpg"))]
#     print("NOT FOUND: " + str(len(not_found)))
#     for b in not_found:
#         print(b)
#     print("NOT USED: " + str(len(not_used)))
#     for b in not_used:
#         print(b)
#       
#     _, filenames = get_filenames(dir_path = dir_path_wp)
#     filenames.sort(reverse=True)
#     
#     for fn in filenames:
#         if ("aux." in  fn):
#             continue
#         new_directory = os.path.join(dir_path_uploads, fn[:-4])
#         print(new_directory)
#         if not os.path.exists(new_directory):
#             os.makedirs(new_directory)
#         images_in_code = []
#         do_on_all_lines(file_path = os.path.join(dir_path_wp, fn), 
#                                           line_func = return_all_images, 
#                                           result = images_in_code, 
#                                           one_line = True)
#         _, uploads5_filenames = get_filenames(dir_path = dir_path_uploads5, lower = False)
#         for ufn in uploads5_filenames:
#             if ufn.lower() in images_in_code:
#                 ufn_with_path = os.path.join(dir_path_uploads5, ufn)
#                 shutil.move(ufn_with_path, os.path.join(new_directory, ufn))
#         for iic in images_in_code:
#             if not isfile(os.path.join(new_directory, iic)):
#                 print("could not find " + iic)
           
        
    
    # run_function_recursively_on_lines(dir_path = dir_path, recursive_func_for_lines = , old_substr = "http://www.yu51a5.com/wp-content/uploads/durers-rhino1.jpg", new_substr = "durers-rhino1.jpg")

    
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
    # run_function_recursively_on_lines(dir_path = dir_path, recursive_func_for_lines = print_if_found, substring = "??")
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
