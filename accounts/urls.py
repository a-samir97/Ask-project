from django.urls import path

from .views import (
            AccountCreateViewAPI,
            loginAPI,
            LogoutAPI,
            confirm_email,
            password_reset,
            password_reset_confirm
        )

app_name = 'accounts'


urlpatterns =  [
    path('', AccountCreateViewAPI.as_view(),name='RegisterAPI'),
    path('login/', loginAPI, name='LoginAPI'),
    path('logout/', LogoutAPI, name='LogoutAPI'),
    path('confirm/email/<uuid:user_uuid>/', confirm_email, name='ConfirmEmail'),
    path('password/reset/', password_reset, name='PasswordReset'),
    path('password/reset/confirm/<uuid:user_uuid>/', password_reset_confirm, name='PasswordResetConfirm'),

]
