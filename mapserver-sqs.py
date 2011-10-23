import urllib
import os
import sys
import json
import time

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
            target = os.path.join(opts.dest, target)
            if os.path.exists(target):
                continue
            meter = urlgrabber.progress.text_progress_meter()
            print >>sys.stderr, image.path, "->", target
            urlgrabber.urlgrab(str(image.path), target, progress_obj=meter)
        else:
            print >>sys.stderr, image.path, "->", target
        files.append(target)
    return files


def run(bbox):

    parser = oam.option_parser("%prog [options]")
    parser.add_option("-s", "--source", dest="source", action="store_true", default=None, help="Include raw imagery sources")
    parser.add_option("-o", "--output", dest="vrt", default=None, help="Output VRT filename")
    parser.add_option("-d", "--destination", dest="dest", default=None, help="Destination directory for image downloads")
    opts, args = parser.parse_args([])
    
    opts.dest = "/mnt/data/images"
    client = oam.build_client(opts)
    files = fetch_image_files(client, bbox, opts)
    out = {}
    for image in client.images_by_bbox(bbox):
        res = min(image.px_width, image.px_height)
        out[image.path] = res
    
    l = sorted(out.items(), key=lambda x: x[1])
    out = {'images':[]}
    if opts.dest:
        f = open("/mnt/data/2.map", "w")
        f.write("""MAP\nWEB\nMETADATA\n"ows_enable_request" "*"\nEND\nEND\nPROJECTION\n"init=epsg:4326"\nEND\n""")
        for item in l:
            path = item[0].split("/")[-1]
            out['images'].append(path) 
            f.write("""LAYER\nNAME "%s" \n STATUS ON \n DATA "/mnt/data/images/%s" \n TYPE RASTER \n END\n""" % (path, path))
        f.write("END")
    print json.dumps(out)
if __name__ == "__main__":
    from boto.sqs.connection import SQSConnection
    conn = SQSConnection('', '')
    q = conn.get_queue("mosaic")
    messages = q.get_messages()
    while True:
        messages = q.get_messages()
	print messages
        if messages:
            print "Running message"
            message = messages[0]
            q.delete_message(message)
            try:
                body = message.get_body()
                bbox = body.split(",")
                run(map(float, bbox))
            except KeyboardInterrupt:
                print "Caught ctrl-c; stopping"
                q.write(message)
		sys.exit()
            except:
                print "Request failed; putting message back on queue."
                q.write(message)
	
        else:
            print "Sleeping for 10 seconds"
            time.sleep(10)
       
