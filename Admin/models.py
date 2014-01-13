from django.db import models
from json import JSONEncoder

class Portal(models.Model,JSONEncoder):
    '''
    portal����
    '''
    name            = models.CharField(max_length=100)      #portal����
    iconUrl         = models.CharField(max_length=500)      #ͼ���ַ
    homepageUrl     = models.CharField(max_length=500)      #��ҳ��ַ
    
    order           = models.IntegerField()                 #�����
    
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
        
