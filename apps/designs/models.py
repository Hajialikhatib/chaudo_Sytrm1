from django.db import models
from apps.users.models import CustomUser


class Design(models.Model):
    CLOTHING_TYPE_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('both', 'Both'),
        ('kids', 'Kids'),
    )

    tailor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='designs', limit_choices_to={'role': 'tailor'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    clothing_type = models.CharField(max_length=10, choices=CLOTHING_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='designs/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.tailor.username}"
