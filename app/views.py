from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, JsonResponse
from .camera import VideoCamera
import json

camera = VideoCamera()  

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def livefe(request):
    try:
        return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  
        pass

def index(request, *args, **kwargs):
    return render(request, 'index.html')

def get_emotions(request):
    emotions = camera.get_emotions() 
    return JsonResponse(emotions)
