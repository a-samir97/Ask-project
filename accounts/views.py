from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from .models import Account
from .serializers import AccountSignupSerializer
from .utils import send_email_confirmation, send_email_password_reset

import uuid

class AccountCreateViewAPI(CreateAPIView):
    queryset = Account
    serializer_class = AccountSignupSerializer
    permission_classes = (AllowAny,)

@api_view(['POST'])
@permission_classes((AllowAny,))
def loginAPI(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # check if username or password is none
    if username is None or password is None:
        return Response({
            'error': 'please provide both username and password'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # if username and password exists ...
    # authenticate username and password
    user = authenticate(username=username, password=password)

    # if authencation failed ...
    if not user:
        return Response({
            'error' : 'Invalid Credentials',
            },
            status=status.HTTP_404_NOT_FOUND
        )
    # if authencation passes ...
    # generate token for the authenticated user ..
    user_token, created = Token.objects.get_or_create(user=user)
    # if new token is generated for the user 
    if created:
        # return generated token and OK response
        return Response(
                {
                'token': user_token.key
                },
            status=status.HTTP_200_OK
            )
    # if token already exists ..
    else:
        # delete the current token 
        user.auth_token.delete()
        # generate a new token for the user 
        token = Token.objects.create(user=user)
        # return token key with response 200 ok
        return Response({'token': token.key}, status=status.HTTP_200_OK)

@api_view(['POST'])
def LogoutAPI(request):
    # if requested user is authenticated ...
    if request.user.is_authenticated \
        and request.auth \
        and request.user:
        # delete token's user
        request.user.auth_token.delete()
        # return HTTP_200_OK
        return Response(status=status.HTTP_200_OK)

    # i think it will not happen
    # but to make sure we can handle this
    # if requested user is not authenticated ...
    else:
        # return bad request
        return Response({
            'error': 'you are not login'
        },
        status=status.HTTP_400_BAD_REQUEST)

# confirm email
@api_view(['POST'])
@permission_classes((AllowAny,))
def confirm_email(request, user_uuid):

    username = request.data.get('username')
    password = request.data.get('password')

    # check if username or password is none
    if username is None or password is None:
        return Response({
            'error': 'please provide both username and password'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # if username and password exists ...
    # authenticate username and password
    user = authenticate(username=username, password=password)

    # if authencation failed ...
    if not user:
        return Response({
            'error' : 'Invalid Credentials',
            },
            status=status.HTTP_404_NOT_FOUND
        )
    # check if the requested user has uuid ...
    if user.confirm_email_token == user_uuid:
        # user now has confirmed his email
        user.confirmed = True
        # remove uuid from user
        user.confirm_email_token = None
        # save model after editting
        user.save()
        # return Response 200 OK
        return Response(status=status.HTTP_200_OK)

    # if the requested user has not uuid ...
    else:
        return Response({

                'error': "this is something wrong"
            },
            status=status.HTTP_400_BAD_REQUEST
    )

# - PasswordResetView sends the mail
@api_view(['POST'])
@permission_classes((AllowAny,))
def password_reset(request):
    # get email from requested data
    email = request.data.get('email')

    # we need to check if email exists or not ...
    if Account.objects.filter(email=email).exists():
        # get the user by email
        user = Account.objects.filter(email=email).first()
        # generate token to the user
        user.reset_password_token = uuid.uuid4()
        # save user model
        user.save()
        # send mail to the user, to confirm reset the passwor
        send_email_password_reset(user, request)
        # return HTTP 200 OK
        return Response(status=status.HTTP_200_OK)
        # if email is not exist ...
    else:
        # return HTTP 404 NOT_FOUND
        return Response({
                'error' : 'email is not valid.'
            },
            status=status.HTTP_404_NOT_FOUND
        )

# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
@api_view(['POST'])
@permission_classes((AllowAny,))
def password_reset_confirm(request, user_uuid):
    # check if the requested user has uuid
    if request.user.reset_password_token and \
        request.user.reset_password_token == user_uuid:
        # get the requested data
        password = request.data.get('password')
        # set the new password
        request.user.set_password(password)
        # set the uuid of the user to be null
        request.user.reset_password_token = None
        # save user model after editting
        request.user.save()
        # return response  ( 201 or 200 )?
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({
            'error': "there is something wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
