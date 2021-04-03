from django.contrib import admin
from django.contrib.gis import admin
from qlcayxanh.models import *
from django.db import models
from django.contrib.auth.models import AbstractUser
from leaflet.admin import LeafletGeoAdmin
# Register your models here.
class cayxanhleaflet(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (15.5629911, 108.4835256),
        }


admin.site.register(loaicay)
admin.site.register(nhanvien)
admin.site.register(ranh_gioi)
admin.site.register(duonggiaothong,LeafletGeoAdmin)
# admin.site.register(cayxanh)
admin.site.register(cayxanh,cayxanhleaflet, 
    settings_overrides =  {
        'DEFAULT_CENTER': (15.5629911, 108.4835256),
        'DEFAULT_ZOOM': 10,
        'TILES': [('','//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png','')],
    })