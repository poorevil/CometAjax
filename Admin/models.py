from django.db import models
from json import JSONEncoder

class Portal(models.Model,JSONEncoder):
    '''
    portal对象
    '''
    name            = models.CharField(max_length=100)      #portal名称
    iconUrl         = models.CharField(max_length=500)      #图标地址
    homepageUrl     = models.CharField(max_length=500)      #主页地址
    
    order           = models.IntegerField()                 #排序号
    
    def __unicode__(self):
        return self.id;
    
    @staticmethod
    def serialize(obj):
        return {
            "id":   obj.id,
            "name": obj.name,
            "iconUrl": obj.iconUrl,
            "homepageUrl": obj.homepageUrl,
        }
        
