import subprocess
import asyncio
import shlex
import time
from datetime import datetime
from subprocess import Popen, PIPE

where = '/sysroot/home/emisar/Documente/Dezvoltare/Gather25/Dowload'

# https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/playlist.m3u8
# https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/1/playlist.m3u8
# https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/2/playlist.m3u8
# https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/3/playlist.m3u8
# https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist.m3u8
# https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/5/playlist.m3u8

# https://storage.sardius.media/archives/2153BA7C697A514/events/site_daa826D4F1/5/playlist.m3u8
# https://storage.sardius.media/archives/2153BA7C697A514/events/site_daa826D4F1/playlist.m3u8

playlists = [
    #eng
    #'https://storage.sardius.media/archives/2153BA7C697A514/events/site_daa826D4F1/5/playlist_1.m3u8',
    #'https://storage.sardius.media/archives/2153BA7C697A514/events/site_daa826D4F1/5/playlist_6.m3u8',
    #rom
    'https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_1.m3u8',
    'https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_6.m3u8',
    ]

numberOfZero = 5
numberParts = 10000

rangestart = 5333
rangestop = 5555
setOfStep = 50

dt = datetime.now()
ts = datetime.timestamp(dt)
where = where + '/' + str(ts)

def shutdown():
    aaaa = 'shutdown -h +1'
    myrunsubproces(aaaa)

def myrunsubproces(command, shell=True, check=True, text=True):
    print('Run command:', command)

    done = True
    i = 1
    while done:
        if i > 1:
            print('Run ' + str(i) + ' of command:', command)

        try:
            subprocess.run(command, shell=shell, check=check, text=text)
            return
        except:
            print("Something went wrong! We will try again.")
            time.sleep(1)
        i = i + 1

async def main():
    #command = shlex.split(command)
    proc = await asyncio.create_subprocess_exec(
       'ls','-lha',
       stdout=asyncio.subprocess.PIPE,
       stderr=asyncio.subprocess.PIPE)

    # do something else while ls is working

    # if proc takes very long to complete, the CPUs are free to use   cycles for 
    # other processes
    stdout, stderr = await proc.communicate()
 
#asyncio.run(main())

async def myrunsubprocesasync(command):
    print('Run command:', command)
    try:
        await subprocess.run(command, shell=True, check=True, text=True)
        return
    except:
        print("Something went wrong!")

def splitArray(array, size):
    result = []
    for i in range(0, len(array), size):
        result.append(array[i:i+size])
    return result

def commandForDownloadPlaylists(location, playlists):
    curlcommands = []
    txtfiles = []
    curlfiles = []
    for playlist in playlists:
        print('Playlist:', playlist)
        parts = playlist.rsplit('/', 3)
        stream = parts[1]
        parts = playlist.rsplit('/', 1)
        address = parts[0]
        parts = parts[-1].rsplit('.', 1)
        name = parts[0]
        extension = parts[-1]
        print(address, name, extension, '('+ stream +')')

        tempfolder = location + '/Playlist/' + stream + '/' + name
        tempsubfolder =  tempfolder + '/' + extension
        txtfile = tempfolder + '/' +  extension + '.txt'
        curlfile = tempfolder + '/' +  extension + '.curl.txt'
        txtfiles.append(txtfile)
        curlfiles.append(curlfile)

        myrunsubproces('mkdir -p ' + tempfolder)
        myrunsubproces('mkdir -p ' + tempsubfolder)

        playlist = 'curl ' + playlist + ' -o ' + tempfolder +'/' + name + '.' + extension
        myrunsubproces(playlist)

        mediafile = 'cat ' + tempfolder + '/' + name + '.' + extension + ' | grep ' + name + ' | sort -V | xargs -I "{}" echo "' + address + '/{}" > ' + txtfile
        myrunsubproces(mediafile)

        curldownloadfile = 'cat ' + tempfolder + '/' + name + '.' + extension + ' | grep ' + name + ' | sort -V | xargs -I "{}" echo "curl -m 55555 ' + address + '/{} > ' + tempsubfolder + '/{}" > ' + curlfile
        myrunsubproces(curldownloadfile)

        curlall = 'curl … $(cat ' + tempfolder + '/' + name + '.' + extension + ' | grep ' + name + ' | sort -V | xargs -I "{}" echo "' + address + '/{} -o '+ tempsubfolder + '/{}")'
        curlcommands.append(curlall)

    return curlcommands, txtfiles, curlfiles

def downloadAll(location, rangestart, rangestop, playlist, extension):
    tempfolder = location + '/All/' + str(rangestart) + '-' + str(rangestop - 1)
    mkvfolder = location + '/All/mkv'
    print(tempfolder, mkvfolder)
 
    myrunsubproces('mkdir -p ' + tempfolder)
    myrunsubproces('mkdir -p ' + mkvfolder)
 
    for x in range(rangestart, rangestop):
        number = "{:05d}".format(x)

        curl = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/' + playlist + '_' + number + '.' + extension + ' -o ' + tempfolder +'/'+ number + '.ts'

        myrunsubproces(curl)

    file = 'ls '+ tempfolder + '/*.ts | sort -V > ' + tempfolder + '/' + extension + '.txt'

    myrunsubproces(file)

    ffmpegts = 'ffmpeg -y -f mpegts -i concatf:' + tempfolder + '/' + extension + '.txt -c copy ' + tempfolder + '/ts.mkv'
    myrunsubproces(ffmpegts)

    deletetempfolder = 'rm -r ' + tempfolder
    myrunsubproces(deletetempfolder)

    tempfolder = location + '/' + str(rangestart) + '-' + str(rangestop - 1)
    mkvfolder = location + '/mkv'
    print(tempfolder, mkvfolder)
 
    myrunsubproces('mkdir -p ' + tempfolder)
    myrunsubproces('mkdir -p ' + mkvfolder)
 
    for x in range(rangestart, rangestop):
        number = "{:05d}".format(x)

        curlts = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_1_' + number + '.ts -o ' + tempfolder +'/'+ number + '.ts'
        curlaac = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_6_' + number + '.aac -o ' + tempfolder +'/'+ number + '.aac'

        myrunsubproces(curlts)
        myrunsubproces(curlaac)

    filets = 'ls '+ tempfolder + '/*.ts | sort -V > ' + tempfolder + '/ts.txt'
    fileaac = 'ls '+ tempfolder + '/*.aac | sort -V > ' + tempfolder + '/aac.txt'

    myrunsubproces(filets)
    myrunsubproces(fileaac)

    ffmpegts = 'ffmpeg -y -f mpegts -i concatf:' + tempfolder + '/ts.txt -c copy ' + tempfolder + '/ts.mkv'
    myrunsubproces(ffmpegts)

    ffmpegaac = 'ffmpeg -y -i concatf:' + tempfolder + '/aac.txt -c copy ' + tempfolder + '/aac.mkv'
    myrunsubproces(ffmpegaac)

    ffmpegvideo = 'ffmpeg -y -i ' + tempfolder + '/ts.mkv -i ' + tempfolder + '/aac.mkv -c copy ' + mkvfolder + '/video_' + str(rangestart) + '-' + str(rangestop - 1) + '.mkv'
    myrunsubproces(ffmpegvideo)

    deletetempfolder = 'rm -r ' + tempfolder
    myrunsubproces(deletetempfolder)

def downloadGroupedNew(location, rangestop, rangestart=0, step=5, clear=False):
    print('Download at' ,location, 'from', rangestart, 'to', rangestop, 'grouped by', step)

    newrangestart = int(rangestart // step)
    newrangestop = int(rangestop // step) + 1

    for x in range(newrangestart, newrangestop):
        a = (x) * step
        b = (x + 1) * step

        if a < rangestart:
            a = rangestart
        if b >= rangestop:
            b = rangestop

        tempfolder = location + '/temp/' + str(a) + '-' + str(b - 1)
        mkvfolder = location + '/mkv'
     
        myrunsubproces('mkdir -p ' + tempfolder)
        myrunsubproces('mkdir -p ' + mkvfolder)

        for x in range(a, b):
            if (x > rangestop):
                break
            elif (x >= rangestart):
                numberZero = '{:0'+ str(numberOfZero) + 'd}'
                number = numberZero.format(x)

                curlts = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_1_' + number + '.ts -o ' + tempfolder +'/'+ number + '.ts'
                curlaac = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_6_' + number + '.aac -o ' + tempfolder +'/'+ number + '.aac'

                myrunsubproces(curlts)
                myrunsubproces(curlaac)

        filets = 'ls '+ tempfolder + '/*.ts | sort -V > ' + tempfolder + '/ts.txt'
        fileaac = 'ls '+ tempfolder + '/*.aac | sort -V > ' + tempfolder + '/aac.txt'

        myrunsubproces(filets)
        myrunsubproces(fileaac)

        ffmpegts = 'ffmpeg -y -f mpegts -i concatf:' + tempfolder + '/ts.txt -c copy ' + tempfolder + '/ts.mkv'
        myrunsubproces(ffmpegts)

        ffmpegaac = 'ffmpeg -y -i concatf:' + tempfolder + '/aac.txt -c copy ' + tempfolder + '/aac.mkv'
        myrunsubproces(ffmpegaac)

        ffmpegvideo = 'ffmpeg -y -i ' + tempfolder + '/ts.mkv -i ' + tempfolder + '/aac.mkv -c copy ' + mkvfolder + '/video_' + str(rangestart) + '-' + str(rangestop - 1) + '.mkv'
        myrunsubproces(ffmpegvideo)

        deletetempfolder = 'rm -r ' + tempfolder
        if clear:
            myrunsubproces(deletetempfolder)

'''
#downloadGroupedNew(where, rangestop, rangestart, step=setOfStep)
commands, files1, files2 = commandForDownloadPlaylists(where, playlists)

#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)
#tasks = []

for command in commands:
    print(command)
    
    #x = input("Run command?")
    #print("Hello, " + x)
    
    #command = shlex.split(command)
    #print(command)
    #process = Popen(command, stdout=PIPE, stderr=PIPE)
    #process = Popen(command)
    #stdout, stderr = process.communicate()
    
    #task = loop.create_task(myrunsubprocesasync(command))
    #tasks.append(task)
    
   #myrunsubproces(command)

#loop.run_until_complete(asyncio.wait(tasks))
#loop.close()

start = 5555
stop = start + 10
lenght = stop - start

x = input("Run command from files?")

for file in files2:

    # open the sample file used 
    file = open(file) 

    # read the content of the file opened 
    content = file.readlines()

    for line in content:
        print(line)
        myrunsubproces(line)
'''

'''
    for i in range(start, stop):
        print(i)
        print(content[i])
        myrunsubproces(content[i])
'''

romanaStart = 179
romanaStop = 9764

romanaAudio = '/sysroot/home/emisar/Video/Gather25/română/audio/'
romanaVideo = '/sysroot/home/emisar/Video/Gather25/română/video/'
romanaImpreuna = '/sysroot/home/emisar/Video/Gather25/română/împreună/'

engelzaStart = 179
engelzaStop = 9764

englezaAudio = '/sysroot/home/emisar/Video/Gather25/engleză/audio/'
englezaVideo = '/sysroot/home/emisar/Video/Gather25/engleză/video/'
englezaImpreuna1 = '/sysroot/home/emisar/Video/Gather25/engleză/1/'
englezaImpreuna2 = '/sysroot/home/emisar/Video/Gather25/engleză/2/'


rangestart = engelzaStart
rangestop = engelzaStop

from os import listdir
from os.path import isfile, join

def get_number_of_elements(list):
    count = 0
    for element in list:
        count += 1
    return count

def makeAVU(audio, video, mix, rangestart = -1, rangestop = -1):

    onlyfilesAudio = [f for f in listdir(audio) if isfile(join(audio, f))]
    onlyfilesVideo = [f for f in listdir(video) if isfile(join(video, f))]

    onlyfilesAudio.sort()
    onlyfilesVideo.sort()

    a = get_number_of_elements(onlyfilesAudio)
    b = get_number_of_elements(onlyfilesVideo)

    if (a == b):
        print('1 Egal', a, b)
    else:
        print('1 Diferit', a, b)
        return
    

    ffi = ''

    for x in range(rangestart, rangestop):
        #print(onlyfilesAudio[x], onlyfilesVideo[x])

        a = onlyfilesAudio[x].rsplit('_',1)[1].rsplit('.')[0]
        b = onlyfilesVideo[x].rsplit('_',1)[1].rsplit('.')[0]

        if (a == b):
            print('2 Egal', a, b)

            newfile = mix + 'mix' + a + '-' + b + '.ts'

            ffm = 'ffmpeg -y -i ' + audio + onlyfilesAudio[x] + ' -i ' + video + onlyfilesVideo[x] + ' -c copy ' + newfile
            #print(ffm)
            myrunsubproces(ffm)
            ffi = ffi + '|' + newfile

        else:
            print('2 Diferit', a, b)
    
    ffi = ffi[1:]
    ff = 'ffmpeg -y -i "concat:' + ffi + '" -c copy ' + mix + 'output.mkv'
    #print(ff)
    
    #myrunsubproces(ff)

    aaaa = 'mv ' + mix + 'output.mkv' + ' ' + mix + 'output.mkv.webm'
    #myrunsubproces(aaaa)

def uniteAudioAndVideo(mix):
    groupedBy = 123
    onlyfiles = [f for f in listdir(mix) if isfile(join(mix, f))]
    onlyfiles.sort()

    #ffmpeg -i "concat:input1.ts|input2.ts|input3.ts" -c copy output.ts

    arrays = splitArray(onlyfiles, groupedBy)
    for array in arrays:

        ffi = ''

        for file in array:
            ffi = ffi + '|' + mix + str(file)
        
        ffi = ffi[1:]

        name = 'group-' + str(array[0]) + '-' + str(array[-1])
        #print(name)

        ff = 'ffmpeg -i "concat:' + ffi + '" -c copy ' + mix + '../3/' + name + '-output.mkv'
        #print(ff)
        myrunsubproces(ff)

        aaaa = 'mv ' + mix + 'output.mkv' + ' ' + mix + 'output.mkv.webm'
        #myrunsubproces(aaaa)

s = 4988
e = 5900

#makeAVU(romanaAudio, romanaVideo, romanaImpreuna, s, e)
#makeAVU(englezaAudio, englezaVideo, englezaImpreuna, s, e)
#uniteAVU2(romanaImpreuna)

mix = romanaImpreuna
aaaa = 'mv ' + mix + 'output.mkv' + ' ' + mix + 'output.mkv.webm'
#myrunsubproces(aaaa)


s = 8042 - (8222 - 8042) #playlist_1_08042
s = 7850
e = 7863

#makeAVU(romanaAudio, romanaVideo, romanaImpreuna, s, e)


s = 0
e = s + 5
#makeAVU(englezaAudio, englezaVideo, englezaImpreuna, s, e)


s = 7863
e = s + 8
#makeAVU(englezaAudio, englezaVideo, englezaImpreuna, s, e)

uniteAudioAndVideo(englezaImpreuna1)
uniteAudioAndVideo(englezaImpreuna2)

shutdown()
