from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse


USER_MODEL = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=2500)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='chto.png', upload_to='profile_pics')
    pdf = models.FileField(null="true", upload_to="blog/uploads")
    tag = models.CharField(max_length=20, null=True, default='без тега')
    # likes = models.IntegerField(default=0)

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
            
class Likes(models.Model):
    related_name = 'likes'
    
    post_key = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE, related_name=related_name)
    user_key = models.ForeignKey(USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE, related_name=related_name)
    
    def __str__(self) -> str:
        return f"Лайк | {self.post_key}"
    
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = [
            'post_key',
            'user_key'
        ]
        
# post.likes.count()