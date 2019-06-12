from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
import string
import random

from datetime import datetime, date
from collections import namedtuple

# Create your views here.
def show_rooms(request):
    if request.method == "GET":
        return render(request,"reserve.html")
    start_date = request.POST['daterange'][:10]
    start_date = start_date[6:] + "-" + start_date[:2]+ "-" + start_date[3:5]
    end_date = request.POST['daterange'][13:]
    end_date = end_date[6:] + "-" + end_date[:2]+ "-" + end_date[3:5]
    if start_date > end_date:
        return render(request,"reserve.html", {'message':'Start date should be smaller compared to End date'})

    today = str(date.today())
    if today > start_date:
        return render(request,"reserve.html", {'message':'This date is already over'})

    capacity = request.POST['capacity']
    rooms = Rooms.objects.filter(capacity__gte=capacity)
    Range = namedtuple('Range', ['start', 'end'])
    r1 = Range(start=datetime(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:10])), end=datetime(int(end_date[:4]),int(end_date[5:7]),int(end_date[8:10])))

    for booking in Booked.objects.all():
        r2 = Range(start=datetime(int(str(booking.start_date)[:4]),int(str(booking.start_date)[5:7]),int(str(booking.start_date)[8:10])), end=datetime(int(str(booking.end_date)[:4]),int(str(booking.end_date)[5:7]),int(str(booking.end_date)[8:10])))
        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        delta = (earliest_end - latest_start).days + 1
        overlap = max(0, delta)
        if overlap:
            rooms = rooms.exclude(roomnumber__exact=booking.roomnumber)

    if len(rooms) == 0:
        return render(request,"reserve.html", {'message':'There are no rooms free in this period'})
    context = {
        'rooms':rooms,
        'start_date':start_date,
        'end_date':end_date
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
        return HttpResponseRedirect(reverse("reserve"))
    else:
        return render(request, "login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "Logged out."})

def cleanshifts(request):
    user = request.user
    try:
        booking = Booked.objects.get(name__exact=user)
        context = {
            'user':user,
            'booking':booking
        }
    except:
        context = {
            'user':user
        }
    return render(request,"cleanshifts.html", context)

def add_cleanshift(request):

    return render(request,"reserve.html")

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
    context = {
        'roomnumber':request.POST['roomnumber'],
        'room_info':Rooms.objects.get(roomnumber__exact=request.POST['roomnumber']),
        'start_date':request.POST['start_date'],
        'end_date':request.POST['end_date']
    }
    return render(request,"room_info.html", context)

def add_booking(request):
    if request.POST['name'] == "" or request.POST['email'] == "" or request.POST['phone'] == "":
        context = {
            'roomnumber':request.POST['roomnumber'],
            'room_info':Rooms.objects.get(roomnumber__exact=request.POST['roomnumber']),
            'start_date':request.POST['start_date'],
            'end_date':request.POST['end_date'],
            'message':'Fill in all information'
        }
        return render(request,"room_info.html", context)
    name = request.POST['name']
    email = request.POST['email']
    phonenumber = ('06' + request.POST['phone'])
    roomnumber = request.POST['roomnumber']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    try:
        user = User.objects.get(username__exact=name)
    except:
        user = None
    print('user', user)
    if user is not None:
        context = {
            'roomnumber':request.POST['roomnumber'],
            'room_info':Rooms.objects.get(roomnumber__exact=request.POST['roomnumber']),
            'start_date':request.POST['start_date'],
            'end_date':request.POST['end_date'],
            'message':'Name has already been taken'
        }
        return render(request,"room_info.html", context)
    password = randompassword()
    user = User.objects.create_user(name, email, password)
    user.save()
    book = Booked.objects.create(name=name,roomnumber=roomnumber,start_date=start_date,end_date=end_date,phonenumber=phonenumber)
    return HttpResponseRedirect(reverse("reserve"))

def reserve(request):
    return render(request,"reserve.html")

def all_reservations(request):
    return render(request,"all_reservations.html")

def randompassword():
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
    size=8
    return ''.join(random.choice(chars) for x in range(size,12))
