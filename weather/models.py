from django.db import models

# Create your models here.

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.city}"

