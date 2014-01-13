#-*- coding:UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http.response import HttpResponse

from testComet.models import Slider

import json,sys

def sliderList(request):
    
    jsonstr = '[]'
    
    try:
        appidParam = request.GET.get('appid','')
        if appidParam is not None and appidParam != '':
            print appidParam
            result_list = list(Slider.objects.filter(appid=appidParam).order_by('order'))
            jsonstr = json.dumps(result_list, default=Slider.serialize)
    except :
        print 'aaaaaaa'
        print sys.exc_info()[0]
        pass
    
    return HttpResponse(jsonstr, content_type="application/json")
        