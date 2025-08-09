from django.shortcuts import render
from .models import Reservation, Table

# The views.py file will handle the logic for displaying and processing reservations.
# Including the home page vieew in reservations/views.py

"""
CREATE A 'CORE' APP TO MANAGE HOMEPAGE ETC (IF NEEDED)
"""

def home(request):
    return render(request, 'base.html')
