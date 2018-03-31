'''
Created on 30 Mar 2018

@author: yuliavoevodskaya
'''
import cv2, os, pydub, os, codecs, shutil, copy
from pydub import AudioSegment

def get_temp_folder(directory_name):
    return os.path.join(directory_name, 'temp2')

def make_temp_dir(directory_name):
    temp_folder = get_temp_folder(directory_name)
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)
    return temp_folder

# do something on all lines of a file
my_encoding = 'utf-8'

def write_to_file(file_path, file_content):
    with codecs.open(file_path, 'w', encoding = my_encoding) as the_file:
        the_file.writelines(file_content)

def make_short_videos(directory_name, width, height):
    
    temp_folder = make_temp_dir(directory_name)

    images_filenames =  [os.path.join(directory_name, fn) for fn in os.listdir(directory_name) 
                            if (fn.endswith('.jpg') or (fn.endswith('.png')))]
    images_filenames.sort()
    images = [cv2.imread(im_name) for im_name in images_filenames]
    images = [cv2.resize(img, (width, height)) for img in images]       
        
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    audio_filenames =  [os.path.join(directory_name, fn) for fn in os.listdir(directory_name) 
                            if fn.endswith('.mp3')]
    audio_filenames.sort()
    counter_audio = 0
    counter_seconds = 0
    
    # create a silent video
    silent_video_name = os.path.join(temp_folder, os.path.basename(directory_name) + '_silent.mp4')
    video = cv2.VideoWriter(silent_video_name, fourcc, 1.0, (width, height))
    
    #combine mp3s
    audio = AudioSegment.silent(duration = 0)
    
    for audio_name in audio_filenames:
        # print(audio_name)    
        audio_piece = AudioSegment.from_mp3(audio_name)
        audio_mediainfo = pydub.utils.mediainfo(audio_name).get('TAG', None)       
        # print(str(audio_piece.duration_seconds))
        img = copy.deepcopy(images[counter_audio % len(images)])
        counter_audio = counter_audio + 1
        track_name = 'Track ' + str(counter_audio) + ": " + audio_mediainfo['title']
        cv2.putText(img, track_name            , (10,600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), cv2.LINE_4)       
        cv2.putText(img, audio_mediainfo['TCM'], (10,700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), cv2.LINE_4)       
      
        counter_frames = 0
        while (counter_frames < (audio_piece.duration_seconds + 1)):
            video.write(img) 
            counter_frames = counter_frames + 1
            counter_seconds = counter_seconds + 1
            
        audio = audio + audio_piece
        # match the duration of audio and video so far
        audio = audio + AudioSegment.silent(duration =  (counter_seconds * 1000.0 - len(audio))) 
                  
    cv2.destroyAllWindows()
    video.release()
    print('1')
    # dump the long mp3
    compilation_audio_name = os.path.join(temp_folder, os.path.basename(directory_name) + '.mp3')
    audio.export(compilation_audio_name, format = "mp3")   
    print('2')    
    # add audio and remove the intermediate files
    video_name = os.path.join(directory_name, os.path.basename(directory_name) + '.mp4')
    os.system('ffmpeg -i "' + silent_video_name + '" -i "' + compilation_audio_name + '" -shortest -c:v copy -c:a aac -b:a 256k "' + video_name + '"')
    os.remove(silent_video_name)
    os.remove(compilation_audio_name)
    

if __name__ == '__main__':
    dir_path = os.path.expanduser('~/Music/LouisXIII')
    make_short_videos(dir_path, 1280, 720)
    #join_videos(dir_path)
    print("done")