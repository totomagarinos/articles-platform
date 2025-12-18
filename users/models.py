from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  ADMIN = "admin"
  EDITOR = "editor"
  WRITER = "writer"
  READER = "reader"

  ROLE_CHOICES = [
    (ADMIN, "Administrador"),
    (EDITOR, "Editor"),
    (WRITER, "Escritor"),
    (READER, "Lector"),
  ]

  role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=READER)

  def __str__(self):
    return f"{self.username} - {self.get_role_desplay()}"
