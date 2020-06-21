from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Account, Category
from .utils import send_email_confirmation

import uuid

class AccountSignupSerializer(serializers.ModelSerializer):
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

class AccountShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer): 
    users = serializers.SerializerMethodField('get_all_users')
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_all_users(self, obj):
        users = obj.users.all()
        serializer = AccountShowSerializer(users,many=True)
        return serializer.data