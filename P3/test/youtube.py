'''
Created on 30 Mar 2018

@author: yuliavoevodskaya
'''
import cv2, os, pydub, os, codecs, shutil, datetime, PIL
from PIL import ImageFont, ImageDraw

def get_filenames_with_extensions_recursively(directory_name, extensions):
    result = []
    for file_or_directory in os.listdir(directory_name):
        file_or_directory_with_path = os.path.join(directory_name, file_or_directory)
        if os.path.isdir(file_or_directory):
            result += get_filenames_with_extensions_recursively(
                                            file_or_directory_with_path, extensions)
            continue 
        for extension in extensions:
            if file_or_directory.endswith(extension):
                result += [file_or_directory_with_path]
                continue
    return result

def get_for_audio_track_number(audio_name):
    audio_mediainfo = pydub.utils.mediainfo(audio_name).get('TAG', None)
    track_str = audio_mediainfo['track'] 
    track_nb_str = track_str.split('/') 
    return int(track_nb_str[0])      

def make_short_videos(directory_name, 
                      width, 
                      height,
                      sub_font_size, 
                      sub_font_name, 
                      sub_encoding, 
                      sub_colour, 
                      description_intro, 
                      file_encoding, 
                      image_extensions = ('.jpg', ),
                      audio_extensions = ('.mp3', )):
    
    #prepare the directory and filenames
    temp_folder = os.path.join(directory_name, 'temp')
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)
    temp_image_name        = os.path.join(temp_folder, os.path.basename(directory_name) + '_temp.jpg') 
    silent_video_name      = os.path.join(temp_folder, os.path.basename(directory_name) + '_silent.mp4')
    descriptions_file_path = os.path.join(temp_folder, os.path.basename(directory_name) + '.txt')
    compilation_audio_name = os.path.join(temp_folder, os.path.basename(directory_name) + '.mp3')
    video_name             = os.path.join(temp_folder, os.path.basename(directory_name) + '.mp4')

    # get the filenames and sort them
    images_filenames = get_filenames_with_extensions_recursively(directory_name, image_extensions)
    images_filenames.sort() 
    audio_filenames =  get_filenames_with_extensions_recursively(directory_name, audio_extensions)
    audio_filenames.sort(key = lambda af: (os.path.dirname(af), get_for_audio_track_number(af)))
    
    # initiate variables
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    font = PIL.ImageFont.truetype(sub_font_name, sub_font_size, encoding = sub_encoding)  
                 
    descriptions = description_intro
    audio = pydub.AudioSegment.silent(duration = 0)
    video = cv2.VideoWriter(silent_video_name, fourcc, 1.0, (width, height))
    
    counter_audio = 0
    counter_seconds = 0
    
    for audio_name in audio_filenames:
        audio_piece = pydub.AudioSegment.from_mp3(audio_name)
        audio_mediainfo = pydub.utils.mediainfo(audio_name).get('TAG', None)       
        # print(str(audio_piece.duration_seconds))
        print(str(audio_mediainfo))
        counter_audio = counter_audio + 1
        track_name = 'Track ' + str(counter_audio) + ": " + audio_mediainfo['title']
        descriptions += [str(datetime.timedelta(seconds=counter_seconds)) + " " + track_name.replace('\\', '') + " by " + audio_mediainfo['TCM']]
        
        #prepare the image: resize and add subtitles using PIL
        img = PIL.Image.open(images_filenames[counter_audio % len(images_filenames)])
        img = img.resize((width, height), PIL.Image.ANTIALIAS)
        
        draw = PIL.ImageDraw.Draw(img)        
        draw.text((10, height - 4 * sub_font_size), track_name            , sub_colour, font = font)
        draw.text((10, height - 2 * sub_font_size), audio_mediainfo['TCM'], sub_colour, font = font)
        
        img.save(temp_image_name)
         
        # add the image to the video using PIL (adding by 1sec-long frames)  
        img2 = cv2.imread(temp_image_name)
        counter_frames = 0
        while (counter_frames < (audio_piece.duration_seconds + 1)):
            video.write(img2) 
            counter_frames = counter_frames + 1
            counter_seconds = counter_seconds + 1
         
        # add the soundtrack to the audio compilation   
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
    audio.export(compilation_audio_name, format = "mp3")   
    
    # combine audio and video
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