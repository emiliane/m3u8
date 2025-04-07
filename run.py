import subprocess
from datetime import datetime

where = 'Dowload'

numberOfZero = 5
numberParts = 10000

rangestart = 5553
rangestop = 5555
setOfStep = 10

dt = datetime.now()
ts = datetime.timestamp(dt)
where = where + '/' + str(ts)

def myrunsubprocess(command):
    print('Run command:', command)
    try:
        subprocess.run(command, shell=True, check=True, text=True)
    except:
        print("Something went wrong!")

def downloadAll(location, rangestart, rangestop, playlist, extension):
    tempfolder = location + '/All/' + str(rangestart) + '-' + str(rangestop - 1)
    mkvfolder = location + '/All/mkv'
    print(tempfolder, mkvfolder)
    
    myrunsubprocess('mkdir -p ' + tempfolder)
    myrunsubprocess('mkdir -p ' + mkvfolder)
    
    for x in range(rangestart, rangestop):
        number = "{:05d}".format(x)

        curl = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/' + playlist + '_' + number + '.' + extension + ' -o ' + tempfolder +'/'+ number + '.ts'

        myrunsubprocess(curl)

    file = 'ls '+ tempfolder + '/*.ts | sort -V > ' + tempfolder + '/' + extension + '.txt'

    print(file)
    myrunsubprocess(file)

    ffmpegts = 'ffmpeg -y -f mpegts -i concatf:' + tempfolder + '/' + extension + '.txt -c copy ' + tempfolder + '/ts.mkv'
    print (ffmpegts)
    myrunsubprocess(ffmpegts)

    deletetempfolder = 'rm -r ' + tempfolder
    print(deletetempfolder)
    myrunsubprocess(deletetempfolder)


    tempfolder = location + '/' + str(rangestart) + '-' + str(rangestop - 1)
    mkvfolder = location + '/mkv'
    print(tempfolder, mkvfolder)
    
    myrunsubprocess('mkdir -p ' + tempfolder)
    myrunsubprocess('mkdir -p ' + mkvfolder)
    
    for x in range(rangestart, rangestop):
        number = "{:05d}".format(x)

        curlts = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_1_' + number + '.ts -o ' + tempfolder +'/'+ number + '.ts'
        curlaac = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_6_' + number + '.aac -o ' + tempfolder +'/'+ number + '.aac'

        myrunsubprocess(curlts)
        myrunsubprocess(curlaac)

    filets = 'ls '+ tempfolder + '/*.ts | sort -V > ' + tempfolder + '/ts.txt'
    fileaac = 'ls '+ tempfolder + '/*.aac | sort -V > ' + tempfolder + '/aac.txt'

    print(filets)
    myrunsubprocess(filets)
    print(fileaac)
    myrunsubprocess(fileaac)

    ffmpegts = 'ffmpeg -y -f mpegts -i concatf:' + tempfolder + '/ts.txt -c copy ' + tempfolder + '/ts.mkv'
    print (ffmpegts)
    myrunsubprocess(ffmpegts)

    ffmpegaac = 'ffmpeg -y -i concatf:' + tempfolder + '/aac.txt -c copy ' + tempfolder + '/aac.mkv'
    print (ffmpegaac)
    myrunsubprocess(ffmpegaac)

    ffmpegvideo = 'ffmpeg -y -i ' + tempfolder + '/ts.mkv -i ' + tempfolder + '/aac.mkv -c copy ' + mkvfolder + '/video' + str(rangestart) + '-' + str(rangestop - 1) + '.mkv'
    print (ffmpegvideo)
    myrunsubprocess(ffmpegvideo)

    deletetempfolder = 'rm -r ' + tempfolder
    print(deletetempfolder)
    myrunsubprocess(deletetempfolder)

def downloadGroupedNew(location, rangestop, rangestart=0, step=5, clear=False):
    print('Download at' ,location, 'from', rangestart, 'to', rangestop, 'grouped by', step)

    newrangestart = int(rangestart // step)
    newrangestop = int(rangestop // step) + 1

    for x in range(newrangestart, newrangestop):
        a = (x) * step
        b = (x + 1) * step

        tempfolder = location + '/temp/' + str(a) + '-' + str(b - 1)
        mkvfolder = location + '/mkv'
        
        myrunsubprocess('mkdir -p ' + tempfolder)
        myrunsubprocess('mkdir -p ' + mkvfolder)

        for x in range(a, b):
            if (x > rangestop):
                break
            elif (x >= rangestart):
                numberZero = '{:0'+ str(numberOfZero) + 'd}'
                number = numberZero.format(x)

                curlts = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_1_' + number + '.ts -o ' + tempfolder +'/'+ number + '.ts'
                curlaac = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_6_' + number + '.aac -o ' + tempfolder +'/'+ number + '.aac'

                myrunsubprocess(curlts)
                myrunsubprocess(curlaac)

        filets = 'ls '+ tempfolder + '/*.ts | sort -V > ' + tempfolder + '/ts.txt'
        fileaac = 'ls '+ tempfolder + '/*.aac | sort -V > ' + tempfolder + '/aac.txt'

        myrunsubprocess(filets)
        myrunsubprocess(fileaac)

        ffmpegts = 'ffmpeg -y -f mpegts -i concatf:' + tempfolder + '/ts.txt -c copy ' + tempfolder + '/ts.mkv'
        myrunsubprocess(ffmpegts)

        ffmpegaac = 'ffmpeg -y -i concatf:' + tempfolder + '/aac.txt -c copy ' + tempfolder + '/aac.mkv'
        myrunsubprocess(ffmpegaac)

        ffmpegvideo = 'ffmpeg -y -i ' + tempfolder + '/ts.mkv -i ' + tempfolder + '/aac.mkv -c copy ' + mkvfolder + '/video' + str(rangestart) + '-' + str(rangestop - 1) + '.mkv'
        myrunsubprocess(ffmpegvideo)

        deletetempfolder = 'rm -r ' + tempfolder
        if clear:
            myrunsubprocess(deletetempfolder)

downloadGroupedNew(where, rangestop, rangestart)
