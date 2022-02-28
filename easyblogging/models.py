from .helpers import*
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class BlogModel(models.Model):
    title=models.CharField(max_length=1000)
    content =HTMLField()
    slug=models.SlugField(max_length=1000, null=True , blank=True)
    image=models.ImageField(upload_to='images/',blank=True,null=True)
    liked = models.IntegerField(default=0, blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    upload_to=models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', related_name='posts')



    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
