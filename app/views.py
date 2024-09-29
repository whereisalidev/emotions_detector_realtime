from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from .camera import *
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  
        pass

def index(request, *args, **kwargs):
    return render(request, 'index.html')