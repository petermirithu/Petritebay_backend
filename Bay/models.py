from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class profile(models.Model):
  '''
  profile info table
  '''
  user=models.OneToOneField(User, on_delete=models.CASCADE)
  profile_pic=CloudinaryField('image',blank=True,null=True)  
  phone_no=models.CharField(max_length=15,blank=True)
  password_reset=models.BooleanField(default=False)
  def __str__(self):
    return str(self.user)
