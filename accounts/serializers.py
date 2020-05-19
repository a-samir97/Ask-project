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
    password2 = serializers.CharField(style={
        'input_type': 'password'
        },

        label='Password confirmation',

        write_only=True,
    )


    class Meta:
        model = Account
        fields = (
                'username', 'email', 'password',
                'password2', 'sex', 'birthday'
            )

    def create(self, validated_data):
        # check if the password equal the password confirmation

        if  validated_data['password'] == validated_data['password2']:
            new_account = Account(
                username=validated_data['username'],
                email=validated_data['email'],
                sex=validated_data['sex'],
                birthday=validated_data['birthday']
            )
            new_account.set_password(validated_data['password'])
            new_account.uuid = uuid.uuid4()
            new_account.save()
            send_email_confirmation(new_account, self.context['request'])
            return new_account
        else:
            raise ValidationError("password confirmation should equal password.")
