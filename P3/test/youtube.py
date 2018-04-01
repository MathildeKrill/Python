'''
Created on 30 Mar 2018

@author: yuliavoevodskaya
'''
import cv2, os, pydub, os, codecs, shutil, datetime, PIL
from PIL import ImageFont, ImageDraw

def make_short_videos(directory_name, 
                      width, 
                      height, 
                      sub_font_size, 
                      sub_font_name, 
                      sub_encoding, 
                      sub_colour, 
                      description_intro, 
                      file_encoding):
    
    temp_folder = os.path.join(directory_name, 'temp')
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)

    images_filenames =  [os.path.join(directory_name, fn) for fn in os.listdir(directory_name) if fn.endswith('.jpg')]
    images_filenames.sort()
    temp_image_name = os.path.join(temp_folder, os.path.basename(directory_name) + '_temp.jpg') 
     
    # audio   
    audio_filenames =  [os.path.join(directory_name, fn) for fn in os.listdir(directory_name) 
                            if fn.endswith('.mp3')]
    audio_filenames.sort()
    counter_audio = 0
    counter_seconds = 0
    
    # initiate variables for creating a silent video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    silent_video_name = os.path.join(temp_folder, os.path.basename(directory_name) + '_silent.mp4')
    video = cv2.VideoWriter(silent_video_name, fourcc, 1.0, (width, height))
    font = PIL.ImageFont.truetype(sub_font_name, sub_font_size, encoding = sub_encoding)               
    
    # initiate variables for combining mp3s and descriptions
    audio = pydub.AudioSegment.silent(duration = 0)
    descriptions = description_intro
    descriptions_file_path = os.path.join(temp_folder, os.path.basename(directory_name) + '.txt')
    
    for audio_name in audio_filenames:
        audio_piece = pydub.AudioSegment.from_mp3(audio_name)
        audio_mediainfo = pydub.utils.mediainfo(audio_name).get('TAG', None)       
        # print(str(audio_piece.duration_seconds))
        counter_audio = counter_audio + 1
        track_name = 'Track ' + str(counter_audio) + ": " + audio_mediainfo['title']
        descriptions += [str(datetime.timedelta(seconds=counter_seconds)) + " " + track_name.replace('\\', '') + " by " + audio_mediainfo['TCM']]
        
        img = PIL.Image.open(images_filenames[counter_audio % len(images_filenames)])
        img = img.resize((width, height), PIL.Image.ANTIALIAS)
        
        draw = PIL.ImageDraw.Draw(img)        
        draw.text((10, height - 4 * sub_font_size), track_name            , sub_colour, font = font)
        draw.text((10, height - 2 * sub_font_size), audio_mediainfo['TCM'], sub_colour, font = font)
        
        img.save(temp_image_name)
             
        img2 = cv2.imread(temp_image_name)
        counter_frames = 0
        while (counter_frames < (audio_piece.duration_seconds + 1)):
            video.write(img2) 
            counter_frames = counter_frames + 1
            counter_seconds = counter_seconds + 1
            
        audio = audio + audio_piece
        # match the duration of audio and video so far
        audio = audio + pydub.AudioSegment.silent(duration =  (counter_seconds * 1000.0 - len(audio))) 
                  
    cv2.destroyAllWindows()
    video.release()
    
    for d_line in descriptions:
        print (d_line)
    with codecs.open(descriptions_file_path, 'w', encoding = file_encoding) as the_file:
        the_file.writelines('/n'.join(descriptions))
    
    # dump the long mp3
    compilation_audio_name = os.path.join(temp_folder, os.path.basename(directory_name) + '.mp3')
    audio.export(compilation_audio_name, format = "mp3")   
    
    # combine audio and video
    video_name = os.path.join(temp_folder, os.path.basename(directory_name) + '.mp4')
    os.system('ffmpeg -i "' + silent_video_name + '" -i "' + compilation_audio_name 
                + '" -shortest -c:v copy -c:a aac -b:a 256k "' + video_name + '"')   
       

if __name__ == '__main__':
    make_short_videos(directory_name = os.path.expanduser('~/Music/LouisXIII copy'), 
                      width = 1280, 
                      height = 720, 
                      sub_font_size = 32,
                      sub_font_name = "/System/Library/Fonts/SFNSText.ttf", 
                      sub_encoding = "unic", 
                      sub_colour = (0, 0, 255),
                      description_intro = ['Intended for personal use. I own the CDs.', ''],
                      file_encoding = 'utf-8')
    print("done")