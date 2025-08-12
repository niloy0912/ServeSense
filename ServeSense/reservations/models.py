from django.db import models


"""
    Need to Create Table first. 
    Then customer 
    Then reservation
    
"""

# ID generated automatically
class Customer(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=20)
    
    def __str__(self):
        return self.lastName + ", " + self.phoneNumber
    
    
class Table(models.Model):
    # Meaningful table Number such as 3B for 3rd table in Balcony etc..
    tableNumber = models.CharField(unique=True, max_length=10)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, default='available')  # e.g., available, reserved, occupied
    
    
    def __str__(self):
        return f"Table {self.tableNumber} - Seats: {self.capacity} - Status: {self.status}"
    
    
class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    numberOfGuests = models.IntegerField()
    reservationTime = models.TimeField()
    reservationDate = models.DateField() # add date automatically when reservation is created
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"Reservation for {self.customer} at {self.reservationDate} for Table {self.table}"