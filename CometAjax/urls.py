#-*- coding:UTF-8 -*-
from django.conf.urls import patterns, include, url
import os
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CometAjax.views.home', name='home'),
    # url(r'^CometAjax/', include('CometAjax.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    (r'^$', 'testComet.views.index'),
    (r'^loginresult/(?P<uuid>[\w\d]{0,50})/$', 'testComet.views.loginResult'),
    (r'^renderQRCode/(?P<uuid>[\w\d]{0,50})/$', 'testComet.views.renderQRCode'),
    (r'^clientLogin$', 'testComet.views.clientLogin'),
    
#    接口部分 
    (r'^sliderList$', 'interface.views.sliderList'),
    
#    注册部分
    (r'^regist/scanqrcode/$', 'AuthCenter.views.scanQRCode'),
    (r'^regist/registResult/(?P<uuid>[\w\d]{0,50})/$', 'AuthCenter.views.registResult'),
    (r'^regist/renderQRCode/(?P<uuid>[\w\d]{0,50})/$', 'AuthCenter.views.renderQRCode'),
    (r'^regist/clientRegist$', 'AuthCenter.views.clientRegist'),
    (r'^regist/bindAccount/(?P<uuid>[\w\d]{0,50})/$', 'AuthCenter.views.bindAccount'),
    (r'^regist/bindAccountFormAjaxPost/$', 'AuthCenter.views.bindAccountFormAjaxPost'),
    
    
    (r'^(?P<path>.*)$', 'django.views.static.serve'
     ,{'document_root': PROJECT_PATH+'/testComet/static', 'show_indexes': False}),
)

urlpatterns += staticfiles_urlpatterns() 
