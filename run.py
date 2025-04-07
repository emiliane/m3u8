import subprocess

where = 'Work'
rangestart = 37
rangestop = 100
setOfStep = 10

def download(location, rangestart, rangestop):
    tempfolder = location + '/' + str(rangestart) + '-' + str(rangestop - 1)
    mkvfolder = location + '/mkv'
    print(tempfolder, mkvfolder)
    
    subprocess.run('mkdir -p ' + tempfolder, shell=True, check=True, text=True)
    subprocess.run('mkdir -p ' + mkvfolder, shell=True, check=True, text=True)
    
    for x in range(rangestart, rangestop):
        number = "{:05d}".format(x)

        curlts = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_1_' + number + '.ts -o ' + tempfolder +'/'+ number + '.ts'
        curlaac = 'curl https://storage.sardius.media/archives/2153BA7C697A514/events/site_DBF5334817/4/playlist_6_' + number + '.aac -o ' + tempfolder +'/'+ number + '.aac'

        print(curlts)    
        subprocess.run(curlts, shell=True, check=True, text=True)
        print(curlaac)
        subprocess.run(curlaac ,shell=True, check=True, text=True)

    filets = 'ls '+ tempfolder + '/*.ts | sort -V > ' + tempfolder + '/ts.txt'
    fileaac = 'ls '+ tempfolder + '/*.aac | sort -V > ' + tempfolder + '/aac.txt'

    print(filets)
    subprocess.run(filets, shell=True, check=True, text=True)
    print(fileaac)
    subprocess.run(fileaac, shell=True, check=True, text=True)

    ffmpegts = 'ffmpeg -y -f mpegts -i concatf:' + tempfolder + '/ts.txt -c copy ' + tempfolder + '/ts.mkv'
    print (ffmpegts)
    subprocess.run(ffmpegts, shell=True, check=True, text=True)

    ffmpegaac = 'ffmpeg -y -i concatf:' + tempfolder + '/aac.txt -c copy ' + tempfolder + '/aac.mkv'
    print (ffmpegaac)
    subprocess.run(ffmpegaac, shell=True, check=True, text=True)

    ffmpegvideo = 'ffmpeg -y -i ' + tempfolder + '/ts.mkv -i ' + tempfolder + '/aac.mkv -c copy ' + mkvfolder + '/video' + str(rangestart) + '-' + str(rangestop - 1) + '.mkv'
    print (ffmpegvideo)
    subprocess.run(ffmpegvideo, shell=True, check=True, text=True)

    deletetempfolder = 'rm -r ' + tempfolder
    print(deletetempfolder)
    subprocess.run(deletetempfolder, shell=True, check=True, text=True)

for x in range(rangestart, rangestop):
    a = (x) * setOfStep
    b = (x + 1) * setOfStep
    print(x, a, b)

    download(where, a, b)