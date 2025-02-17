from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    logo = models.ImageField(upload_to='artists/',blank=False, null=True)
    is_confirmed = models.BooleanField(default=False)
    sub_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name