from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    # user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to="user_image/%Y/%m/%d", null=True, blank=True)

    def get_image(self):
        try:
            pass
        except Exception as e:
            print(e)
            return f"https://avatars.dicebear.com/api/bottts/:{self.username}.svg"
