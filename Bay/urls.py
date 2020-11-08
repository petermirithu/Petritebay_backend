from django.conf.urls import url
from . import views
from django.urls import path,include
from rest_framework import routers
from . import views
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token


urlpatterns = [  
  # auth  
  path('auth/',include('rest_auth.urls')),
  path(r'auth/signup/', include('rest_auth.registration.urls')),    
  path(r'api-token-refresh/',refresh_jwt_token),          

  path('api/profile/<int:user_id>',views.getprofile),
  url(r'api/updateprofile/$',views.update_profile),
  url(r'api/send_message/$',views.send_message),
]