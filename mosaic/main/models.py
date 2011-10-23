from django.db import models

# Create your models here.

class Request(models.Model):
    bbox = models.CharField(max_length=255)
    fulfilled = models.BooleanField(default=False)
    status = models.TextField()
