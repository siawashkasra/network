from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    first_name = models.CharField("First Name", max_length=200)
    last_name = models.CharField("Last Name", max_length=200)




    def get_initials(self):
        return self.first_name [:1] + self.last_name [:1]




    def get_full_name(self):
        return self.first_name + " " + self.last_name



    def serialize(self):

         return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }




    def has_liked(self):
        # print(self.users.filter(user_id=self.id))
        return True




class Post(models.Model):
    content = models.TextField("Content")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    timestamp = models.DateTimeField(auto_now_add=True)




    def serialize(self):
        
        return {
            "id": self.id,
            "author": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp,
        }




    def has_been_liked(self):
        return list(self.posts.values_list('user_id', flat=True))


    def like_count(self):
        return self.posts.filter(post_id=self.id).count();




class Following(models.Model):
    follower_id = models.ManyToManyField(User, related_name="followers")
    followed_id = models.ManyToManyField(User, related_name="followeds")



class Like(models.Model):
    user_id = models.ManyToManyField(User, related_name="users")
    post_id = models.ManyToManyField(Post, related_name="posts")


