from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.


class Hashtag(models.Model):
    content = models.TextField(unique=True)
    def __str__(self):
        return self.content
    
    
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts',blank=True)
    hashtags = models.ManyToManyField(Hashtag ,blank=True)
    
    content = models.TextField()
    def __str__(self):
        return self.content
        
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = ProcessedImageField(blank=True ,
                                processors=[ResizeToFill(600, 600)],
                                upload_to='posts')
                                
                                
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    

                                
                                

