from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ADMIN = "admin"
    EDITOR = "editor"
    WRITER = "writer"

    ROLE_CHOICES = [
        (ADMIN, "Administrator"),
        (EDITOR, "Editor"),
        (WRITER, "Escritor"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    bio = models.TextField(max_length=500, blank=True)

    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True)

    @property
    def is_writer(self):
        return self.role == self.WRITER

    @property
    def is_editor(self):
        return self.role == self.EDITOR

    def __str__(self):
        role_display = self.get_role_display() if self.role else "Usuario"
        return f"{self.username} - {role_display}"
