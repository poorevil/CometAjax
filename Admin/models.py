#-*- coding:UTF-8 -*-
from django.db import models
from json import JSONEncoder

class Portal(models.Model,JSONEncoder):
    '''
    portal对象
    '''
    name                = models.CharField(max_length=100)      #portal名称
    iconUrl             = models.CharField(max_length=500)      #图标地址
    homepageUrl         = models.CharField(max_length=500)      #主页地址
    registInterfaceUrl  = models.CharField(max_length=500)      #账号绑定接口地址
    registInterfaceFormAction = models.CharField(max_length=10)      #账号绑定接口地址提交方式
    
    order               = models.IntegerField()                 #排序号
    
    def __unicode__(self):
        return self.id;
    
    @staticmethod
    def serialize(obj):
        return {
            "id":   obj.id,
            "name": obj.name,
            "iconUrl": obj.iconUrl,
            "homepageUrl": obj.homepageUrl,
            "registInterfaceUrl": obj.registInterfaceUrl,
        }
        
class UserInfo(models.Model,JSONEncoder):
    '''
    已绑定账户的用户信息
    '''
    token           = models.CharField(max_length=100)      #访问内网的token
    portal          = models.ForeignKey(Portal)             #对应的portal
    deviceId        = models.CharField(max_length=100)      #设备唯一标识
    
    #用户其他信息
    name            = models.CharField(max_length=100)      #姓名
    #datetime。。。等等
    
    def __unicode__(self):
        return self.id;
    
    @staticmethod
    def serialize(obj):
        return {
            "id":   obj.id,
            "token": obj.token,
            "portal": obj.portal.serialize(),
            "deviceId": obj.deviceId,
            "name": obj.name,
        }
    
class PortalRegistKVDetail(models.Model,JSONEncoder):
    '''
    portal账号绑定时需要的键值对信息
    用于：
        1.生成账号绑定页面的form表单
        2.账号绑定页面提交时，对后台portal认证接口提交键值对的对应信息
        
        TODO:需要扩展valueType字段，对应挂上码表，支持多种值类型，如：下拉列表，单选，多选等
    '''
    portal                  = models.ForeignKey(Portal)             #对应的portal
    key                     = models.CharField(max_length=100)      #键名(用于提交接口的英文名)
    valueType               = models.CharField(max_length=100)      #值类型
    keyHumanReadableName    = models.CharField(max_length=100)      #键名称(用于页面form表单显示，中文)
    keyHelpMessage          = models.CharField(max_length=250)      #提示信息(用于页面form表单显示，中文)
    
    order                   = models.IntegerField()                 #排序号
    
