
from django.shortcuts import render
from .models import register_table
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')       

def register_form_submission(request):
    print("***welcome to register page")
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email_id = request.POST.get('email_id')
    phone_number = request.POST.get('phone_number')
    appointment_time = request.POST.get('appointment_time')
    reason_for_the_appointment = request.POST.get('reason_for_the_appointment')
    print(f"{first_name} {last_name} {email_id} {phone_number} {appointment_time} {reason_for_the_appointment}")
    otp_number = random.randint(0, 99999)  # Changed from 00000 to 0 for consistency
    print(f"otp number is {otp_number}")

    # Save to the database
    ex1 = register_table(
        first_name=first_name,
        last_name=last_name,
        email_id=email_id,
        phone_number=phone_number,
        appointment_time=appointment_time,
        reason_for_the_appointment=reason_for_the_appointment,
        otp_number=otp_number
    )
    ex1.save()
    print(f"data successfully saved")
    
    try:
        subject = 'Hospital Appointment Booking'
        message = f'Hi {first_name} {last_name}, thank you for registering on our appointment booking application.\n Your OTP is -> {otp_number}.\nPlease enter OTP to proceed'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email_id]
        send_mail(subject, message, email_from, recipient_list)
        print("mail sent successfully")
    except Exception as e:
        print("mail not sent. Error:", str(e))

    return render(request, 'login.html')

def login_form_submission(request):
    email_id = request.POST.get('email_id')
    otp_number = request.POST.get('otp_number')
    if register_table.objects.filter(email_id=email_id, otp_number=otp_number).exists():
        print("login successfully")
        logger_data = register_table.objects.get(email_id=email_id, otp_number=otp_number)
        return render(request, 'dashboard.html', {'logger_data': logger_data})
    else:
        print("login failed")
        messages.error(request, 'Please check email or OTP number', extra_tags='failed')
        return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')
