from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView , RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin

from .serializers import  TeacherSerializer , StudentSerializer , UserLoginSerializer
from .models import  Teacher , Student
from .permissions import IsTeacher,IsTeacherOrAdmin



@api_view(['GET'])
def api_overview(request):
    Teacher_Student={

            'To get list of Teacher  REQUEST-TYPE = GET                 '  :                '/list-teacher/',
            'Adding a teacher  REQUEST-TYPE = POST                      '  :                '/register-teacher/',
            'To get list of Student  REQUEST-TYPE = GET                 '  :                '/list-teacher/',
            'Adding a student  REQUEST-TYPE = POST                      '  :                '/register-student/',
            'Detail of single student  REQUEST-TYPE = GET               '  :                '/detail-student/',

    }
    
    
    url_list={
        'ENDPOINTS FOR Teacher and stuent                               '  :                 Teacher_Student ,
        'ADMIN PANEL                                                    '  :                 '/admin/',
        'LOGIN                                                          '  :                 'accounts/login/',
        'Forget password                                                '  :                 '/password-reset/',
        

                                                                     
    }
    return Response(url_list)









# In Case we want to register AdminUser through the form just uncomment this

'''
class AdminUserAPIView(CreateAPIView):
    serializer_class=AdminUserSerializer
    queryset=AdminUser.objects.all()

    def perform_create(self,serializer):
        serializer.save()
'''

#This view is used to register user and get a list of user only admin user can perform these operation.
class TeacherAPIView(ListCreateAPIView):
    serializer_class=TeacherSerializer
    permission_classes=[IsAdminUser]
    queryset=Teacher.objects.all()



#This view is used to register user and get a list of user  ,adminuser or teacher can perform these operation.
class StudentAPIView(ListCreateAPIView):
    serializer_class=StudentSerializer
    permission_classes=[IsTeacherOrAdmin]
    queryset=Student.objects.all()



#This view is used to get detail of single student,any user  can perform these operation.Although as mentioned if we
# want only student to perform this operation instaed IsAuthenticated just use IsStudent from accounts.permissions
class StudentDetailAPIView(RetrieveAPIView):
    serializer_class=StudentSerializer
    permission_classes=[IsAuthenticated]
    queryset=Student.objects.all()


    def retrieve(self,request, *args, **kwargs):
        instance = self.request.user
        serializer = self.serializer_class(instance)
        return Response(serializer.data)



#This is used as for Login
class UserLoginView(APIView):
    serializer_class=UserLoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)