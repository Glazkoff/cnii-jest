from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_interface.models import Theme
from .models import CustomUser


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = User
#     list_display = ['email', 'username', ]


admin.site.register(CustomUser)
admin.site.unregister(Theme)

admin.site.site_header = "Админпанель системы ЦНИИ Русского жестового языка"
admin.site.site_title = "Админпанель ЦНИИ Русского жестового языка"
admin.site.index_title = "Административная часть сайта ЦНИИ Русского жестового языка"
