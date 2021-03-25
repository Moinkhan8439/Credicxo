import jwt
import time
from django.utils.timezone import timedelta
from datetime import datetime
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import AdminUser
 



#This is our default authentication backend ,it is called whenever we want to authenticate through a jwt token
class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'
    

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication. 
 
        `authenticate` has two possible return values:
 
        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.
 
        2) `(user, token)` - We return a user/token combination when 
                             authentication is successful.
 
                            If neither case is met, that means there's an error 
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed` 
                            exception and let Django REST Framework
                            handle the rest.
        """
        request.user = None
 
        # `auth_header` should be an array with two elements: 1) the name of
        # the authentication header (in this case, "Token") and 2) the JWT 
        # that we should authenticate against.
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
 
        if not auth_header:
            return None
 
        if len(auth_header) == 1:
            # Invalid token header. No credentials provided. Do not attempt to
            # authenticate.
            return None
 
        elif len(auth_header) > 2:
            # Invalid token header. The Token string should not contain spaces. Do
            # not attempt to authenticate.
            return None
 
        #spliting the authorization header in "token" and actual_token
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')


        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)
    

    def _authenticate_credentials(self, request, token):
        try:
            #payload is our data whatever we encode in our case its email and the datetime in secs we are using
            #the pyjwt library of python to encode and decode the jwt token.Here we will get error the token is somehow modified 
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms = ["HS256"])
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)
        
        #Here we check if the email mentioned in payload matches with any user or not
        try:
            user = AdminUser.objects.get(email=payload['email'])
        except AdminUser.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        #To check the if the token is expired we compared the expiry on the token with current datetime.
        payload_exp=payload['exp']
        new=datetime.now()
        now=time.mktime(new.timetuple())
        if int(now) > int(payload_exp):
            msg = 'Your token has been expired!!'
            raise exceptions.AuthenticationFailed(msg)

        #this checks if the user is still active 
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)
        
        return (user, token)



