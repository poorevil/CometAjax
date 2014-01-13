#-*- coding:UTF-8 -*-
from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.core.cache import cache

from base64 import b64encode
import time,hashlib,qrcode,cStringIO

def scanQRCode(request):
    
    ''' 根据加密算法得出随即UUID '''
    m = hashlib.md5()
    m.update("%f"%time.time())
    uuid = m.hexdigest()
    
    return render_to_response('AuthCenter/templates/regist_scan_qrcode.html', {'uuid': uuid}) 

def renderQRCode(request,uuid):
    '''  用于网页显示二维码  '''
    img = qrcode.make(uuid)
    
    qrCodeImage_File = cStringIO.StringIO()
    img.save( qrCodeImage_File , kind= 'PNG')
    datauri ="data:image/png;base64,%s" % b64encode( qrCodeImage_File.getvalue() )
    qrCodeImage_File.close()
    
    return HttpResponse(datauri)

def registResult(request,uuid):
    '''  用于网页检查客户端扫描结果  '''
    for i in range(0,10):
        loginResult = cache.get(uuid,'null')
        if cmp(loginResult,'null') != 0:
            ''' 
            扫描成功
            web页面跳转至对应的portal绑定页
            '''
            return HttpResponse('''{"result_code":208,"msg":"login succeed！！！"}''', content_type="application/json")
        
        time.sleep(1)

    return HttpResponse('''{"result_code":408,"msg":"lsdfdsfsdgfdg"}''', content_type="application/json")

def clientRegist(request):
    '''  用于客户端绑定账号时，扫描二维码后post的绑定数据   '''
    if request.method == 'POST' :
        
        uuid     = request.POST.get('uuid','')             #二维码内容
        deviceId = request.POST.get('deviceId','')         #设备唯一标识
        portalId = request.POST.get('portalId','')         #当前需要绑定的门户标识
        
        if len(uuid)>0 and len(deviceId)>0 and len(portalId)>0 :
            ''' 
            TODO:1.校验uuid是否合法
            TODO:2.校验deviceId,portalId合法性
            3.将deviceId，portalId保存至memcache中，用于页面跳转至相应portal的账号绑定页面
            '''
        
            registDict = {'uuid':uuid,'deviceId':deviceId,'portalId':portalId}
            cache.set(uuid,registDict,60*5)
            
            return HttpResponse('''{"regist_result":200,"msg":"go to login page"}''', content_type="application/json")
        
    return HttpResponse('''{"regist_result":400,"msg":"regist failed"}''', content_type="application/json")

def bindAccount(request,uuid):
    ''' 
    账号绑定页
    TODO: 
        显示对应的portal logo
        根据后台配置，显示对应的账号绑定表格
    '''
    if len(uuid) > 0 :
        registDict = cache.get(uuid,None)
        if registDict is not None:
            portalId = registDict['portalId']
            print portalId
            '''
            通过portalId从后台中取到对应的绑定所需提交的key-value
            组装form表单内容，写入页面
            '''
    
    
    
    
    return render_to_response('AuthCenter/templates/regist_bind_account.html', {'uuid': uuid}) 
    
    
def bindAccountFormAjaxPost(request):
    '''
    账号绑定页通过Ajax post提交的表单数据
    TODO:
        1.校验uuid是否合法
        1.1.根据uuid从memcached中取到portalId
        2.提交用户名、密码等(根据后台配置，提交对应的账号绑定key-value)到后台认证服务器进行校验
        3.保存uuid、后台认证服务器返回的token串、当前时间等
        4.修改memcached中uuid对应的值
        5.返回绑定结果
    '''
    if request.method == 'POST' :
        uuid = request.POST.get('uuid','')
        if len(uuid) > 0 :
            registDict = cache.get(uuid,None)
            if registDict is not None:
                portalId = registDict['portalId']
                print portalId
                ''' 通过portalId从后台中取到对应的绑定所需提交的key '''
                
                username = request.POST.get('username','')
                pwd = request.POST.get('pwd','')
        #        print '%s    %s'%(username,pwd)
                for i in range(0,5):
                
                    time.sleep(1)
    
    
#    return HttpResponse('''{"result_code":208,"msg":"bind succeed"}''', content_type="application/json")
    
    return HttpResponse('''{"result_code":408,"msg":"bind failed"}''', content_type="application/json")
    