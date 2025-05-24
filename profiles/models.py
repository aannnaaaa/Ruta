from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=200, verbose_name='Название поездки')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(verbose_name='Дата поездки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'