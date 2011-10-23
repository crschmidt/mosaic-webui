# Create your views here.
from main.models import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

@csrf_exempt
def req(request, rid=None):
    if request.method == "POST":
        bbox = request.POST['bbox']
        r = Request(bbox=bbox)
        r.save()
        return HttpResponseRedirect("/request/%s/" % r.id)
    if rid:
        r = Request.objects.get(pk=rid)
        return render_to_response("request.html", {'request': r})
        
def new(request):
    return render_to_response("ui.html")
