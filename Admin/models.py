from django.db import models
from json import JSONEncoder

class Portal(models.Model,JSONEncoder):
    '''
    portal对象
    '''
#     @property (nonatomic,retain) NSString *pid;             //唯一标识
# @property (nonatomic,retain) NSString *name;            //名称
# @property (nonatomic,assign) NSTimeInterval lastLogin;  //最后登录时间
# @property (nonatomic,retain) NSString *iconFileName;    //图标
    
    
    name            = models.CharField(max_length=100)      #portal名称
    iconUrl         = models.CharField(max_length=500)      #图标地址
    homepageUrl     = models.CharField(max_length=500)      #主页地址
    
    order           = models.IntegerField()                 #排序号
    
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