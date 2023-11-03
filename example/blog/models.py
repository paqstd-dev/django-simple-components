from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)
    cover = models.ImageField(upload_to='images')

    content = models.TextField()

    categories = models.ManyToManyField(
        Category,
        related_name='posts',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
