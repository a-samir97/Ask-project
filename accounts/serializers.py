from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Account
from .utils import send_email_confirmation

import uuid

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={
        'input_type': 'password'
        },

        label='Password'
    )

    class Meta:
        model = Account
        fields = (
                'username', 'email', 'password',
                'gender', 'birthdate'
            )

    def create(self, validated_data):
        new_account = Account(
            username=validated_data['username'],
            email=validated_data['email'],
            gender=validated_data['gender'],
            birthdate=validated_data['birthdate']
        )
        new_account.set_password(validated_data['password'])
        new_account.uuid = uuid.uuid4()
        new_account.save()
        send_email_confirmation(new_account, self.context['request'])
        return new_account
