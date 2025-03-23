from django.urls import path
from .views import doctor_register, doctor_login, doctor_logout, generate_slots, save_slots, view_slots, cancel_slot, view_appointments  
urlpatterns = [
    path("register/", doctor_register, name="doctor_register"), 
    path("login/", doctor_login, name="doctor_login"),
    path("logout/", doctor_logout, name="doctor_logout"),
    path("generate_slots/", generate_slots, name="generate_slots"),
    path("save_slots/", save_slots, name="save_slots"),
    path("view_slots/", view_slots, name="view_slots"),
    path("cancel_slot/<int:slot_id>/", cancel_slot, name="cancel_slot"),
    path('appointments/', view_appointments, name='view_appointments'),
]
