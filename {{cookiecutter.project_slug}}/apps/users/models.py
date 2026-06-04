import os
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from .validators import validate_avatar


def avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"avatars/{uuid.uuid4().hex}{ext}"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    first_name = None
    last_name = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True,
        blank=True,
        validators=[validate_avatar],
    )

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/images/user.svg"

    def __str__(self):
        return f"{self.user.email} - profile"

    def delete_avatar(self):
        if self.avatar:
            if os.path.isfile(self.avatar.path):
                os.remove(self.avatar.path)
            self.avatar = None
            self.save(update_fields=["avatar"])