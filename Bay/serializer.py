from rest_framework import serializers
from .models import profile
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