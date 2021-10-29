from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.forms import ValidationError


class YourVisionNowSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email_domain = user_email(sociallogin.user).split("@")[1]
        if email_domain is not 'gmail.com' or 'yourvisionnow.com':
            raise ValidationError('Please log in with a Google account that ends \
                                  with "@gmail.com" or "@yourvisionnow.com". You \
                                  may have to log out of your current Gmail account. \
                                  Try again at <a href="./">Your Vision Now</a>')
