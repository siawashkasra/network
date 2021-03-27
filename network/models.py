from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
    content = models.TextField("Content")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    timestamp = models.DateTimeField(auto_now_add=True)


    def serialize(self):
        
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp,
        }