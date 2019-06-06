from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Rooms, Booked, Reviews, Cleanshifts, Chat, Clipped
from django.contrib.auth.models import User

# Create your views here.
def show_rooms(request):
    if request.method == "GET":
        context = {
            'rooms':Rooms.objects.all()
        }
        return render(request,"rooms.html", context)
    else:
        room = Rooms.objects.filter(roomnumber__exact=request.POST["roomnumber"])
        return render(request,"rooms.html")

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
