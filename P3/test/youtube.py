'''
Created on 30 Mar 2018

@author: yuliavoevodskaya
'''
import cv2, os, pydub, os
from pydub import AudioSegment

def make_temp_dir(directory_name):
    temp_folder = os.path.join(directory_name, 'temp2')
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    return temp_folder

def make_long_mp3(directory_name, width, height):
    
    temp_folder = make_temp_dir(directory_name)
    output_name = os.path.basename(os.path.dirname(directory_name)) 
    output_video_name = os.path.join(temp_folder, output_name + '.mp4') 
    output_audio_name = os.path.join(temp_folder, output_name + '.mp3')

    images_filenames =  [os.path.join(directory_name, fn) for fn in os.listdir(directory_name) 
                            if (fn.endswith('.jpg') or (fn.endswith('.png')))]
    images_filenames.sort()
    images = [cv2.imread(im_name) for im_name in images_filenames]
    images = [cv2.resize(img, (width, height)) for img in images]       
        
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
    one_sec_pause = AudioSegment.silent(duration=1000) # 1 sec    
    
    audio_filenames =  [os.path.join(directory_name, fn) for fn in os.listdir(directory_name) 
                            if fn.endswith('.mp3')]
    audio_filenames.sort()
    counter_images = 0
    for audio_name in audio_filenames:
        print(audio_name)    
        audio_piece = AudioSegment.from_mp3(audio_name)
        audio_mediainfo = pydub.utils.mediainfo(audio_name).get('TAG', None)
        title = audio_mediainfo['title'] + '\n' + audio_mediainfo['TCM']
        print(title)
        
        print(str(audio_piece.duration_seconds))
        
        # create a silent video
        silent_video_name = os.path.join(temp_folder, os.path.basename(audio_name)[:-4] + '_silent.mp4')
        print(silent_video_name)
        video = cv2.VideoWriter(silent_video_name, fourcc, 0.5, (width, height))
        counter_frames = 0
        while (counter_frames < (audio_piece.duration_seconds + 3)):
            img = images[counter_images]
            #cv2.addText(img, title, (10,500), cv2.FONT_HERSHEY_SIMPLEX)       
            video.write(img) 
            counter_frames = counter_frames + 2       
        cv2.destroyAllWindows()
        video.release()
        counter_images = (counter_images + 1) % len(images)
        
        # add audio
        video_name = os.path.join(temp_folder, os.path.basename(audio_name)[:-4] + '.mp4')
        os.system('ffmpeg -i "' + silent_video_name + '" -i "' + audio_name + '" -shortest -c:v copy -c:a aac -b:a 256k "' + video_name + '"')
        
    #audio.export(compilation_audio_name, format="mp3")    
    

if __name__ == '__main__':
    dir_path = os.path.expanduser('~/Music/LouisXIII/')
    make_long_mp3(dir_path, 1280, 720)
    print("done")