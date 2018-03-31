'''
Created on 30 Mar 2018

@author: yuliavoevodskaya
'''
import cv2, os, pydub, os, shlex, codecs, shutil, copy
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
    for audio_name in audio_filenames:
        print(audio_name)    
        audio_piece = AudioSegment.from_mp3(audio_name)
        audio_mediainfo = pydub.utils.mediainfo(audio_name).get('TAG', None)
        
        print(str(audio_piece.duration_seconds))
        img = copy.deepcopy(images[counter_audio % len(images)])
        counter_audio = counter_audio + 1
        track_name = 'Track ' + str(counter_audio) + ": " + audio_mediainfo['title']
        cv2.putText(img, track_name            , (10,600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), cv2.LINE_4)       
        cv2.putText(img, audio_mediainfo['TCM'], (10,700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), cv2.LINE_4)       
        
        # create a silent video
        silent_video_name = os.path.join(temp_folder, os.path.basename(audio_name)[:-4] + '_silent.mp4')
        print(silent_video_name)
        video = cv2.VideoWriter(silent_video_name, fourcc, 0.5, (width, height))
        counter_frames = 0
        while (counter_frames < (audio_piece.duration_seconds + 3)):
            video.write(img) 
            counter_frames = counter_frames + 2       
        cv2.destroyAllWindows()
        video.release()
        
        # add audio
        video_name = os.path.join(temp_folder, os.path.basename(audio_name)[:-4].replace(',', '').replace("'", '').replace(" ", '') + '.mp4')
        os.system('ffmpeg -i "' + silent_video_name + '" -i "' + audio_name + '" -shortest -c:v copy -c:a aac -b:a 256k "' + video_name + '"')
        os.remove(silent_video_name)
    
def join_videos(directory_name):
    temp_folder = get_temp_folder(directory_name)
    output_name = os.path.basename(os.path.dirname(directory_name)) 
    output_video_name = os.path.join(directory_name, output_name + '.mp4') 
    output_text_name = os.path.join(directory_name, output_name + '.txt')
    if os.path.exists(output_video_name):
        os.remove(output_video_name)   

    video_filenames =  [os.path.join(temp_folder, fn) for fn in os.listdir(temp_folder) 
                            if fn.endswith('.mp4')]
    video_filenames.sort()
    video_filenames = ['file ' + shlex.quote(video_name) for video_name in video_filenames]     
    print(video_filenames)
    write_to_file(file_path = output_text_name, file_content = '\n'.join(video_filenames))
    
    ffmpeg_line = 'ffmpeg -f concat -safe 0 -i "' + output_text_name + '" -c copy "' + output_video_name + '"'
    print(ffmpeg_line)
    os.system(ffmpeg_line)     

if __name__ == '__main__':
    dir_path = os.path.expanduser('~/Music/LouisXIII copy/')
    make_short_videos(dir_path, 1280, 720)
    join_videos(dir_path)
    print("done")