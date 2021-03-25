from django.contrib import admin
from .models import AdminUser,Teacher,Student
from django.contrib.auth.admin import UserAdmin
from .forms import AdminChangeForm,AdminCreationForm,NonAdminChangeForm,NonAdminCreationForm




class AdminUserAdmin(UserAdmin):
    form = AdminChangeForm
    add_form = AdminCreationForm

    list_display = ('email' , 'password',  'is_staff','is_active' ,'is_superuser')
    list_filter = ('is_superuser','is_teacher')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ( 'is_teacher', 'is_staff', 'is_superuser')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name')}),
        ('Personal info', {'fields': ('is_teacher','is_staff', 'is_superuser',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email','username')
    ordering = ('email',)
    filter_horizontal = ()


#In comparison to the AdminUser ,in this we dont have is_staff,is_superuser field as we dont want to give authority to the user that
# by any mistake he/she can a make a teaacher or student as admin or staff.
class NonAdminUserAdmin(UserAdmin):
    form = NonAdminChangeForm
    add_form = NonAdminCreationForm

    list_display = ('email' , 'password',  'is_active' ,'is_teacher','first_name','last_name',)
    list_filter = ('is_teacher',)

    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name',)}),
        ('Personal info', {'fields': ( 'is_teacher',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name',)}),
        ('Personal info', {'fields': ('is_teacher',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email','username')
    ordering = ('email',)
    filter_horizontal = ()






admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(Teacher,NonAdminUserAdmin)
admin.site.register(Student,NonAdminUserAdmin)


