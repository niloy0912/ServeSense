# reservations/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Customer, Table, Reservation
import datetime

class ReservationTests(TestCase):

    # set up some basic data that all our tests can use
    def setUp(self):
        self.table = Table.objects.create(tableNumber='A1', capacity=2)
        self.customer = Customer.objects.create(firstName='John', lastName='Smith', phoneNumber='5231211')

    def test_create_reservation_works(self):
        # data for a new booking
        new_booking_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '555-2222',
            'number_of_guests': 2,
            'reservation_date': datetime.date.today(),
            'reservation_time': '19:00',
        }

        # start with 0 reservations
        self.assertEqual(Reservation.objects.count(), 0)

        # post the data to the create page
        self.client.post(reverse('add_reservation'), data=new_booking_data)

        # We should now have 1 reservation
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
            'first_name': 'Another',
            'last_name': 'Person',
            'phone_number': '555-3333',
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