from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

def already_loggedin(view_func):
    def wrapper_func(request, *args, **kwargs):
        print(request.user.id) # none for AnnoymousUer ...one way to check user
        if request.user.is_anonymous:
            print("inside")
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/home')
    return wrapper_func

def already_registered(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method =='POST':
            user = User.objects.filter(email=request.POST['email']).first()
            if user:
                print("reg failed")
                return redirect('/signup')
            else:
                print("applying for reg")
                return view_func(request, *args, **kwargs)
        return render(request, 'booking/signup.html')
    return wrapper

def allowed_groups(allowed_groups=[]):
    def user_decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user_groups=[]
            for group in request.user.groups.all():
                user_groups.append(group)
            flag=False
            for user_group in user_groups:
                if user_group.name in allowed_groups:
                    flag=True
                    break
            if flag:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("permission denied")
        return wrapper_func
    return user_decorator