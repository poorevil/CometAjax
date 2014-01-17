#-*- coding:UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http.response import HttpResponse

from testComet.models import Slider
from Admin.models import Portal,UserInfo

import json,sys

def sliderList(request):
    
    jsonstr = '[]'
    
    try:
        appidParam = request.GET.get('appid','')
        if appidParam is not None and appidParam != '':
#             print appidParam
            result_list = list(Slider.objects.filter(appid=appidParam).order_by('order'))
            jsonstr = json.dumps(result_list, default=Slider.serialize)
    except :
        print sys.exc_info()[0]
        pass
    
    return HttpResponse(jsonstr, content_type="application/json")

def portalList(request):
    ''' portal 列表 '''
    jsonstr = '[]'
    
    try:
        appidParam = request.GET.get('appid','')                            #客户端标识
        deviceIdParam = request.GET.get('deviceId','')                           #设备标识
        if len(appidParam)>0  and len(deviceIdParam)>0:
#             print appidParam
            result_list = list(Portal.objects.order_by('order'))   #appid=appidParam
            
            jsonDictList = [];
            
            for p in result_list:
                jsonDict = p.serialize(p)
                try:
                    userInfo = UserInfo.objects.filter(portal=p,deviceId=deviceIdParam)
                    if userInfo is not None and len(userInfo)>0:
                        jsonDict['isRegisted'] = True
                    else:
                        jsonDict['isRegisted'] = False
                except :
                    jsonDict['isRegisted'] = False
                    pass
                
                jsonDictList.append(jsonDict)
            
            
            jsonstr = json.dumps(jsonDictList)
    except :
        print sys.exc_info()[0]
        pass
    
    return HttpResponse(jsonstr, content_type="application/json")
        