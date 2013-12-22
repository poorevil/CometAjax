#-*- coding:UTF-8 -*-

from django.shortcuts import render_to_response
from django.http.response import HttpResponse

from base64 import b64encode
import qrcode
import cStringIO
import time
import hashlib

from django.core.cache import cache

def index(request):
    
    ''' 根据加密算法得出随即UUID '''
    m = hashlib.md5()
    m.update("%f"%time.time())
    uuid = m.hexdigest()
    
    print time.time()
    
    return render_to_response('testComet/index.html', {'uuid': uuid}) 

def loginResult(request,uuid):
    for i in range(0,10):
        
        loginResult = cache.get(uuid,'null')
        print loginResult
        if cmp(loginResult,'null') != 0:
            ''' 
            登录成功
            TODO:设置session
            '''
            cache.delete(uuid)
            
            return HttpResponse('''{"result_code":208,"msg":"login succeed！！！"}''')
        
        time.sleep(1)

    return HttpResponse('''{"result_code":408,"msg":"lsdfdsfsdgfdg"}''')

def renderQRCode(request,uuid):
    
    img = qrcode.make(uuid)
    
    qrCodeImage_File = cStringIO.StringIO()
    img.save( qrCodeImage_File , kind= 'PNG')
    datauri ="data:image/png;base64,%s" % b64encode( qrCodeImage_File.getvalue() )
    qrCodeImage_File.close()
    
    return HttpResponse(datauri)
    
def clientLogin(request):
    
    if request.method == 'POST' :
        
        uuid = request.POST.get('uuid')
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        
        print username
        print pwd
        
        ' check username and password'
        if cmp(username,'evil') == 0 and cmp(pwd,'evil') == 0 :
            cache.set(uuid,'login succeed',30)
            
            return HttpResponse('''{"login_result":200,"msg":"login succeed"}''')
        
    return HttpResponse('''{"login_result":400,"msg":"login failed"}''')
    
    
    
    