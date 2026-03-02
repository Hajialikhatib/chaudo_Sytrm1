from django.db import models
from apps.users.models import CustomUser
from apps.designs.models import Design


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    ORDER_TYPE_CHOICES = (
        ('design', 'From Existing Design'),
        ('custom', 'Custom Design'),
    )

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='orders', limit_choices_to={'role': 'user'}
    )
    tailor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='tailor_orders', limit_choices_to={'role': 'tailor'}
    )
    design = models.ForeignKey(
        Design, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders'
    )
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='design')
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    custom_design_image = models.ImageField(
        upload_to='custom_designs/', blank=True, null=True
    )
    custom_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} → {self.tailor.username}"
