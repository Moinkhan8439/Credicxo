from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import AdminUser


class AdminCreationForm(forms.ModelForm):

    class Meta:
        model = AdminUser
        fields = ('email','is_staff','is_teacher', 'is_superuser','password','first_name','last_name')


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AdminChangeForm(forms.ModelForm):
    
    class Meta:
        model = AdminUser
        fields = ('email', 'password','is_teacher', 'is_active','first_name','last_name' ,'is_superuser')



class NonAdminCreationForm(forms.ModelForm):

    class Meta:
        model = AdminUser
        fields = ('email','is_staff','is_teacher', 'password','first_name','last_name')


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class NonAdminChangeForm(forms.ModelForm):
    
    class Meta:
        model = AdminUser
        fields = ('email', 'password','is_teacher', 'is_active','first_name','last_name' )
