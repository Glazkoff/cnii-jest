from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    """Форма для создания новых пользователей. Включает все обязательные поля, плюс повторение пароля"""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'birthday')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не соврпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    list_display = ('email', 'birthday', 'name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('date_of_birth',)}),
        ('Разрешения', {'fields': ('is_admin',)}),
    )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'date_of_birth', 'password1', 'password2'),
    #     }),
    # )
    # search_fields = ('email',)
    # ordering = ('email',)
    # filter_horizontal = ()

    class Meta:
        model = User
        fields = ('email', 'password', 'birthday',
                  'is_active')


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
