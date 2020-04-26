
my_encoding = 'utf-8'
import codecs, os
from os.path import isfile, expanduser

file_path = expanduser('~/Desktop/feb_07.txt')


def remove_char(file_path, new_file_path, char_to_remove):
    with codecs.open(file_path, encoding = my_encoding) as file_opened:
        file_content_list = file_opened.readlines()
    for line in file_content_list:
        chars = [line]
        print(chars)
    new_file_content_list = [line.replace(char_to_remove, '') for line in file_content_list]
    for line in new_file_content_list:
        chars = [line]
        print(chars)
    with codecs.open(new_file_path, 'w', encoding = my_encoding) as the_file:
        the_file.writelines(new_file_content_list)

if __name__ == '__main__':
    file_path_2 = file_path[:-4] + '2' + file_path[-4:]
    file_path_3 = file_path[:-4] + '3' + file_path[-4:]
    remove_char(file_path = file_path, new_file_path = file_path_2, char_to_remove = '\xad')
    remove_char(file_path = file_path_2, new_file_path = file_path_3, char_to_remove = '\u2028')
    print(file_path[:-4] + '_2' + file_path[-4:])
