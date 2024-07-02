from django.contrib import admin
from .models import Accounts, Roles, UserSignupStatus, Addresses, EquipmentCategory, EquipmentInventory, EquipmentDetails, EquipmentReservations, Reservations, ReservationStatus 

# Register your models here.
admin.site.register(Accounts)
admin.site.register(Roles)
admin.site.register(UserSignupStatus)
admin.site.register(Addresses)
admin.site.register(EquipmentCategory)
admin.site.register(EquipmentInventory)
admin.site.register(EquipmentDetails)
admin.site.register(EquipmentReservations)
admin.site.register(Reservations)
admin.site.register(ReservationStatus)