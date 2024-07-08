from django.db import models

# Create your models here.

class Diagram(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='diagrams/', null=True, blank=True)
