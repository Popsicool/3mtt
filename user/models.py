from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    message = models.TextField()
    attended_to = models.BooleanField(default=False)
    def __str__(self):
        return f'Name: {self.name}  Email: {self.email}'


'''
python manage.py makemigrations
python manage.py migrate

'''