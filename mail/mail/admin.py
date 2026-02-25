from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Email)


# Register your models here.
