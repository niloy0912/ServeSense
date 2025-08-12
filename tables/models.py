from django.db import models

class Table(models.Model):
    STATUS_CHOICES = [
        ('Free', 'Free'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
    ]
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Free')
    time_left = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Table {self.number}"
