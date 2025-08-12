from django.test import TestCase
from django.urls import reverse #reverse is used to find urls
from .models import User, Attendance

"""
Staff App - Testing Documentation
---------------------------------

Overview:
The testing approach for the 'staff' app is designed to validate all
aspects of employee management, from account creation to attendance tracking.
The tests ensure that the user interface actions correctly manipulate the User
and Attendance models in the backend. Like the reservations app, these tests
use the TestCase class to ensure isolation and predictability.

Test Structure:
All tests are located in the StaffFeatureTests class.

1. setUp() Method:
   The setUp() method for this app creates a single, standard staff user
   ('testwaiter'). This user acts as the primary subject for all subsequent
   tests, such as editing their role or clocking them in and out.

2. Individual Test Cases:
   Each method is named to clearly describe the feature it is testing
   (e.g., 'test_add_new_staff_member_works').

Key Scenarios Covered:
- Account Management:
  Tests validate the user creation process by simulating a form submission
  with all required fields (including password confirmation). It also tests
  the "edit" functionality by changing a user's role and checking the
  database for the update.

- Shift and Attendance Logic:
  The 'test_clock_in_and_out_works' case validates the entire shift-tracking
  workflow. It checks that the user's 'is_on_duty' status changes correctly
  and, crucially, that a corresponding 'Attendance' record is created upon
  clock-in and updated with a 'clock_out_time' upon clock-out.

- Page Accessibility:
  Simple tests are included as basic "smoke tests" to confirm that key
  pages like the staff list and attendance log can be accessed without
  encountering server errors.
"""

class StaffTests(TestCase):

    # setup basic info for all tests
    def setUp(self):
        self.staff_member = User.objects.create_user(
            username='testwaiter',
            password='Super_Password123',
            role='Waiter'
        )

    # Render staff list
    def test_staff_list_page_works(self):
        url = reverse('staff_list')
        response = self.client.get(url) #self.client is like a dummy web browser
        self.assertEqual(response.status_code, 200) #200 means OK


    # Add a new staff member?
    # Test fails. why???
    def test_add_new_staff_member_works(self):
        # this is the data we want to submit in the "add staff" form.
        new_staff_data = {
            'username': 'newchef',
            'first_name': 'New',
            'last_name': 'Chef',
            'role': 'Chef',
            # For security, UserCreationForm requires two matching passwords.
            'password': 'VeryToughPassword456',
            'password2': 'VeryToughPassword456'
        }
        self.assertEqual(User.objects.count(), 1)
        url = reverse('add_staff')
        self.client.post(url, data=new_staff_data)        
        self.assertEqual(User.objects.count(), 2)


    # Edit an existing staff member
    def test_edit_staff_role_works(self):
        edited_data = {
            'role': 'Manager'
        }
        self.assertEqual(self.staff_member.role, 'Waiter')
        url = reverse('edit_staff', args=[self.staff_member.id])
        self.client.post(url, data=edited_data)
        # We have to "refresh" our 'self.staff_member' object to get the latest data from the database after the change.
        self.staff_member.refresh_from_db()
        self.assertEqual(self.staff_member.role, 'Manager')


    # Does clocking in and out work
    def test_clock_in_and_out_works(self):
        # Check the user's status at the start. is_on_duty should be False.
        self.assertFalse(self.staff_member.is_on_duty)
        # We also check that there are no attendance records in the database at the start.
        self.assertEqual(Attendance.objects.count(), 0)

        # Test Clocking In
        clock_in_url = reverse('clock_in', args=[self.staff_member.id])
        self.client.get(clock_in_url)
        self.staff_member.refresh_from_db()
        self.assertTrue(self.staff_member.is_on_duty)
        self.assertEqual(Attendance.objects.count(), 1)

        #Now let's test Clocking Out
        clock_out_url = reverse('clock_out', args=[self.staff_member.id])
        self.client.get(clock_out_url)
        self.staff_member.refresh_from_db()
        self.assertFalse(self.staff_member.is_on_duty)
        
        # -Check the details of the attendance log
        # Get the first (and only) attendance record from the database.
        shift_log = Attendance.objects.first()
        
        # Check that the log is linked to the correct staff member.
        self.assertEqual(shift_log.staff_member, self.staff_member)
        
        # Check that the log now has a clock-out time (it's not None).
        self.assertIsNotNone(shift_log.clock_out_time)