from rest_framework import serializers
from .models import AdminUser,Teacher,Student
from django.contrib.auth import authenticate
import jwt
from django.conf import settings


#uncomment this if you want to register admin through form like Student and Teacher
'''
class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model=AdminUser
        fields=['username','email','first_name','last_name','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = AdminUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
'''


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model=Teacher
        fields=['username','email','first_name','last_name','password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Teacher.objects.create_teacher(**validated_data)
        user.set_password(password)
        user.save()
        return user



class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Student
        fields=['username','email','first_name','last_name','password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Student.objects.create_student(**validated_data)
        user.set_password(password)
        user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
 
    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)
 
        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)
 
        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        
        #print(jwt.decode(user.token,settings.SECRET_KEY, algorithms=["HS256"]))
    
        return {
            'email': user.email,
            'token': user.token
        }


    