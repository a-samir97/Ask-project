from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

#from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token

from .models import Account
from .serializers import AccountSerializer
from .utils import send_email_confirmation, send_email_password_reset

import uuid

class AccountCreateViewAPI(CreateAPIView):
    queryset = Account
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)

@csrf_exempt
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
    user_token = Token.objects.create(user=user)
    # return generated token and OK response
    return Response(
            {
            'token': user_token.key
            },
        status=status.HTTP_200_OK
        )

@api_view(['GET'])
def LogoutAPI(request):
    # if requested user is authenticated ...
    if request.user.is_authenticated and request.auth and request.user:
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
    if user.uuid == user_uuid:
        # user now has confirmed his email
        user.confirmed = True
        # remove uuid from user
        user.uuid = None
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
@csrf_exempt
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
        user.uuid = uuid.uuid4()
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

# - PasswordResetDoneView shows a success message for the above
@api_view(['GET'])
def password_reset_done(request):
    # if request user has uuid
    if  request.user.uuid:
        return Response({
            "success": "Email has been sent to you, Please check your email"
            },
            status=status.HTTP_200_OK
        )
    # if requested user has not uuid field
    else:
        return Response({
            'error' : 'please there is an error, please try to reset your email again'
        },
        status=status.HTTP_400_BAD_REQUEST
    )

# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def password_reset_confirm(request, user_uuid):
    # check if the requested user has uuid
    if request.user.uuid:
        # get the requested data
        password = request.data.get('password')
        password_confirmation = request.data.get('password-confirmation')
        # check if password equal password-confirmation
        if password == password_confirmation:
            # set the new password
            request.user.set_password(password)
            # set the uuid of the user to be null
            request.user.uuid = None
            # save user model after editting
            request.user.save()
            # return response  ( 201 or 200 )?
            return Response(status=status.HTTP_200_OK)
        # if password  not equal password_confirmation
        else:
            return Response({
                'error' : "Password does not mathc password confirmation"
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'error': "there is something wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
