import urllib
import os
import sys
import json

import urlgrabber, urlgrabber.progress
import oam

def fetch_image_files(client, bbox, opts):
    # if opts.layer:
    #    path = str(opts.layer)
    #    if not opts.test and not os.path.isdir(path):
    #        os.makedirs(path)
    # else:
    files = []
    args = {"archive":"true"} if opts.source else {}
    for image in client.images_by_bbox(bbox, **args):
        target = image.path.split("/")[-1]
        if opts.dest:
            meter = urlgrabber.progress.text_progress_meter()
            target = os.path.join(opts.dest, target)
            print >>sys.stderr, image.path, "->", target
            urlgrabber.urlgrab(str(image.path), target, progress_obj=meter)
        else:
            print >>sys.stderr, image.path, "->", target
        files.append(target)
    return files


parser = oam.option_parser("%prog [options]")
parser.add_option("-s", "--source", dest="source", action="store_true", default=None, help="Include raw imagery sources")
parser.add_option("-o", "--output", dest="vrt", default=None, help="Output VRT filename")
parser.add_option("-d", "--destination", dest="dest", default=None, help="Destination directory for image downloads")
opts, args = parser.parse_args()

imgid = sys.argv[1]
u = urllib.urlopen("http://oam.osgeo.org/api/image/%s/" % imgid)
imgdata = json.load(u)
bbox = imgdata['bbox']
client = oam.build_client(opts)
files = fetch_image_files(client, bbox, opts)
out = {}
for image in client.images_by_bbox(bbox):
    res = min(image.px_width, image.px_height)
    out[image.path] = res

l = sorted(out.items(), key=lambda x: x[1])
if opts.dest:
    f = open("%s/ordered.txt" % (opts.dest), "w")
    for item in l:
        f.write('%s\n' % item[0].split("/")[-1])
print "cd %s; for i in `cat ordered.txt`; do gdaltindex oam.shp $i; done" % opts.dest
print "wget https://github.com/oam/oam/raw/master/accesstools/oammapserver/oam.map"
print "shp2img -i image/jpeg -m oam.map -e %s -l oam -s %s %s -o out.jpg" % (" ".join(map(str, imgdata['bbox'])), imgdata['width'], imgdata['height']) 
