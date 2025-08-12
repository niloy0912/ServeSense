from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('Waiter', 'Waiter'),
        ('Chef', 'Chef'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Waiter')
    is_on_duty = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
    

class Attendance(models.Model):
# Store member id, clock in time, and clock out time
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.staff_member.username} - Shift from {self.clock_in_time.strftime('%Y-%m-%d %H:%M')}"