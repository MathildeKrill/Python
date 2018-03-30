'''
Created on 30 Mar 2018

@author: yuliavoevodskaya
'''
import cv2, os#, pydub
import numpy as np
from os.path import expanduser
from pydub.utils import mediainfo, AudioSegment

def make_temp_dir(directory_name):
    temp_folder = os.path.join(directory_name, 'temp2')
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    return temp_folder

def make_long_mp3(directory_name):
    
    temp_folder = make_temp_dir(directory_name)
    audio_name = os.path.join(temp_folder, 'audio.mp3')
    
    one_sec_pause = AudioSegment.silent(duration=1000) # 1 sec
    audio = one_sec_pause
    
    audio_filenames =  [os.path.join(directory_name, fn) for fn in os.listdir(directory_name) 
                            if fn.endswith('.mp3')]
    for au_name in audio_filenames:    
        audio_piece = AudioSegment.from_mp3(au_name)
        audio = audio + audio_piece + one_sec_pause
        print(mediainfo(audio_piece).get('TAG', None))

    audio.export(audio_name, format="mp3")
    
def make_video2(directory_name, width, height):
    
    temp_folder = make_temp_dir(directory_name)
    video_name = os.path.join(temp_folder, 'video.mp4') 
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, 0.5, (width, height))
    
    images_filenames =  [os.path.join(directory_name, fn) for fn in os.listdir(directory_name) 
                            if (fn.endswith('.jpg') or (fn.endswith('.png')))]
    for im_name in images_filenames:
        img = cv2.imread(im_name)
        resized_img = cv2.resize(img, (width, height)) 
        video.write(resized_img)
    
    cv2.destroyAllWindows()
    video.release()

if __name__ == '__main__':
    dir_path = expanduser('~/Music/LouisXIII/')
    make_video2(dir_path, 1280, 720)
    print("done")