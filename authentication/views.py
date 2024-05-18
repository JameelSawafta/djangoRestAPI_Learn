from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import AuthSerializer ,LoginSerializer,RequestPasswordResetEmailSerializer,SetNewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = AuthSerializer

    def post(self,request:Request):
        userData = request.data
        serializer = self.serializer_class(data= userData)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=serializer.data.get('email'))

        token = RefreshToken.for_user(user=user)

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token.access_token)
        email_body = 'Hi '+user.username+' Use the link below to verify your email \n'+absurl

        data = {
            'subject':'Verify your email',
            'email_body':email_body,
            'to_email':user.email
        }
        Util.sendEmail(data)

        return Response(serializer.data,status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):


    def get(self,request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer


    def post(self,request:Request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']

        if get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink  = reverse('password-reset-confirm', kwargs={'uidb64':uidb64,'token':token})
            link = 'http://'+current_site+relativeLink
            email_body = 'Hello, \n Use the link below to reset your password \n'+link
            data = {
                'subject':'Password Reset',
                'email_body':email_body,
                'to_email':user.email
            }
            Util.sendEmail(data)
        return Response({'success':'We have sent you a link to reset your password'},status=status.HTTP_200_OK)



class PasswordTokenCheckAPI(generics.GenericAPIView):

    def get(self,request,uidb64,token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user=user,token=token):
                return Response({'error':'Token is not valid, please request a new one'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True,'message':'Credentials Valid','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error':'Token is not valid, please request a new one'},status=status.HTTP_401_UNAUTHORIZED)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self,request:Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Password reset success'},status=status.HTTP_200_OK)


