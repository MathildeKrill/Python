'''
Created on 31 Mar 2018

@author: yuliavoevodskaya
'''
import cv2, os, pydub, os, codecs, shutil, datetime, PIL, re, pip

if __name__ == '__main__':
    
    with open(os.path.expanduser('~/Downloads/temp_join3.txt'), 'w') as the_file:
        the_file.writelines(l + "\n" for l in ['a', 'b', 'c4'])
        
    with open(os.path.expanduser('~/Downloads/temp3.txt'), 'w') as the_file:
        the_file.writelines(['d', 'e', 'f'])
        
    #audio = pydub.AudioSegment.silent(duration = 0)
    audio_name = os.path.expanduser('~/Downloads/Fur Elise.mp3') # just under 3 min long
    audio = pydub.AudioSegment.from_mp3(audio_name)
    for compilation_audio in (audio * 370, ):
        length_music = len(compilation_audio) / 60000.0
        print("compilation_audio duration (min): " + str((length_music)))
        mp3_path = os.path.expanduser('~/Downloads/compilation' + str(int(length_music)) + '.mp3')
        compilation_audio.export(mp3_path, format = "mp3")
        
    installed_packages = pip.get_installed_distributions()
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                      for i in installed_packages])
    print(installed_packages_list)