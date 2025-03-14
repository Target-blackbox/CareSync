from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, LoginForm, ForgotPasswordForm, OTPVerificationForm, ResetPasswordForm
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils import timezone
from reports.models import ReportFolder

from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                
                # Generate OTP and store in session
                otp = generate_otp()
                request.session['reset_otp'] = otp
                request.session['reset_email'] = email
                request.session['reset_timestamp'] = timezone.now().timestamp()
                
                # Send OTP via email
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}\nThis OTP is valid for 10 minutes.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                messages.success(request, 'OTP has been sent to your email.')
                return redirect('verify_otp')
            except Exception as e:
                messages.error(request, 'Error sending OTP. Please try again.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})

def verify_otp(request):
    if 'reset_otp' not in request.session:
        messages.error(request, 'Please request OTP first')
        return redirect('forgot_password')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            stored_otp = request.session.get('reset_otp')
            timestamp = request.session.get('reset_timestamp')
            
            # Check if OTP is expired (10 minutes)
            current_time = timezone.now().timestamp()
            if current_time - timestamp > 600:
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('forgot_password')
            
            if otp == stored_otp:
                # Clear OTP from session
                del request.session['reset_otp']
                del request.session['reset_timestamp']
                messages.success(request, 'OTP verified successfully')
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid OTP')
    else:
        form = OTPVerificationForm()
    return render(request, 'verify_otp.html', {'form': form})

def reset_password(request):
    if 'reset_email' not in request.session:
        messages.error(request, 'Invalid password reset request')
        return redirect('forgot_password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                email = request.session.get('reset_email')
                user = CustomUser.objects.get(email=email)
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                
                # Clear session data
                del request.session['reset_email']
                
                messages.success(request, 'Password has been reset successfully. Please login with your new password.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'Error resetting password. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})

@login_required
def profile(request):
    folders = ReportFolder.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'folders' : folders,
    }
    return render(request, 'profile.html', context)
