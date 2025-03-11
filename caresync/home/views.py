from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientRegistrationForm, PatientLoginForm
from django.contrib.auth import login
from .models import Patient
from django.contrib.auth.hashers import check_password


def home(request):
    return render(request, 'home.html')

def register_patient(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! 🎉")
            return redirect("login")  # Redirect to login page
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PatientRegistrationForm()
    
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            password = form.cleaned_data.get("password")

            try:
                patient = Patient.objects.get(name=name)  # Fetch user by name
                if check_password(password, patient.password):  # Check password manually
                    # Store user session manually instead of using Django's login()
                    request.session["patient_id"] = patient.id  # Store user ID in session
                    request.session["patient_name"] = patient.name  # Store user name
                    messages.success(request, "Login successful! 🎉")
                    return redirect("home")  # Redirect to home after login
                else:
                    messages.error(request, "Invalid credentials. Please try again.")
            except Patient.DoesNotExist:
                messages.error(request, "No account found with this name.")
        else:
            messages.error(request, "Please enter valid details.")

    else:
        form = PatientLoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    request.session.flush()  # Clear the session
    messages.success(request, "Logged out successfully! ✅")
    return redirect("home") 