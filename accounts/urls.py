from django.urls import path
from .views import api_overview, TeacherAPIView , StudentAPIView , StudentDetailAPIView,UserLoginView
from django.contrib.auth.views import PasswordResetView , PasswordResetDoneView ,PasswordResetConfirmView ,PasswordResetCompleteView

urlpatterns = [
    path('',api_overview),
    path('login/',UserLoginView.as_view()),
    #path('register-user',AdminUserAPIView.as_view()),
    path('register-teacher/',TeacherAPIView.as_view()),
    path('register-student/',StudentAPIView.as_view()),
    path('list-teacher/',TeacherAPIView.as_view()),
    path('list-student/',StudentAPIView.as_view()),
    path('detail-student/',StudentDetailAPIView.as_view()),
    path('password-reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

