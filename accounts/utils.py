from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_confirmation(user, request):
    subject = "Account Confirmation"
    html_message = render_to_string('confirmation_email.html', {'user': user, 'request': request})
    plain_message = strip_tags(html_message)
    from_email = "a.samir9710@gmail.com"
    to_email = user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

def send_email_password_reset(user, request):
    subject = "Reset Password"
    html_message = render_to_string('reset_password.html', {'user' : user, 'request': request})
    plain_message = strip_tags(html_message)
    from_email = 'a.samir9710@gmail.com'
    to_email = user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
