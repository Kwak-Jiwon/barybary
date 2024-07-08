# tasting_notes/admin.py

from django.contrib import admin
from .models import UserContact,UserResidence

admin.site.register(UserContact)
admin.site.register(UserResidence)
