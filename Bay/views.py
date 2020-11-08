from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializer import profileSerializer
from .models import profile
from django.contrib.auth.models import User
from rest_framework import viewsets,status
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
import json
from rest_framework import pagination
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
import re
from django.http import HttpResponse,JsonResponse
from requests.auth import HTTPBasicAuth
import requests
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
import uuid 
from django.contrib.auth.decorators import permission_required
from .email import send_us_a_message

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getprofile(request, user_id):
  user_info=User.objects.get(id=int(user_id))  
  profile_info=profile.objects.get(user=user_info)  
  serialised_profile=profileSerializer(profile_info,many=False)      
  serialised_profile.data["user"].pop('password')    
  serialised_profile.data["user"].pop('last_login')    
  serialised_profile.data["user"].pop('is_superuser')    
  serialised_profile.data["user"].pop('is_staff')    
  serialised_profile.data["user"].pop('groups')    
  serialised_profile.data["user"].pop('user_permissions')    
  serialised_profile.data["user"].pop('is_active')              
  return Response(serialised_profile.data)  

@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request,format=None):    
  data=json.loads(request.body)
  profile_id=data["id"]
  phone_no=data["phone_no"]
  user_id=data["user"]["id"]
  email=data["user"]["email"]
  firstname=data["user"]["first_name"]
  lastname=data["user"]["last_name"]

  profile_info=profile.objects.get(id=int(profile_id))
  profile_info.phone_no=phone_no
  profile_info.save()    
  
  user_data=User.objects.get(id=int(user_id))
  user_data.email=email
  user_data.first_name=firstname
  user_data.last_name=lastname
  user_data.save()

  return Response('Updated',status=status.HTTP_200_OK)    

@csrf_exempt
@permission_classes([])
@api_view(['POST'])  
def send_message(request,format=None):  
  data=json.loads(request.body)
  name=data["name"]
  subject=data["subject"]
  message=data["message"]
  email=data["email"]
  
  try:
    validate_email(email)
    send_us_a_message(name,email,subject,message)          
    return Response('Successfully received message',status=status.HTTP_200_OK)              

  except ValidationError:
    return Response('Please use a real email or try again a sending message',status=status.HTTP_400_BAD_REQUEST)        