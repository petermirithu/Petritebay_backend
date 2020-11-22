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

class products(models.Model):
  name=models.CharField(max_length=500)
  image=CloudinaryField('image',blank=True,default='')    
  description=models.CharField(max_length=1000, blank=True)  
  price=models.DecimalField(decimal_places=2,max_digits=100)    

  def __str__(self):
    return self.name  

class orderedItem(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)  
  product = models.ForeignKey(products, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=0)  
  units_price=models.DecimalField(max_digits=100,decimal_places=2,default=0)
  date=models.DateTimeField(auto_now_add=True)  
  ordered=models.BooleanField(default=False)          
  finished_payment=models.BooleanField(default=False)

  def __str__(self):
      return str(self.product)


class cart(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)  
  products=models.ManyToManyField(orderedItem,blank=True)  
  total=models.DecimalField(decimal_places=2,max_digits=100,default=0)
  date=models.DateTimeField(auto_now=True)      
  receipt_no=models.CharField(default='',max_length=100)
  phone_no=models.CharField(default='',max_length=20)  
  ordered=models.BooleanField(default=False)          
  finished_payment=models.BooleanField(default=False)
  deliveryInfo=models.TextField(blank=True)

  def __str__(self):        
    return str(self.user)    

class dogWalking(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)  
  dogSize=models.CharField(max_length=1000)
  hours=models.IntegerField(default=0)
  unit=models.DecimalField(decimal_places=2,max_digits=100,default=0)
  cost=models.DecimalField(decimal_places=2,max_digits=100,default=0)
  date=models.DateTimeField(null=True)
  deliveryInfo=models.TextField(blank=True)
  serviced=models.BooleanField(default=False)

  def __str__(self):
    return str(self.user)

class sessions(models.Model):
  name=models.CharField(max_length=1000)

  def __str__(self):
    return str(self.name)

class dogGrooming(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)  
  dogBreed=models.CharField(max_length=1000)
  cost=models.DecimalField(decimal_places=2,max_digits=100,default=0)
  sessions=models.ManyToManyField(sessions,blank=True)
  date=models.DateTimeField(null=True)
  deliveryInfo=models.TextField(blank=True)
  serviced=models.BooleanField(default=False)

  def __str__(self):
    return str(self.user)

class petSitting(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)  
  dogBreed=models.CharField(max_length=1000)
  days=models.IntegerField(default=0)
  unit=models.DecimalField(decimal_places=2,max_digits=100,default=0)
  cost=models.DecimalField(decimal_places=2,max_digits=100,default=0)
  date=models.DateTimeField(null=True)
  deliveryInfo=models.TextField(blank=True)
  serviced=models.BooleanField(default=False)
  
  def __str__(self):
    return str(self.user)
