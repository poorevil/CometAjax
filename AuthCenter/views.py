#-*- coding:UTF-8 -*-
from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.core.cache import cache
# from django.core.exceptions import ObjectDoesNotExist

from Admin.models import *

from base64 import b64encode
import time,hashlib,qrcode,cStringIO,requests,json

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

def clientTestRegistResult(request,uuid):
    '''  用于客户端检查客户端扫描结果  '''
    for i in range(0,10):
        registDict = cache.get(uuid,None)
        if registDict is not None:
            registedStatus = registDict['registed']
            if registedStatus!=None and registedStatus == True:
                ''' 绑定成功 '''
                return HttpResponse('''{"result_code":208,"msg":"regist succeed","accessToken":"%s"}'''%registDict['accessToken'], 
                                    content_type="application/json")
            
        time.sleep(1)

    return HttpResponse('''{"result_code":408,"msg":"registing wait"}''', content_type="application/json")

def registResult(request,uuid):
    '''  用于网页检查客户端扫描结果  '''
    for i in range(0,10):
        loginResult = cache.get(uuid,None)
        if loginResult is not None:
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
            portalObj = None
            userInfo = None
            try:
                portalObj = Portal.objects.get(id=portalId)
                userInfo = UserInfo.objects.get(portal=portalId)
            except:
                pass
            
            if userInfo is not None and portalObj is not None:
                ''' TODO:登录操作 '''
                interfaceUrl = portalObj.registInterfaceUrl         #TODO:登录接口url地址
                response = None
                
                registParamDict = {'deviceId':deviceId,'accessToken':userInfo.token}
                if cmp('post',portalObj.registInterfaceFormAction.lower()) == 0:
                    response = requests.post(interfaceUrl, data=registParamDict, timeout = 50, allow_redirects = False)
                else :
                    response = requests.get(interfaceUrl, params=registParamDict, timeout = 50, allow_redirects = False)
                
                content = response.text
                
                if content is not None and len(content) > 0:
                    resultDict = json.loads(content)                #返回结果
                    resultCode = resultDict['resultCode']           #响应码
                    if cmp(resultCode.lower(),'success') == 0:
                        ''' 登录成功 '''
                        return HttpResponse('''{"regist_result":201,"msg":"login succeed"}''', content_type="application/json")
                        
                    else:
                        ''' 登录失败 '''
                        return HttpResponse('''{"regist_result":401,"msg":"login failed"}''', content_type="application/json")
                
            else:
            
                ''' 
                TODO:1.校验uuid是否合法
                TODO:2.校验deviceId,portalId合法性
                3.将deviceId，portalId保存至memcache中，用于页面跳转至相应portal的账号绑定页面
                '''
            
                registDict = {'uuid':uuid,'deviceId':deviceId,'portalId':portalId,'registed':False,'accessToken':''}
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
#             print portalId
            '''
            通过portalId从后台中取到对应的绑定所需提交的key-value
            组装form表单内容，写入页面
            '''
            portalObj = None
            try:
                portalObj = Portal.objects.get(id=portalId)
                
                registKVList = list(PortalRegistKVDetail.objects.filter(portal=portalObj).order_by('order'))
            
    #             for kvDetail in registKVList :
    #                 print 'key:%s  valuetype:%s'%(kvDetail.key,kvDetail.valueType)
                dict = {'uuid': uuid,'registKVList':registKVList}
                return render_to_response('AuthCenter/templates/regist_bind_account.html', dict) 
            except :
                portalObj = None
    
    return render_to_response('AuthCenter/templates/regist_error.html') 
    
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
#             根据uuid从memcached中取到portalId
            registDict = cache.get(uuid,None)
            if registDict is not None :
                registStatus = registDict['registed']
                
                if registStatus == True:
                    return HttpResponse('''{"result_code":308,"msg":"this account already binded"}''', content_type="application/json")
                
                portalId = registDict['portalId']
#                 print portalId
                ''' 通过portalId从后台中取到对应的绑定所需提交的key '''
                portalObj = None
                try:
                    portalObj = Portal.objects.get(id=portalId)
                except :
                    portalObj = None
                
                if portalObj is not None :
                    registKVList = list(PortalRegistKVDetail.objects.filter(portal=portalObj).order_by('order'))
                    
                    if len(registKVList) > 0:
                        registParamDict = {}        #提交后台验证中心的键值对字典
                        for kvDetail in registKVList :
                            '''
                                TODO:
                                    1.此处比较后期改为码表，比较id，可以用switch来判断
                                    2.后期需要支持单选框、多选框、下拉框等
                            '''
                            if cmp('text',kvDetail.valueType) == 0 or cmp('password',kvDetail.valueType) == 0:
                                registParamDict[kvDetail.key] = request.POST.get(kvDetail.key,'')
                                print 'key:%s  valuetype:%s'%(kvDetail.key,kvDetail.valueType)
                    
                        ''' 
                            提交后台接口进行账号绑定
                            接口要求，返回json格式数据，格式必须包含如下内容：
                            {"resultCode":"success","accessToken":"asdfsdfdsfsdf"}
                        '''
                        interfaceUrl = portalObj.registInterfaceUrl         #绑定接口url地址
                        response = None
                        if cmp('post',portalObj.registInterfaceFormAction.lower()) == 0:
                            response = requests.post(interfaceUrl, data=registParamDict, timeout = 50, allow_redirects = False)
                        else :
                            response = requests.get(interfaceUrl, params=registParamDict, timeout = 50, allow_redirects = False)
                        
                        content = response.text
                        
                        if content is not None and len(content) > 0:
                            resultDict = json.loads(content)                #返回结果
                            resultCode = resultDict['resultCode']           #响应码
                            if cmp(resultCode.lower(),'success') == 0:
                                accessToken = resultDict['accessToken']     #绑定账号对应的token
                                print 'accessToken  %s'%accessToken
                                ''' 保存token '''
                                userInfo = UserInfo()
                                userInfo.token = accessToken
                                userInfo.portal = portalObj
                                userInfo.deviceId = registDict['deviceId']
                                #用户其他信息...
                                userInfo.save()
                                
                                ''' 修改memcached中uuid对应的注册状态为True '''
                                registDict['registed'] = True
                                registDict['accessToken'] = accessToken
                                cache.set(uuid,registDict,60*5)
                                
                                return HttpResponse('''{"result_code":208,"msg":"bind succeed"}''', content_type="application/json")
        
    return HttpResponse('''{"result_code":408,"msg":"bind failed"}''', content_type="application/json")
    