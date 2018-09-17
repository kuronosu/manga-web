from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class MyUserAdmin(UserAdmin):
    model = User
    fieldsets = [
        ("General", {"fields": [
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'avatar',
            'password'
        ]}),
        # ("Details", {"fields": ["description", "creation_date"], "classes": ["collapse"]})
    ]

admin.site.register(User, MyUserAdmin)