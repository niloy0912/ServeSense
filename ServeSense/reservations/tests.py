from django.test import TestCase
from django.urls import reverse # reverse is used to find urls
from .models import Customer, Table, Reservation
import datetime

"""
Reservations App - Testing Documentation
----------------------------------------

Overview:
The testing strategy for the 'reservations' app focuses on validating the
core business logic of the reservation system. The tests are designed to
ensure that a manager can create, view, and manage reservations reliably.
We use Django's built-in TestCase class, which provides a clean, isolated
database for each test run, ensuring that tests do not interfere with each
other or the main development database.

Test Structure:
The tests are contained within the ReservationLogicTests class. This class
follows a standard structure:

1. setUp() Method:
   Before any test is run, this method creates a baseline set of data,
   including a sample Table, a Customer, and a Reservation. This
   pre-populates the test database with predictable data, allowing each
   test case to have a consistent starting point without repeating
   creation logic.

2. Individual Test Cases:
   Each core functionality is tested in its own dedicated method (e.g.,
   'test_create_reservation_success'). This makes the suite easy to read
   and debug. If one test fails, it does not stop the others from running.

Key Scenarios Covered:
- Successful Creation (The "Happy Path"):
  Tests if a user can successfully submit the "add reservation" form and
  verifies that a new Reservation object is correctly added to the database.

- Failure Condition (The "Sad Path"):
  Tests the system's ability to prevent a double booking by attempting to
  create a reservation for a time slot that is already taken. It asserts
  that a new reservation is NOT created and that the user is shown an
  error message.

- Core Actions (Edit, Delete, Accept):
  Separate tests verify that the edit, delete, and accept functionalities
  work as expected by checking that the database records are updated or
  removed correctly after the action is performed.
"""



class ReservationTests(TestCase):
    # set up some basic data that all our tests can use
    def setUp(self):
        self.table = Table.objects.create(tableNumber='A1', capacity=2)
        self.customer = Customer.objects.create(firstName='John', lastName='Doe', phoneNumber='5231211')


    def test_create_reservation_works(self):
        # data for a new booking
        new_booking_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '555-2222',
            'number_of_guests': 2,
            'reservation_date': datetime.date.today(),
            'reservation_time': '12:00',
        }

        self.assertEqual(Reservation.objects.count(), 0)
        self.client.post(reverse('add_reservation'), data=new_booking_data)
        self.assertEqual(Reservation.objects.count(), 1)


    def test_double_booking_is_prevented(self):
        # First, make a reservation for 8 PM
        Reservation.objects.create(
            customer=self.customer,
            table=self.table,
            numberOfGuests=2,
            reservationDate=datetime.date.today(),
            reservationTime='20:00'
        )

        # Now, try to book the same table at the same time
        double_book_data = {
            'first_name': 'another',
            'last_name': 'person',
            'phone_number': '5553333',
            'number_of_guests': 2,
            'reservation_date': datetime.date.today(),
            'reservation_time': '20:00', # Same time
        }

        # We start with 1 reservation, and it should stay that way
        self.assertEqual(Reservation.objects.count(), 1)
        response = self.client.post(reverse('add_reservation'), data=double_book_data)
        self.assertEqual(Reservation.objects.count(), 1)

        # It should show the form again and contain an error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, no tables are available")
        
        
    def test_edit_reservation_works(self):
        # Create a reservation that we can edit
        reservation = Reservation.objects.create(
            customer=self.customer,
            table=self.table,
            numberOfGuests=2,
            reservationDate=datetime.date.today(),
            reservationTime='18:00'
        )
        
        # New data - let's change the guest count
        edited_data = {
            'numberOfGuests': 1,
            'reservationDate': reservation.reservationDate,
            'reservationTime': reservation.reservationTime,
            'status': 'Pending',
        }
        
        edit_url = reverse('edit_reservation', args=[reservation.id])
        self.client.post(edit_url, data=edited_data)
        
        # Get the reservation from the DB again to check it
        reservation.refresh_from_db()
        self.assertEqual(reservation.numberOfGuests, 1)


    def test_accept_reservation_works(self):
        reservation = Reservation.objects.create(
            customer=self.customer,
            table=self.table,
            numberOfGuests=2,
            reservationDate=datetime.date.today(),
            reservationTime='17:00'
        )
        
        # Check initial state
        self.assertEqual(reservation.status, 'Pending')
        self.assertEqual(reservation.table.status, 'available')
        
        # Hit the 'accept' URL
        accept_url = reverse('accept_reservation', args=[reservation.id])
        self.client.get(accept_url)

        # Refresh objects from DB to see changes
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, 'Confirmed')
        
        table = Table.objects.get(id=self.table.id)
        self.assertEqual(table.status, 'reserved')