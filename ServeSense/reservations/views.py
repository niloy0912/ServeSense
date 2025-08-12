# reservations/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReservationForm, EditReservationForm
from .models import Customer, Table, Reservation

"""
Reservations App - Views Documentation
-----------------------------   
This views.py file handles all the request/response logic for the reservations application.
It contains the following functionalities:

- home: Renders the main homepage of the application.

- reservation_list: Displays a complete list of all reservations, ordered by date and time.
  This view fetches all Reservation objects from the database and passes them to the 
  'reservation_list.html' template for rendering.

- create_reservation: Manages the creation of new reservations. 
  On a GET request, it displays an empty reservation form. 
  On a POST request, it validates the submitted data. If valid, it first checks for an 
  existing customer by phone number or creates a new one. It then finds an available table 
  that meets the capacity and time requirements. If a table is found, it creates the 
  reservation and redirects to the reservation list. If no table is available, it displays 
  an error message on the form.

- edit_reservation: Handles the modification of an existing reservation. 
  It takes a reservation_id from the URL to fetch a specific reservation. 
  On a GET request, it displays a form pre-populated with that reservation's data. 
  On a POST request, it validates and saves the updated information, then redirects to the 
  reservation list.

- delete_reservation: Manages the deletion of a specific reservation. 
  On a GET request, it displays a confirmation page to prevent accidental deletion. 
  On a POST request (after the user confirms), it deletes the reservation record from the 
  database and redirects to the reservation list.
  
- accept_reservation: Handles the business logic for confirming a reservation.
  It takes a reservation_id, finds the reservation, updates its status to 'Confirmed',
  finds the associated table, updates its status to 'reserved', and then redirects
  the user back to the reservation list with a success message.
"""

def home(request):
    return render(request, 'index.html')


def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # create new customer or get existing one
            try:
                customer = Customer.objects.get(phoneNumber=data['phone_number'])
            except Customer.DoesNotExist:
                customer = Customer.objects.create(
                    firstName=data['first_name'],
                    lastName=data['last_name'],
                    phoneNumber=data['phone_number']
                )
            
            possible_tables = Table.objects.filter(capacity__gte=data['number_of_guests'])
            
            # Check for available tables at the requested time
            found_table = None
            for table in possible_tables:
                is_reserved = Reservation.objects.filter(
                    table=table, 
                    reservationDate=data['reservation_date'], 
                    reservationTime=data['reservation_time']
                ).exists()  # is_reserved is True if the table is already booked
                
                if not is_reserved:
                    found_table = table
                    break
            
            if found_table:
                Reservation.objects.create(
                    customer=customer,
                    table=found_table,
                    numberOfGuests=data['number_of_guests'],
                    reservationDate=data['reservation_date'],
                    reservationTime=data['reservation_time']
                )
                messages.success(request, "Reservation created successfully!")
                return redirect('reservation_list')
            else:
                form.add_error(None, "Sorry, no tables are available for that time and party size.")
    
    else:
        form = ReservationForm()

    return render(request, 'add_reservation.html', {'form': form})


def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation updated successfully!")
            return redirect('reservation_list')
    else:
        form = EditReservationForm(instance=reservation)

    return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Reservation has been cancelled.")
        return redirect('reservation_list')

    return render(request, 'delete_reservation.html', {'reservation': reservation})


def accept_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    reservation.status = 'Confirmed'
    reservation.save()
    
    table_to_update = reservation.table
    table_to_update.status = 'reserved'
    table_to_update.save()

    messages.success(request, f"Reservation for {reservation.customer.firstName} has been Confirmed and Table {table_to_update.tableNumber} is now reserved.")
    
    return redirect('reservation_list')


def reservation_list(request):
    all_reservations = Reservation.objects.order_by('reservationDate', 'reservationTime')
    context = {
        'reservations': all_reservations
    }
    return render(request, 'reservation_list.html', context)