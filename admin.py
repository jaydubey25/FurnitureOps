from django.contrib import admin
from .models import extendedusers, extendedNgoRequest, extendedNgoAcceptedRequest

# Registration your models here.
admin.site.register(extendedusers)
admin.site.register(extendedNgoRequest)
admin.site.register(extendedNgoAcceptedRequest)