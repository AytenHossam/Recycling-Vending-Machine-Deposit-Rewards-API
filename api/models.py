from django.db import models
from django.contrib.auth.models import User

class Machine(models.Model):
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return f"Machine {self.id} - {self.location} ({self.status})"

class Deposit(models.Model):
    MATERIAL_CHOICES = [
        ('plastic', 'Plastic'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='deposits')
    material_type = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    weight = models.FloatField()
    points = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} deposited {self.weight}kg {self.material_type} at {self.machine}"

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    company_id = models.CharField(max_length=100)

    def __str__(self):
        return f"AdminProfile: {self.user.username} ({self.company_id})"
