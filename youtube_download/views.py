from django.shortcuts import render, redirect
# pytube package for Download youtube video
from pytube import YouTube
import os
import threading

# Create your views here.
url = ''

class Complete(threading.Thread):
    def __init__(self, url, res, homedir):
        self.url = url
        self.res = res
        self.homedir = homedir
        threading.Thread.__init__(self)
    def run(self):
        YouTube(self.url).streams.get_by_resolution(self.res).download(self.homedir + '/Downloads')
        

def ytb_down(request):
    return render(request,'ytb_main.html')

def yt_download(request):
    global url
    url = request.GET.get('url')
    # Create object for know which video download ..
    try:
        obj = YouTube(url)
        resolutions = []
        strm_all = obj.streams.filter(progressive = True, file_extension = 'mp4').all()
        for i in strm_all:
            resolutions.append(i.resolution)
        resolutions = list(dict.fromkeys(resolutions))

        embed_link = url.replace("watch?v=", "embed/")
        path = "D:\\"

        return render(request,'yt_download.html',{'rsl': resolutions, 'embd': embed_link })

    except:
        return render(request, 'Sorry Internet is Down')


def download_complete(request,res):
    global url
    homedir = os.path.expanduser("~")
    # dirs = homedir + '/Downloads'
    # print(f'Direct: ', f'{dirs}/Downloads')
    if request.method == 'POST':
        Complete(url, res, homedir).start()
        # YouTube(url).streams.get_by_resolution(res).download(homedir + '/Downloads')
        return render (request, 'download_complete.html')
    else:
        return render(request, 'sorry.html')