import subprocess
import asyncio
import shlex
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
    'https://storage.sardius.media/archives/2153BA7C697A514/events/site_daa826D4F1/5/playlist_1.m3u8',
    'https://storage.sardius.media/archives/2153BA7C697A514/events/site_daa826D4F1/5/playlist_6.m3u8',
    ]

numberOfZero = 5
numberParts = 10000

rangestart = 5333
rangestop = 5555
setOfStep = 50

dt = datetime.now()
ts = datetime.timestamp(dt)
where = where + '/' + str(ts)

def myrunsubproces(command, shell=True, check=True, text=True):
    print('Run command:', command)
    try:
        subprocess.run(command, shell=shell, check=check, text=text)
        return
    except:
        print("Something went wrong!")

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
 
asyncio.run(main())

async def myrunsubprocesasync(command):
    print('Run command:', command)
    try:
        await subprocess.run(command, shell=True, check=True, text=True)
        return
    except:
        print("Something went wrong!")

def commandForDownloadPlaylists(location, playlists):
    curlcommands = []
    txtfiles = []
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

        myrunsubproces('mkdir -p ' + tempfolder)
        myrunsubproces('mkdir -p ' + tempsubfolder)

        playlist = 'curl ' + playlist + ' -o ' + tempfolder +'/' + name + '.' + extension
        myrunsubproces(playlist)

        mediafile = 'cat ' + tempfolder + '/' + name + '.' + extension + ' | grep ' + name + ' | sort -V | xargs -I "{}" echo "' + address + '/{}" > ' + txtfile
        myrunsubproces(mediafile)

        curldownloadfile = 'cat ' + tempfolder + '/' + name + '.' + extension + ' | grep ' + name + ' | sort -V | xargs -I "{}" echo "curl ' + address + '/{} -o ' + tempsubfolder + '/{}" > ' + curlfile
        myrunsubproces(curldownloadfile)

        curlall = 'curl … $(cat ' + tempfolder + '/' + name + '.' + extension + ' | grep ' + name + ' | sort -V | xargs -I "{}" echo "' + address + '/{} -o '+ tempsubfolder + '/{}")'
        curlcommands.append(curlall)

    return curlcommands, txtfiles

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

#downloadGroupedNew(where, rangestop, rangestart, step=setOfStep)
commands = commandForDownloadPlaylists(where, playlists)

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