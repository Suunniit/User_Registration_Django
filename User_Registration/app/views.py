from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from random import randint
from app.forms import *

# Create your views here.

def register(request):
    EUFO = UserForm()
    EPFO = ProfileForm()
    d = {'EUFO': EUFO, 'EPFO':EPFO}
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST, request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            pw = UFDO.cleaned_data.get('password')
            MUFDO = UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO = PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            message = f"Hello {UFDO.cleaned_data.get('first_name')} Your Registration in this application is successful"
            email = UFDO.cleaned_data.get('email')
            send_mail(
                'Registration Successful',
                message,
                'sunit.biswal423@gmail.com',
                [email],
                fail_silently=False,
            )
            return HttpResponse('User Registered Successfully')
        return HttpResponse('Invalid Data')
    return render(request, 'register.html', d)

def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO:
            login(request, AUO)
            d={'AUO':AUO}
            request.session['username'] = un
            return render(request, 'home.html', d)
        return HttpResponse('Invalid Username or Password')
    return render(request, 'login.html')

@login_required
def user_profile(request):
    try:
        un = request.session['username']
        UO = User.objects.get(username=un)
        d={'UO':UO}
        request.session.modified = True
        return render(request, 'user_profile.html', d)
    except:
        return render(request, 'login.html')

def home(request):
    request.session.modified = True
    return render(request, 'home.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'home.html')

# def cpass(request):
#     if request.method == 'POST':
#         try:
#             un = request.session['username']
#             UO = User.objects.get(username=un)
#             op = request.POST.get('op')
#             np = request.POST.get('np')
#             cp = request.POST.get('cp')
            
#             if not all([op, np, cp]):
#                 return HttpResponse('Missing data in form submission', status=400)

#             if UO.check_password(op):
#                 if np == cp:
#                     UO.set_password(np)
#                     UO.save()
#                     return HttpResponse('Password Changed Successfully')
#                 return HttpResponse('Password Mismatch')
#             return HttpResponse('Invalid Old Password')
#         except KeyError as e:
#             return HttpResponse(f'Missing key: {str(e)}', status=500)
#     return render(request, 'cpass.html')

@login_required
def cpass(request):
    if request.method == 'POST':
        np = request.POST.get('np')
        cp = request.POST.get('cp')
        if np == cp:
            otp = randint(100000, 999999)
            request.session['np'] = np
            request.session['otp'] = otp
            un = request.session.get('username')
            UO = User.objects.get(username=un)
            email = UO.email
            send_mail(
                'RE :- OTP for changing password',
                f'Your OTP is :{otp}',
                'sunit.biswal423@gmail.com',
                [email],
                fail_silently=False,
            )
            return render(request, 'otp.html')
        return HttpResponse('Password Mismatch')
            
    return render(request, 'cpass.html')

def otp(request):
    if request.method == 'POST':
        UOTP = request.POST.get('otp')
        GOTP = request.session.get('otp')
        if UOTP == str(GOTP):
            un = request.session.get('username')
            UO = User.objects.get(username=un)
            np = request.session.get('np')
            UO.set_password(np)
            UO.save()
            return HttpResponse('Password Changed Successfully')
        return HttpResponse('Invalid OTP')
    return render(request, 'otp.html')

def uname(request):
    if request.method == 'POST':
        un = request.POST.get('un') 
        UO = User.objects.get(username=un)
        if UO:
            otp = randint(100000, 999999)
            request.session['un'] = un
            request.session['otp'] = otp
            email = UO.email
            send_mail(
                'RE :- OTP for changing password',
                f'Your OTP is :{otp}',
                'sunit.biswal423@gmail.com',
                [email],
                fail_silently=False,
            )
            return render(request, 'otp1.html')
        return HttpResponse('Invalid Username')
    return render(request, 'uname.html')
    
def otp1(request):
    if request.method == 'POST':
        UOTP = request.POST.get('otp')
        GOTP = request.session.get('otp')
        if str(GOTP) == UOTP:
            return render(request, 'fpass.html')
        return HttpResponse('Invalid OTP')
    return render(request, 'otp1.html')

def fpass(request):
    if request.method == 'POST':
        np = request.POST.get('np')
        cp = request.POST.get('cp')
        if np == cp:
            un = request.session['un']
            Uo = User.objects.get(username=un)
            Uo.set_password(np)
            Uo.save()
            return render(request, 'login.html')
        return HttpResponse('Password Mismatch')
    return render(request, 'fpass.html') 
