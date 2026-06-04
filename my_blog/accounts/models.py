from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=False,blank=False)
    messeage = models.TextField(max_length = 100)
    image = models.ImageField(upload_to="image/", height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile/", height_field=None, width_field=None, max_length=None,null = True,blank = True)
    dob = models.DateField( null = True,blank = True,auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.user.username