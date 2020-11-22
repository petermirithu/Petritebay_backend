from django.contrib import admin
from .models import profile,cart,products,orderedItem,sessions,dogGrooming,dogWalking,petSitting
# Register your models here.
admin.site.register(profile)
admin.site.register(cart)
admin.site.register(products)
admin.site.register(orderedItem)
admin.site.register(sessions)
admin.site.register(dogWalking)
admin.site.register(dogGrooming)
admin.site.register(petSitting)

