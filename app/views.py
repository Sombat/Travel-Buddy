from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
	return redirect('/main')

def main(request):
	return render(request,'main.html')

def register(request):
	# print(len(User.objects.filter(username=request.POST['username'])))
	errors = User.objects.register_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/main')
	else:
		hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		newUser = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hash1.decode())
		request.session['logged_in_user_id'] = newUser.id
	return redirect('/travels')

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		userinDB = User.objects.get(username=request.POST['username'])
		request.session['logged_in_user_id'] = userinDB.id
	return redirect('/travels')

def success(request):
	if 'logged_in_user_id' in request.session:
		context = {
			'logged_in_user': User.objects.get(id=request.session['logged_in_user_id'])
		}
		return render(request, 'success.html', context)
	return redirect('/main')

def logout(request):
	request.session.flush()
	return redirect('/main')

def travels(request):
	userinDB = User.objects.get(id=request.session['logged_in_user_id'])
	context = {
		"logged_in_user": User.objects.get(id=request.session['logged_in_user_id']),
		"your_trips": Trip.objects.filter(guest=userinDB).order_by('-created_at'),
		"other_trips": Trip.objects.exclude(guest=userinDB).order_by('-created_at'),
	}
	return render(request,'travels.html', context)

def add(request):
	return render(request,'add.html')

def add_trip(request):
	# print(date.today())
	# # print(date.today().strftime('%Y/%m/%d'))
	# print(request.POST['travel_start'])
	# # print(datetime.strptime(request.POST['travel_start']))
	errors = Trip.objects.trip_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/travels/add')
	else:
		logged_in_user = User.objects.get(id=request.session['logged_in_user_id'])
		newTrip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], travel_start=request.POST['travel_start'], travel_end=request.POST['travel_end'], creator=logged_in_user)
		logged_in_user.trips_guest_of.add(newTrip)
	return redirect('/travels')

def join_trip(request, trip_id):
	user_to_add = User.objects.get(id=request.session['logged_in_user_id'])
	trip_to_join = Trip.objects.get(id=trip_id)
	user_to_add.trips_guest_of.add(trip_to_join)
	return redirect('/travels')

def destination(request, trip_id):
	context = {
		"this_trip": Trip.objects.get(id=trip_id),
	}
	return render(request, 'destination.html', context)