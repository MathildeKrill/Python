'''
Created on 30 Mar 2018

@author: yuliavoevodskaya
'''
import cv2, os, pydub, os, codecs, shutil, datetime, PIL, re
from PIL import ImageFont, ImageDraw

def get_filenames_with_extensions_recursively(directory_name, extensions):
    result = []
    for file_or_directory in os.listdir(directory_name):
        file_or_directory_with_path = os.path.join(directory_name, file_or_directory)
        if os.path.isdir(file_or_directory_with_path):
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
    try:
        track_str = audio_mediainfo['track'] 
        track_nb_str = track_str.split('/')
        return int(track_nb_str[0]) 
    except:
        return -1  

def make_video(       directory_name, 
                      func_get_audio_description_subtitles,
                      width = 1280, 
                      height = 720, 
                      sub_font_size = 32,
                      sub_font_name = "/System/Library/Fonts/SFNSText.ttf", 
                      sub_encoding = "unic", 
                      sub_colour = (0, 0, 255),
                      sub_indent_x = 10,
                      description_intro = ['Intended for personal use. I own the CDs.', ''],
                      file_encoding = 'utf-8', 
                      image_extensions = ('.jpg', ),
                      audio_extensions = ('.mp3', ), 
                      dry_run = False):
    
    #prepare the directory and filenames
    temp_folder = os.path.join(directory_name, 'temp')
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    temp_image_name        = os.path.join(temp_folder, os.path.basename(directory_name) + '_temp.jpg') 
    silent_video_name      = os.path.join(temp_folder, os.path.basename(directory_name) + '_silent.mp4')
    descriptions_file_path = os.path.join(temp_folder, os.path.basename(directory_name) + '.txt')
    compilation_audio_name = os.path.join(temp_folder, os.path.basename(directory_name) + '.mp3')
    video_name             = os.path.join(temp_folder, os.path.basename(directory_name) + '.mp4')
    ffmpeg_output_path     = os.path.join(temp_folder, os.path.basename(directory_name) + '_ffmpeg.out')
    if os.path.exists(temp_image_name):
        os.remove(temp_image_name)
    if os.path.exists(compilation_audio_name):
        os.remove(compilation_audio_name)
        
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
        audio_mediainfo = pydub.utils.mediainfo(audio_name).get('TAG', None)       
       
        counter_audio += 1
        description, subtitles = func_get_audio_description_subtitles(counter_audio, audio_mediainfo)
        descriptions += [str(datetime.timedelta(seconds=counter_seconds)) + " " + description]
        
        if not dry_run:               
            #prepare the image: resize and add subtitles using PIL
            img = PIL.Image.open(images_filenames[counter_audio % len(images_filenames)])
            img = img.resize((width, height), PIL.Image.ANTIALIAS)
            
            draw = PIL.ImageDraw.Draw(img)
            sub_indent_y = height
            for subtitle in reversed(subtitles):  
                sub_indent_y -=  2 * sub_font_size     
                draw.text((sub_indent_x, sub_indent_y), subtitle, sub_colour, font = font)
            
            img.save(temp_image_name)
             
            # add the image to the video using PIL (adding by 1sec-long frames)  
            img2 = cv2.imread(temp_image_name)
        else:
            img2 = None
            
        audio_piece = pydub.AudioSegment.from_mp3(audio_name)        
        counter_frames = 0
        while (counter_frames < (audio_piece.duration_seconds + 1)):
            if not dry_run:
                video.write(img2) 
            counter_frames = counter_frames + 1
            counter_seconds = counter_seconds + 1
        
        if dry_run: 
            continue
        # add the soundtrack to the audio compilation   
        audio = audio + audio_piece
        # match the duration of audio and video so far
        audio = audio + pydub.AudioSegment.silent(duration =  (counter_seconds * 1000.0 - len(audio))) 
                  
    cv2.destroyAllWindows()
    video.release()
    
    print("total length (min) is " + str(counter_seconds / 60.0))
    descriptions_len = 0
    for d_line in descriptions:
        print (d_line)
        descriptions_len += len(d_line)
    print("Descriptions length is (chars) " + str(descriptions_len))
    with codecs.open(descriptions_file_path, 'w', encoding = file_encoding) as the_file:
        the_file.writelines(d_line + "\n" for d_line in (descriptions))
    
    # dump the long mp3
    audio.export(compilation_audio_name, format = "mp3")   
    
    # combine audio and video
    ffmpeg_cmd = 'ffmpeg -i "' + silent_video_name + '" -i "' + compilation_audio_name \
                + '" -shortest -c:v copy -c:a aac -b:a 256k "' + video_name + '"' \
                + ' > "'+ ffmpeg_output_path + '" 2>&1'
    print(ffmpeg_cmd)
    os.system(ffmpeg_cmd)   

def get_audio_description_subtitles_louis(counter_audio, audio_mediainfo):
    title = audio_mediainfo['title'].replace('\\', '')
    track_name = 'Track ' + str(counter_audio) + ": " + title
    artist_name = audio_mediainfo['TCM'].replace('\\', '')
    artist_name = (re.split('\s\((\d\d\d\d-\d\d\d\d)\)', artist_name))[0]# remove dates like (1578-1645)
    desc = track_name
    if artist_name != 'Dumont, Henry; Lully, Jean-Baptiste; Desmarets, Henry':
        desc += " by " + artist_name
    return desc, [track_name, artist_name]

def get_audio_description_subtitles_farsi(counter_audio, audio_mediainfo):
    track_name = 'Track ' + str(counter_audio) 
    return track_name, [track_name, "Colloquial Persian by Abdi Rafiee"]

def dry_runget_audio_description_subtitles_dry_run(counter_audio, audio_mediainfo):
    print(audio_mediainfo)   
    return "", ""

if __name__ == '__main__':
#     make_video(   directory_name = os.path.expanduser('~/Music/iTunes/iTunes Media/Music/Unknown Artist/Farsi'), 
#                   func_get_audio_description_subtitles = get_audio_description_subtitles_farsi,
#                   description_intro = ['', 'Colloquial Persian by Abdi Rafiee', 'Intended for personal use. I own the book.', ''],
#                   dry_run = True)
# 
    dirs = ['Louis XIV 23']
    for d in dirs:
        make_video(   directory_name = os.path.expanduser('~/Music/' + d), 
                      func_get_audio_description_subtitles = get_audio_description_subtitles_louis,
                      dry_run = False)
    print("done")
