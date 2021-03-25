
# Credicxo Teacher - Student

This project is based on Django Rest framework and Uses the JWT Token Authentications.



## Steps to run the API:

1. Install requirements.txt 
2. Run- python manage.py makemigrations
3. Run- python manage.py migrate
4. Run- python manage.py runserver 



## API-OVERVIEW

Now enter http://127.0.0.1:8000/ in your Browser this will give the details about the functionality offered.
To perform any of the operations mentioned just add the corresponding relative url to this http://127.0.0.1:8000/ .

***Note : All the authorization details is mentioned in the documentations.***


### Registering a ADMIN

We can only register admin through the Django admin panel. To acces Django Admin panel you have to create a superuser
Follows these steps to register an ADMIN user:
1. python manage.py createsuperuser
2. Fill all details(username ,email and pasword)
3. Now got to http://127.0.0.1:8000/admin/ and login through the credentials you just entered.
4. Register admin through the USERS section(please tick the is_staff then only you will be considered as ADMIN)


### Forgot Password

In case you want to use forgot password.This api uses the default reset password mechanism provided by django.
To be able to send email just add the email and password through which you want to send email into your environment 
variables , then go to your gmail less secure apps and allows less secure apps.Now Understand the process:<br>
1.  Go to http://127.0.0.1:8000/reset-password/ and enter the email.
2. If email is valid ,a link will be sent to you the email you entered,click on the link.
3. Now it will ask to enter password and confirm password .
4. After that a page will come to with a link to login.



To get details about other endpoints read the documentation at [docs](https://documenter.getpostman.com/view/14584052/TzCHBVW7).
