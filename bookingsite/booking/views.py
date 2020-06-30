import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .decorators import allowed_groups, already_loggedin, already_registered
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Auditorium, TimeSlot, Event
import datetime

# Create your views here.


def landingpage(request):
    print('hello')
    return render(request, 'booking/index.html')

@already_loggedin
def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email']).first() # can't check password directly here as passwords are stored in hashed form in table
                                                                        # for that use check_password method..... to change use set_passwrod
        print(str(user) + " user")
        if user and user.check_password(request.POST['pass']):
            print(user.check_password(request.POST['pass']))
            auth_login(request, user)
            print(request.user.email)
            return redirect('/home')
        else:
            return redirect('/login')
    return render(request, 'booking/login.html')

@already_registered
def signup(request):
    if request.method == 'POST':
        # User._meta.get_field('username')._unique = False
        user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['pass'])
        user.save()
        print("reg success")
        auth_login(request, user)
        return redirect('/home')
        
    return render(request, 'booking/signup.html')

def getgroup(request):
    groups = []
    res = request.user.groups.all()
    for i in res:
        groups.append(i.name)
    return groups

@login_required(login_url='login/')
@allowed_groups(allowed_groups=['student', 'teacher'])
def home(request):
    groups = getgroup(request)
    return render(request, 'booking/sidebar.html', {'groups': groups})


@login_required(login_url='login/')
def auditorium(request):
    groups = getgroup(request)
    superuser = request.user.is_superuser
    print(superuser)
    audi = Auditorium.objects.all()
    path = os.path.join(settings.MEDIA_ROOT)
    print(path)
    return render(request, 'booking/auditorium.html', {'groups': groups, 'superuser': superuser, 'audi':audi, 'path': path})

@allowed_groups(allowed_groups=['student'])
@login_required(login_url='login/')
def bookingform(request, **kwargs):
    groups = getgroup(request)
    superuser = request.user.is_superuser
    timeslotobj = TimeSlot.objects.filter(audiname=kwargs['idno']).all()
    print(type(timeslotobj[0].start_at))
    if request.method == 'POST':
        event = Event()
        event.email = request.POST['email'].lstrip(' ').rstrip(' ')
        event.eventname = request.POST['title'].lstrip(' ').rstrip(' ')
        event.eventdesc = request.POST['desc'].lstrip(' ').rstrip(' ')
        event.eventdate = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
        event.slots = datetime.time(hour=int(request.POST['slots']))
        event.eventexp = int(request.POST['exp'])
        event.phone = request.POST['phone']
        event.status = 0
        event.save()
    return render(request, "booking/bookingform.html", {'groups': groups, 'superuser': superuser, 'timeslotobj': timeslotobj})

@allowed_groups(allowed_groups=['teacher'])
@login_required(login_url='login/')
def addaudi(request, **kwargs):
    groups, roomno = getgroup(request), kwargs['roomno']
    audi = Auditorium.objects.filter(name=roomno).first()
    imgname=None
    path = os.path.join(settings.MEDIA_ROOT)
    if audi:
        imgname = str(audi.img)
        imgname = imgname.split('/')[2]
    if request.method == 'POST':
        try:
            if not audi:
                audi = Auditorium()
                audi.name = request.POST['audiname']            
                audi.description = request.POST['desc']
                if request.FILES:
                    audi.img = request.FILES['image']
                audi.save()
            
            times=[] 
            for time in request.POST['time'].split(","):
                times.append(time.lstrip(' ').rstrip(' '))
            days=[]
            for day in request.POST.getlist('days'):
                days.append(day)
            print(times)
            print(days)
            for time in times:
                timeslot = TimeSlot()
                timeslot.start_at = datetime.time(hour=int(time.split('-')[0]))
                timeslot.close_at = datetime.time(hour=int(time.split('-')[1]))
                timeslot.days = days
                print(Auditorium.objects.filter(name=request.POST['audiname']).first())
                timeslot.audiname = Auditorium.objects.filter(name=request.POST['audiname']).first()
                timeslot.save()
                print("saved")
            redirect('/audi')

        except Exception as e:
            print("in except")
            print(e)
            
        
        redirect('/audi')

    return render(request, 'booking/addaudi.html', {'i':range(5), 'groups': groups, 'roomno': roomno, 'audi': audi, 'imgname': imgname})

@login_required(login_url='login/')
def events(request):
    groups = getgroup(request)
    events = Event.objects.filter(status=1).all()
    appl = Event.objects.filter(email=request.user.email).all()
    return render(request, 'booking/events.html', {'groups': groups, 'events': events, 'appl': appl})


@login_required(login_url='login/')
def adminpage(request):
    return HttpResponse("admin")

@allowed_groups(allowed_groups=['teacher'])
@login_required(login_url='login/')
def passevents(request, **kwargs):
    print(kwargs)
    groups = getgroup(request)
    events = Event.objects.filter(status=0).all()
    if int(kwargs['status']) == 1:
        event = Event.objects.filter(id=int(kwargs['eventid'])).first()
        event.status = 1
        event.save()
    elif int(kwargs['status']) == 1:
        event = Event.objects.filter(id=int(kwargs['eventid'])).first()
        event.status = -1
        event.save()

    return render(request, 'booking/appl.html', {'groups': groups, 'events': events})

@login_required(login_url='login/')
def logout(request):
    auth_logout(request)
    return redirect('/')