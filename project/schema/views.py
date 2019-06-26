from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
import string
import random
import time
import datetime as dt
from collections import namedtuple

import flask
import os

from mollie.api.client import Client
from mollie.api.error import Error

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

#
# Initialize the Mollie API library with your API key.
#
api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')
mollie_client = Client()
mollie_client.set_api_key("test_rTe5Ak2VKrBF2SgxFcJgCdfqVHnE7S")

# Create your views here.
def show_rooms(request):
    if request.method == "GET":
        return render(request,"reserve.html")
    elif request.POST['datefilter'] == "":
        return render(request,"reserve.html", {'message':'Fill in all fields'})

    start_date = request.POST['datefilter'][:10]
    end_date = request.POST['datefilter'][13:]
    today = str(dt.date.today())

    if check_date(start_date) or check_date(end_date):
        return render(request, "reserve.html", {'message':"Don't do that"})

    if today > start_date or start_date >= end_date:
        return render(request,"reserve.html", {'message':'This date is already over'})

    rooms = Rooms.objects.all()
    Range = namedtuple('Range', ['start', 'end'])
    r1 = Range(start=dt.datetime(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:10])),
                end=dt.datetime(int(end_date[:4]),int(end_date[5:7]),int(end_date[8:10])))

    for booking in Booked.objects.all():
        if check_available(booking, start_date, end_date):
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
        if user.is_superuser:
            return HttpResponseRedirect(reverse("all_reservations"))
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
    clean_date = request.POST['datetimes']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']

    if check_date(clean_date) or check_time(start_time) or check_time(end_time):
        return render(request,"reserve.html", {'message':"Don't do that"})

    if clean_date == "" or start_time == "" or end_time == "":
        return render(request,"cleanshifts.html", {'message':"Fill in all fields"})

    start_time = dt.time(int(start_time[:2]), int(start_time[3:5]))
    end_time = dt.time(int(end_time[:2]), int(end_time[3:5]))
    if request.user.is_superuser:
        roomnumber = request.POST['roomnumber2']
    else:
        roomnumber = request.POST['roomnumber']
        if roomnumber == "" or person_room(roomnumber, request.user):
            return render(request,"reserve.html", {'message':"Don't do that"})

    today = str(dt.date.today())
    time_now = dt.time(int(str(dt.datetime.now())[11:13]),int(str(dt.datetime.now())[14:16]))

    if today > clean_date:
        return render(request,"cleanshifts.html", {'message':"This date is already over"})
    elif today == clean_date and start_time < time_now:
        return render(request,"cleanshifts.html", {'message':"This time is already over"})
    elif end_time < start_time:
        return render(request,"cleanshifts.html", {'message':"Invalid time"})
    shift = Cleanshifts.objects.create(name=request.user,
                                        roomnumber=roomnumber,
                                        date=clean_date,
                                        start_time=start_time,
                                        end_time=end_time)
    return HttpResponseRedirect(reverse("cleanshifts"))

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
    roomnumber = Booked.objects.get(name=request.user).roomnumber

    review = Reviews.objects.create(name=request.user,
                                    roomnumber=roomnumber,
                                    message=request.POST['review'],
                                    note=request.POST['rating'],
                                    anoniem=anoniem)
    return HttpResponseRedirect(reverse("reviews"))

def room_info(request):
    if len(Rooms.objects.filter(roomnumber__exact=request.POST['roomnumber'])) == 1:
        context = {
            'roomnumber':request.POST['roomnumber'],
            'room_info':Rooms.objects.get(roomnumber__exact=request.POST['roomnumber']),
            'start_date':request.POST['start_date'],
            'end_date':request.POST['end_date']
        }
        return render(request,"room_info.html", context)
    else:
        return render(request,"reserve.html", {'message':"Don't do that"})

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
    name = request.POST['name'] + randompassword()
    email = request.POST['email']
    phonenumber = ('06' + request.POST['phone'])
    roomnumber = request.POST['roomnumber']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    today = str(dt.date.today())

    if check_date(start_date) or check_date(end_date):
        return render(request, "reserve.html", {'message':"Don't do that"})
    if today > start_date or start_date >= end_date:
        return render(request,"reserve.html", {'message':'This date is already over'})
    elif roomnumber == "" or len(Rooms.objects.filter(roomnumber__exact=roomnumber)) != 1:
        return render(request,"reserve.html", {'message':"Don't do that"})
    elif len(phonenumber) != 10 or not phonenumber.isnumeric():
        context = {
            'roomnumber':request.POST['roomnumber'],
            'room_info':Rooms.objects.get(roomnumber__exact=request.POST['roomnumber']),
            'start_date':request.POST['start_date'],
            'end_date':request.POST['end_date'],
            'message':'Invalid phonenumber'
        }
        return render(request,"room_info.html", context)

    for booking in Booked.objects.filter(roomnumber__exact=roomnumber):
        if check_available(booking, start_date, end_date):
            return render(request, "reserve.html", {'message':"This room is already been booked"})

    d1 = dt.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
    d2 = dt.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))
    nights = (d2 - d1).days
    price = float(Rooms.objects.get(roomnumber__exact=roomnumber).price) * nights
    try:
        user = User.objects.get(username__exact=name)
    except:
        user = None

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
    payment = mollie(request, name, price)
    book = Booked.objects.create(name=name,
                                roomnumber=roomnumber,
                                start_date=start_date,
                                end_date=end_date,
                                phonenumber=phonenumber,
                                payment_id=payment.id)
    return HttpResponseRedirect(payment.checkout_url)

def reserve(request):
    return render(request,"reserve.html")

def all_reservations(request):
    return render(request,"all_reservations.html")

def randompassword():
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
    size=8
    return ''.join(random.choice(chars) for x in range(size,12))

def mollie(request, name, price):
    try:
        #
        # Generate a unique webshop order id for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        my_webshop_id = name

        #
        # Payment parameters:
        # amount        Currency and value. This example creates a € 120,- payment.
        # description   Description of the payment.
        # redirectUrl   Redirect location. The customer will be redirected there after the payment.
        # metadata      Custom metadata that is stored with the payment.
        #
        payment = mollie_client.payments.create({
            'amount': {
                'currency': 'EUR',
                'value': f'{price:.2f}'
            },
            'description': 'My first API payment',
            'redirectUrl': request.build_absolute_uri(reverse("succes", args=[my_webshop_id])),
            'metadata': {
                'order_id': "12345"
            }
        })

        #
        # In this example we store the order with its payment status in a database.
        #
        data = {'status': payment.status}
        # database_write(my_webshop_id, data)

        #
        # Send the customer off to complete the payment.
        #
        return payment

    except Error as err:
        print('API call failed: {error}'.format(error=err))

def succes(request, name):

    try:
        booking = Booked.objects.get(name__exact=name)
        payment = mollie_client.payments.get(booking.payment_id)
    except:
        return render(request,"reserve.html")

    if payment.status == "paid":
        return render(request,"succes.html")
    else:
        booking.delete()
        return render(request,"reserve.html", {'message':'Payment went wrong'})

@csrf_exempt
def events(request):
    list = []
    all = Booked.objects.all()
    for booking in all:
        dict = {"id": booking.id, "title": booking.roomnumber, "start": booking.start_date, "end": booking.end_date}
        list.append(dict)

    return JsonResponse(list, safe=False)

@csrf_exempt
def events_clean(request):
    list = []
    all = Cleanshifts.objects.all()
    for shift in all:
        start = dt.datetime.combine(shift.date, shift.start_time)
        end = dt.datetime.combine(shift.date, shift.end_time)
        dict = {"id": shift.id, "title": shift.roomnumber, "start": start, "end": end}
        list.append(dict)

    return JsonResponse(list, safe=False)

@csrf_exempt
def events_clean_person(request):
    list = []
    all = Cleanshifts.objects.filter(name__exact=request.user)
    for shift in all:
        start = dt.datetime.combine(shift.date, shift.start_time)
        end = dt.datetime.combine(shift.date, shift.end_time)
        dict = {"id": shift.id, "title": shift.roomnumber, "start": start, "end": end}
        list.append(dict)

    return JsonResponse(list, safe=False)

def check_date(date):
    try:
        dt.datetime.strptime(date, '%Y-%m-%d')
        return False
    except ValueError:
        return True

def check_time(time):
    try:
        dt.datetime.strptime(time, "%H:%M")
        return False
    except ValueError:
        return True

def person_room(room, user):
    if user.is_superuser:
        return False
    elif int(Booked.objects.get(name__exact=user).roomnumber) == int(room):
        return False
    else:
        return True

def check_available(booking, start_date, end_date):
    Range = namedtuple('Range', ['start', 'end'])
    r1 = Range(start=dt.datetime(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:10])),
                end=dt.datetime(int(end_date[:4]),int(end_date[5:7]),int(end_date[8:10])))
    r2 = Range(start=dt.datetime(int(str(booking.start_date)[:4]),int(str(booking.start_date)[5:7]),int(str(booking.start_date)[8:10])),
                end=dt.datetime(int(str(booking.end_date)[:4]),int(str(booking.end_date)[5:7]),int(str(booking.end_date)[8:10])))
    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)
    delta = (earliest_end - latest_start).days + 1
    overlap = max(0, delta)
    if overlap:
        return True
    else:
        return False
