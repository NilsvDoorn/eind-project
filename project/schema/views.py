from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *

from datetime import datetime
from collections import namedtuple

from django.views import generic
from django.utils.safestring import mark_safe
# from .utils import Calendar

# Create your views here.
def show_rooms(request):
    if request.method == "GET":
        return render(request,"reserve.html")
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']

    if start_date > end_date:
        return render(request,"reserve.html", {'message':'Start date should be smaller compared to End date'})
    capacity = request.POST['capacity']
    rooms = Rooms.objects.filter(capacity__gte=capacity)
    Range = namedtuple('Range', ['start', 'end'])
    r1 = Range(start=datetime(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:10])), end=datetime(int(end_date[:4]),int(end_date[5:7]),int(end_date[8:10])))
    for booking in Booked.objects.all():
        print(booking)
        r2 = Range(start=datetime(booking.start_date[:4],booking.start_date[5:7],booking.start_date[8:10]), end=datetime(booking.end_date[:4],booking.end_date[5:7],booking.end_date[8:10]))
        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        delta = (earliest_end - latest_start).days + 1
        overlap = max(0, delta)
        if overlap:
            print('true')
        else:
            print('false')
    context = {
        'rooms':rooms
    }
    return render(request,"rooms.html", context)

def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("show_rooms"))
    else:
        return render(request, "login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "Logged out."})

def cleanshifts(request):
    context = {
        'cleanshifts':Cleanshifts.objects.all()
    }
    return render(request,"cleanshifts.html", context)

def add_cleanshift(request):
    pass

def reviews(request):
    reviewed = False
    reviews = Reviews.objects.all()
    for review in reviews:
        if review.name == request.user.username:
            reviewed = True
    context = {
        'reviewed':reviewed,
        'reviews':reviews
    }
    return render(request,"reviews.html", context)

def add_review(request):
    try:
        anoniem = request.POST['anoniem']
    except:
        anoniem = False
    review = Reviews.objects.create(name=request.user,roomnumber=1,message=request.POST['review'],note=request.POST['rating'],anoniem=anoniem)
    return HttpResponseRedirect(reverse("reviews"))

def room_info(request):
    print(request.POST['roomnumber'])
    print(Rooms.objects.filter(roomnumber__exact=request.POST['roomnumber']))
    context = {
        'room_info':Rooms.objects.filter(roomnumber__exact=request.POST['roomnumber'])
    }
    return render(request,"room_info.html", context)

def add_booking(request):
    pass

def reserve(request):
    return render(request,"reserve.html")

def all_reservations(request):
    return render(request,"all_reservations.html")

# class CalendarView(generic.ListView):
#     model = Event
#     template_name = 'cal/calendar.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # use today's date for the calendar
#         d = get_date(self.request.GET.get('day', None))
#
#         # Instantiate our calendar class with today's year and date
#         cal = Calendar(d.year, d.month)
#
#         # Call the formatmonth method, which returns our calendar as a table
#         html_cal = cal.formatmonth(withyear=True)
#         context['calendar'] = mark_safe(html_cal)
#         return context
#
# def get_date(req_day):
#     if req_day:
#         year, month = (int(x) for x in req_day.split('-'))
#         return date(year, month, day=1)
#     return datetime.today()
