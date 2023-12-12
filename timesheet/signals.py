from django.db.models.signals import pre_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth
import requests
@receiver(pre_save, sender=UserSocialAuth)
def fetch_google_user_info(sender, instance, **kwargs):
    if instance.pk and instance.provider == 'google-oauth2'and instance.user.google_extra_data is None:
        print("Updating UserSocialAuth instance")
        access_token = instance.extra_data.get('access_token')
        if access_token:
            # Make an API call to Google using the access token
            google_user_info = fetch_google_user_data(access_token)
            print(google_user_info)
            if google_user_info:
                # Update the social authentication record with the retrieved user data
                instance.user.google_extra_data = google_user_info


def fetch_google_user_data(access_token):
    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None