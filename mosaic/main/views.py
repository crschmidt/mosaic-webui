# Create your views here.
from main.models import *

def req(request, rid=None):
    if request.method == "POST":
        bbox = request.POST['bbox']
        r = Request(bbox)
        r.save()
        return HttpResponseRedirect("/req/%s/" % r.id)
    if rid:
        r = Request.objects.get(pk=rid)
        return render_to_response("request.html", {'request': r})
        
        
