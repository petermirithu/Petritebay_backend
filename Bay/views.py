from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializer import profileSerializer,cartSerializer,UserSerializer,productsSerializer,orderedItemSerializer,dogGroomingSerializer,dogWalkingSerializer,petSittingSerializer
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
from .email import send_us_a_message,send_user_order_receipt,user_made_order
from .models import products,cart,orderedItem,profile,sessions,dogWalking,dogGrooming,petSitting
from rest_framework.generics import ListAPIView,RetrieveAPIView

# Create your views here.
class productListView(ListAPIView):
  queryset=products.objects.all()        
  serializer_class=productsSerializer
  permission_classes=[]

@api_view(['POST','PUT'])  
@permission_classes([IsAuthenticated])
def add_to_cart(request,format=None):    
  data=json.loads(request.body)
  user_id=data["user_id"]
  product_id=data["product_id"]
  quantity=data["quantity"]

  if int(quantity)==0:
    return Response("Quantity can't be zero",status=status.HTTP_400_BAD_REQUEST)  
  else:
    try:
      db_product=products.objects.get(id=int(product_id))          
      user_info=User.objects.get(id=int(user_id))
      try:
        user_cart=cart.objects.get(user=user_info, ordered=False,finished_payment=False)        
        user_prods=user_cart.products.all()
        listed_items=[]
        for prod in user_prods:
          listed_items.append(prod.product.name)

        if db_product.name in listed_items:
          sub_total=db_product.price*int(quantity)

          prev_order=orderedItem.objects.get(product=db_product,ordered=False,finished_payment=False,user=user_info)
          prev_order.quantity+=int(quantity)
          prev_order.units_price+=sub_total
          prev_order.save()

          user_cart.total+=sub_total
          user_cart.save()
          return Response('Successfully updated the item in cart',status=status.HTTP_200_OK)
        else:
          new_order=orderedItem(product=db_product,quantity=int(quantity),user=user_info)
          new_order.save()

          new_order_f=orderedItem.objects.get(product=db_product,ordered=False,finished_payment=False,user=user_info)

          x_sub_total=db_product.price*int(quantity)
          new_order_f.units_price+=x_sub_total
          user_cart.products.add(new_order_f.id)
          user_cart.total+=x_sub_total
          new_order_f.save()
          user_cart.save()
          return Response('Successfully added item to cart',status=status.HTTP_201_CREATED)

      except cart.DoesNotExist:
        f_sub_total=db_product.price*int(quantity)


        new_cart=cart(user=user_info,total=f_sub_total)
        new_cart.save()

        new_order_x=orderedItem(product=db_product,user=user_info,quantity=quantity,units_price=f_sub_total)            
        new_order_x.save()

        new_order_f2=orderedItem.objects.get(product=db_product,ordered=False,finished_payment=False,user=user_info)
        new_user_cart=cart.objects.get(user=user_info, ordered=False,finished_payment=False)        
        new_user_cart.products.add(new_order_f2.id)              
        new_user_cart.save()

        return Response('Successfully added item to cart',status=status.HTTP_201_CREATED)
          
    except products.DoesNotExist:
      return Response('Product you picked does not exist',status=status.HTTP_204_NO_CONTENT)  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_Cart(request,user_id):  
  try:
    user_info=User.objects.get(id=user_id)
    try:    
      user_cart=cart.objects.get(user=user_info,ordered=False,finished_payment=False)          
      serialised_cart=cartSerializer(user_cart)            
      for user_y in serialised_cart.data["products"]:
        user_y.pop('user')                           
      return Response(serialised_cart.data)                                
    except cart.DoesNotExist:
      return Response('You have no cart',status=status.HTTP_204_NO_CONTENT)
  except User.DoesNotExist:
      return Response('User does not exist',status=status.HTTP_404_NOT_FOUND)

@api_view(['POST','DELETE'])  
@permission_classes([IsAuthenticated])
def remove_from_cart(request,user_id,product_id):  
  user_info=User.objects.get(id=int(user_id))  
  db_product=products.objects.get(id=int(product_id))
  user_cart=cart.objects.get(user=user_info,ordered=False,finished_payment=False)
  item_ordered=orderedItem.objects.get(user=user_info,product=db_product,ordered=False,finished_payment=False)
  
  costed=db_product.price*item_ordered.quantity
  items_in_cart=user_cart.products.all()
  if len(items_in_cart)==1:
    user_cart.total=0
    user_cart.products.remove(item_ordered.id)
    user_cart.save()
    item_ordered.delete()
    return Response('Removed item from cart',status=status.HTTP_200_OK)
  else:
    new_cost=user_cart.total-costed  
    user_cart.total=new_cost
    user_cart.products.remove(item_ordered.id)
    user_cart.save()
    item_ordered.delete()
    return Response('Removed item from cart',status=status.HTTP_200_OK)    

@api_view(['POST'])  
@permission_classes([IsAuthenticated])
def confirm_order(request,format=None):  
  data=json.loads(request.body)
  user_id=data["user_id"]
  phone_no=data["phoneno"]
  email=data["email"].strip()
  deliveryInfo=data["deliveryInfo"]

  try:
    user_info=User.objects.get(id=int(user_id))
    user_cart=cart.objects.get(user=user_info,ordered=False,finished_payment=False)                        
    orders=orderedItem.objects.filter(user=user_info,ordered=False,finished_payment=False)
    receipt_no=uuid.uuid4().hex[:6].upper()    
    acc_ref=str(user_info.username)+str(receipt_no)
    if user_cart.receipt_no==acc_ref:
      receipt_no_new=uuid.uuid4().hex[:6].upper()    
      acc_ref=str(user_info.username)+str(receipt_no_new)
    if user_cart.receipt_no!=acc_ref:                  
      try:
        validate_email(email)
        send_user_order_receipt(user_info.username,email,orders,acc_ref,user_cart.total)
        user_made_order(user_info.username,email,phone_no,orders,acc_ref,user_cart.total)
        user_cart.ordered=True        
        user_cart.receipt_no=acc_ref          
        user_cart.deliveryInfo=deliveryInfo
        user_cart.phone_no=phone_no
        user_cart.user.email=email
        user_cart.user.save()
        user_cart.save()    
        user_products=user_cart.products.all()        
        for prod in user_products:
          prod.ordered=True                    
          prod.save()                                          
        return Response('Successfully received your order. We shall get back you later.',status=status.HTTP_201_CREATED)        
      except ValidationError:
        return Response('Please use a real email',status=status.HTTP_400_BAD_REQUEST)              
    else:  
      return Response('Error generating receipt',status=status.HTTP_400_BAD_REQUEST)          

  except User.DoesNotExist:
    return Response('User with that id not found',status=status.HTTP_404_NOT_FOUND)        



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_past_orders(request,user_id):  

  try:
    user_info=User.objects.get(id=user_id)
    try:    
      user_cart=cart.objects.filter(user=user_info,ordered=True)          
      serialised_cart=cartSerializer(user_cart,many=True)            
      for order in serialised_cart.data:
        for user_x in order["products"]:
          user_x.pop('user')    
                      
      return Response(serialised_cart.data)                                
    except cart.DoesNotExist:
      return Response('You have no past order',status=status.HTTP_204_NO_CONTENT)
  except User.DoesNotExist:
      return Response('User does not exist',status=status.HTTP_404_NOT_FOUND)

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

@api_view(['POST'])  
def confirm_booking(request,format=None):  
  vardogWalking=None
  vardogGrooming=None
  varpetSitting=None
  data=json.loads(request.body)
  placeInfo=data["placeInfo"]  
  bookingDate=data["date"]
  user_id=data["user_id"]  
  if 'dogWalking' in data:
    vardogWalking=data["dogWalking"]
  if 'dogGrooming' in data:
    vardogGrooming=data["dogGrooming"]
  if 'petSitting' in data:
    varpetSitting=data["petSitting"]


  user_info=User.objects.get(id=int(user_id))  
  foundSessions=sessions.objects.all()

  if vardogWalking != None:    
    walkingObj=dogWalking(user=user_info,dogSize=vardogWalking["dog_size"],
                          hours=vardogWalking["hours"],unit=vardogWalking["unit"],cost=vardogWalking["cost"],
                          date=bookingDate,deliveryInfo=placeInfo)
    walkingObj.save()

  if vardogGrooming != None:
    groomingObj=dogGrooming(user=user_info,dogBreed=vardogGrooming["dog_breed"],cost=vardogGrooming["cost"],date=bookingDate,deliveryInfo=placeInfo)
    groomingObj.save()
    queryObj=dogGrooming.objects.get(user=user_info,serviced=False,dogBreed=vardogGrooming["dog_breed"],cost=vardogGrooming["cost"],date=bookingDate,deliveryInfo=placeInfo)

    for item in foundSessions:
      if item.name in vardogGrooming["sessions"]:
        queryObj.sessions.add(item.id)

    queryObj.save()        

  if varpetSitting != None:
    sittingObj=petSitting(user=user_info,dogBreed=varpetSitting["dog_breed"],days=varpetSitting["days"],
                          unit=varpetSitting["unit"],cost=varpetSitting["cost"],date=bookingDate,deliveryInfo=placeInfo)    
    sittingObj.save()

  return Response('Successfully booked the services. We shall contact you soon.',status=status.HTTP_200_OK)        

@api_view(['GET'])  
def get_bookings(request,user_id):  
  user_info=User.objects.get(id=int(user_id))  
  walkings=None
  groomings=None
  sittings=None  
  walkings=dogWalking.objects.filter(user=user_info)
  groomings=dogGrooming.objects.filter(user=user_info)
  sittings=petSitting.objects.filter(user=user_info)
  serialised_walkings=dogWalkingSerializer(walkings,many=True)            
  serialised_groomings=dogGroomingSerializer(groomings,many=True)
  serialised_sittings=petSittingSerializer(sittings,many=True)
  payload={'walking':serialised_walkings.data,'grooming':serialised_groomings.data,'sitting':serialised_sittings.data}
  return Response(payload)  

