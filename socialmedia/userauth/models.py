from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime 

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey( User , on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True , default= 0)
    bio = models.TextField(blank=True , default=' ')
    profileimg = models.ImageField(upload_to='profile_image' , default='blank-profile-picture.png')
    location = models.TextField(max_length=100 , blank=True , default=' ')

    def __str__(self):
        return self.user.username 
    



class Post(models.Model):
    # here we Use Uses UUID instead of auto-increment ID
    # beacause UUID is more secure than auto increment (ex :- 550e8400-e29b-41d4-a716-446655440000)
    # default=uuid.uuid4 → auto-generates unique ID
    id = models.UUIDField(primary_key=True , default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_like = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} :- {self.caption}"
    


class LikePost(models.Model):
    post_id = models.CharField(max_length=500 ,null=True, blank=True)
    username = models.CharField(max_length=100 )
    
    def __str__(self):
        return self.username
        
class Followers(models.Model):
    follower = models.CharField(max_length=255)
    user = models.CharField(max_length=100 , default='')

    def __str__(self):
        return f"{self.user} :- {self.follower}"