#-*- coding:UTF-8 -*-

from django.db import models

from json import JSONEncoder

class Slider(models.Model,JSONEncoder):
    '''
    幻灯片对象
    '''
#    @property (nonatomic,retain) NSString *sid;
#@property (nonatomic,retain) NSString *title;
#@property (nonatomic,retain) NSString *openUrl;
#@property (nonatomic,retain) NSString *imageUrl;
    sid             = models.CharField(max_length=20,unique=True)   #用于排重
    title           = models.CharField(max_length=100)
    openUrl         = models.CharField(max_length=500)
    imageUrl        = models.CharField(max_length=500)
    appid           = models.CharField(max_length=20)               #所属软件
    order           = models.IntegerField()
    
    def __unicode__(self):
        return self.sid;
    
    @staticmethod
    def serialize(obj):
        return {
            "sid":   obj.sid,
            "title": obj.title,
            "openUrl": obj.openUrl,
            "imageUrl": obj.imageUrl,
        }