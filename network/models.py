from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    likes = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return f"{self.author.username} added a post"

    def serialize_post(self):
        return {
            "post_id": self.id,
            "author": self.author.username,
            "content": self.content,
            "timestamp": self.date_posted,
            "likes": self.likes.all().count()
        }


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_follower")

    def __str__(self):
        return f"{self.user.username} has a new follower: {self.follower}"
        
        
class Like(models.Model):
    LIKE_FIELDS = (
        ("Like", "Like"),
        ("Unlike", "Unlike"),
    )
    #  Use who 'likes' the post
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    # Post 'liked'
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    # like timestamp
    created = models.DateTimeField(auto_now_add=True)
    # like/unlike field
    field = models.CharField(choices=LIKE_FIELDS, max_length=8)

    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"

    # serialiser method to use with the fetch API
    def serialize(self):
        return {
            "field": self.field,
            "likes": self.post.likes.all().count()
        }





    


