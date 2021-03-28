from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField("First Name", max_length=200)
    last_name = models.CharField("Last Name", max_length=200)



class Post(models.Model):
    content = models.TextField("Content")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    timestamp = models.DateTimeField(auto_now_add=True)


    def serialize(self):
        
        return {
            "id": self.id,
            "user": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "content": self.content,
            "timestamp": self.timestamp,
        }