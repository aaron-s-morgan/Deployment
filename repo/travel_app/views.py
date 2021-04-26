from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == "POST":
        # Validation check before DB save
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # print(request.POST['password'])

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # print(hash_pw)
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['logged_user'] = new_user.id

        return redirect('/dashboard')
    return redirect("/")
    # localhost:8000/dashboard

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/dashboard')
        messages.error(request, "Email or password are incorrect.")
            
    return redirect("/")

def dashboard(request):
    myself = User.objects.get(id=request.session['logged_user'])
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'trips' : Trip.objects.all(),
        'myself' : myself
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def create(request):
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
    }
    return render (request, 'create_trip.html', context)


def create_trip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')

    Trip.objects.create(
        destination=request.POST['destination'],
        start_date=request.POST['start_date'],
        end_date=request.POST['end_date'],  
        plan=request.POST['plan'],
        creator = User.objects.get(id=request.session['logged_user'])
    )
    return redirect('/dashboard')


def show_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'trip' : trip
    }
    return render(request, 'show_trip.html', context)

def edit(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'trip' : trip
    }
    return render (request, 'edit_trip.html', context)

def edit_trip(request, trip_id):
    errors = Trip.objects.trip_validator(request.POST)
    if errors:
        trip = Trip.objects.get(id=trip_id)
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect(f'/trips/edit/{trip.id}')

    trip = Trip.objects.get(id=trip_id)
    trip.destination = request.POST['destination']
    trip.start_date = request.POST['start_date']
    trip.end_date = request.POST['end_date']
    trip.plan = request.POST['plan']
    trip.save()
    context = {
        'trip' : trip
    }
    return redirect('/dashboard')

def delete_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/dashboard')

def join(request, trip_id):
    user = User.objects.get(id=request.session['logged_user'])
    trip = Trip.objects.get(id=trip_id)
    user.trips.add(trip)

    return redirect('/dashboard')

def unjoin(request, trip_id):
    user = User.objects.get(id=request.session['logged_user'])
    trip = Trip.objects.get(id=trip_id)
    user.trips.remove(trip)

    return redirect('/dashboard')