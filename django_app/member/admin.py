from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from member.models import MyUser, CeleryTest


class MyUserAdmin(UserAdmin):
    pass


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(CeleryTest)
