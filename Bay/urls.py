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
  url(r'^api/products/$',views.productListView.as_view()),      
  url(r'^api/add_to_cart/$',views.add_to_cart),
  path('api/remove_from_cart/<int:user_id>/<int:product_id>',views.remove_from_cart),
  path('api/cart/<int:user_id>',views.get_user_Cart),
  path('api/pastOrders/<int:user_id>',views.get_past_orders),
  url(r'api/confirmOrder/$',views.confirm_order),
  url(r'api/confirmBooking/$',views.confirm_booking),
  path('api/getBookings/<int:user_id>',views.get_bookings),
]