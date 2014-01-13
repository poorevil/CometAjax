from django.db import models
from json import JSONEncoder

class Portal(models.Model,JSONEncoder):
    '''
    portal����
    '''
#     @property (nonatomic,retain) NSString *pid;             //Ψһ��ʶ
# @property (nonatomic,retain) NSString *name;            //����
# @property (nonatomic,assign) NSTimeInterval lastLogin;  //����¼ʱ��
# @property (nonatomic,retain) NSString *iconFileName;    //ͼ��
    
    
    name            = models.CharField(max_length=100)      #portal����
    iconUrl         = models.CharField(max_length=500)      #ͼ���ַ
    homepageUrl     = models.CharField(max_length=500)      #��ҳ��ַ
    
    order           = models.IntegerField()                 #�����
    
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