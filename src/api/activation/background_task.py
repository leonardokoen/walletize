from celery import shared_task
import random
from time import sleep
from api.models import User
from django.core.mail import send_mail
import os

#Decorator that make this function work in background
@shared_task
def photo_validation(id_front, id_back, selfie, user_id): 
    
    # Simulate the time to complete the task
    sleep(30)
    
    user = User.objects.get(id = user_id)
    subject = "Walletize Activation Results"
    from_email='walletizeapp@gmail.com'
    to = user.email
    # Simulate Failure
    if not random.choice([0, 1]):
        
        #Send email
        send_mail(
            subject,
            "We could not activate your Account. Try again later!",
            from_email,
            [to],
            fail_silently=False
        )
        # Delete Temporary Files
        os.remove(id_front)
        os.remove(id_back)
        os.remove(selfie)
        return
    
    # Simulate Success
    send_mail(
            subject,
            "Your Account is Activated",
            from_email,
            [to],
            fail_silently=False
        )
    # Activate User
    user.is_active = True
    user.save()
    # Delete Temporary Files
    os.remove(id_front)
    os.remove(id_back)
    os.remove(selfie)
    return