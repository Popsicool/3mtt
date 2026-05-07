from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    sold = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="product/")
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)