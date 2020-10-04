from urllib.request import urlopen

from django.core.files.base import ContentFile
from social_core.exceptions import AuthForbidden
from authapp.models import ShopClientProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    print(response)
    if backend.name == "google-oauth2":
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopclientprofile.gender = ShopClientProfile.MALE
            else:
                user.shopclientprofile.gender = ShopClientProfile.FEMALE

        if 'tagline' in response.keys():
            user.shopclientprofile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.shopclientprofile.aboutMe = response['aboutMe']

        if 'picture' in response.keys():
            if not user.avatar:
                url = response['picture']
                user.avatar.save(f'avatar_{user.username}.jpg', ContentFile(urlopen(url).read()))

        if 'ageRange' in response.keys():
            min_age = response['ageRange']['min']
            if int(min_age) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.save()
