#-*- coding:UTF-8 -*-

from django.shortcuts import render_to_response
from django.http.response import HttpResponse

import time

from base64 import b64encode
import qrcode
import cStringIO

def index(request):
    return render_to_response('testComet/index.html', {'dummy': "stupid"}) 

def stepEventHub(request):
#     conn.send(body=json.dumps({"msg":"server"}),destination="/EventHub", ack='auto')

    for i in range(0,10):
        print 'loop...'
        time.sleep(1)

    return HttpResponse('''{"result_code":200,"msg":"lsdfdsfsdgfdg"}''')

def renderQRCode(request):
    
    img = qrcode.make('k/#newwindow=1&q=html+invisible+element&safe=strict')
    
    qrCodeImage_File = cStringIO.StringIO()
    img.save( qrCodeImage_File , kind= 'PNG')
    datauri ="data:image/png;base64,%s" % b64encode( qrCodeImage_File.getvalue() )
    qrCodeImage_File.close()
    
    return HttpResponse(datauri)
    
    
    
    
    