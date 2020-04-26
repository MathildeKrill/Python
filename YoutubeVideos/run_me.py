from youtube import make_video, get_audio_description_subtitles_simple
import re
import os

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

def get_audio_description_subtitles_LeGenreHumain(counter_audio, audio_mediainfo):
    titles = ["Le Genre Humain", "Noël", "Le Bonheur C'est Mieux Que La Vie", 
     "Le Genre Humain", "Le Courage D'aimer", "Le Bonheur C'est Mieux Que La Vie (Version Instrumentale)", 
     "Crépuscule Sur Le Boulevard", "Noël (Instrumental)", "2000 Ans Et Des Poussières", 
     "Crépuscule Sur Le Boulevard", "Le Genre Humain", "La Ville Lumière (Instrumental)", 
     "J'ai Pas Tout Dit", "2000 Ans Et Des Poussières (Instrumental)", "Maria Mari", 
     "Le Courage D'aimer (Instrumental)", "Le Bonheur C'est Mieux Que La Vie", "La Ville Lumière"]
    title = titles[counter_audio-1]
    track_name = 'Track ' + str(counter_audio) + ": " + title
    artist_name = "Francis Lai"
    desc = track_name + " by " + artist_name
    return desc, [track_name, artist_name]

def get_audio_description_subtitles_hsk(counter_audio, audio_mediainfo):
    title = audio_mediainfo['title'].strip()
    track_name = 'Track ' + str(counter_audio) + ": " + title
    desc = track_name
    return desc, [track_name, '']

if __name__ == '__main__':

#     make_video(   directory_name = os.path.expanduser('~/Music/iTunes/iTunes Media/Music/Unknown Artist/Farsi'), 
#                   func_get_audio_description_subtitles = get_audio_description_subtitles_farsi,
#                   description_intro = ['', 'Colloquial Persian by Abdi Rafiee', 'Intended for personal use. I own the book.', ''],
#                   dry_run = True)
# 
    dirs = [ 'iTunes/iTunes Media/Music/Michel Thomas Method/Mandarin Chinese IV/' + str(i) for i in range(9, 11)
             #'iTunes/iTunes Media/Music/Michael Thomas/Total Mandarin Chinese 1', 
             #'iTunes/iTunes Media/Music/Michel Thomas Method/Total • Mandarin Chinese'
             #'Yiru/Yiruma - River Flows In You (2011)', 'Yiru/Yiruma - Piano (2015)', 'Yiru/Yiruma - Blind Film (2013)', 
             ]
    #'LouisXIII', 'Louis XIV 13', 'Louis XIV 23']#]
    for d in dirs:
        directory_name = os.path.expanduser('~/Music/' + d)
        make_video(   directory_name = directory_name,
                      video_title = 'Total Mandarin ' + os.path.basename(directory_name),
                      artist_override = 'Michael Thomas',
                      func_get_audio_description_subtitles = get_audio_description_subtitles_simple, # get_audio_description_subtitles_louis,
                      description_intro = ['Intended for personal use. I own the CDs', ''],
                      dry_run = False)
        
#     make_video(   directory_name = "/Volumes/My Passport/Netbook/Music/COMPPiLATIONS/Williams - Spanish Guitar Music",
#                   artist_override = 'John Williams',
#                   dry_run = False)
     
#     make_video(   directory_name = "/Volumes/My Passport/Netbook/Music/Francis Lai",
#                   func_get_audio_description_subtitles = get_audio_description_subtitles_LeGenreHumain,
#                   dry_run = False)
        
    print("done")
    
    