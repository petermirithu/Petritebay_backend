from rest_framework import serializers
from .models import profile,products,cart,orderedItem,sessions,dogWalking,dogGrooming,petSitting
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')
    
class profileSerializer(serializers.ModelSerializer):
  '''
  convert profile to json
  '''
  class Meta:
    model=profile
    depth=1
    fields=("id","user","profile_pic","phone_no")

class productsSerializer(serializers.ModelSerializer):
  '''
  convert products object to json 
  '''
  class Meta:
    model=products
    depth = 1
    fields=('id','name','image','description','price')

class orderedItemSerializer(serializers.ModelSerializer):
  '''
  convert ordered items to json
  '''
  class Meta:
    model=orderedItem
    depth=2     
    exclude=("user",)

class cartSerializer(serializers.ModelSerializer):
  '''
  convert cart items to json
  '''        
  class Meta:
    model=cart
    depth=3   
    exclude=("user",)
    
class dogWalkingSerializer(serializers.ModelSerializer):
  class Meta:
    model=dogWalking
    depth=1
    exclude=("user",)

class dogGroomingSerializer(serializers.ModelSerializer):
  class Meta:
    model=dogGrooming
    depth=1
    exclude=("user",)

class petSittingSerializer(serializers.ModelSerializer):
  class Meta:
    model=petSitting
    depth=1
    exclude=("user",)
    