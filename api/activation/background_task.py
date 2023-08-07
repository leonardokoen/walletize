from celery import shared_task
import random
from time import sleep
from api.models import User
from django.core.mail import EmailMessage
import os


@shared_task
def photo_validation(id_front, id_back, selfie, user_id): 
    
    # Simulate the time to complete the task
    sleep(30)
    user = User.objects.get(id = user_id)
    subject = "Walletize Activation Results"
    from_email='walletize_app@protonmail.com'
    to = user.email
    # Simulate Failure
    if not random.choice([0, 1]):
        
        body = ""

        email = EmailMessage(
            subject = subject,
            body = "We could not activate your Account. Try again later!",
            from_email=from_email,
            to = [to]
        )

        os.remove(id_front)
        os.remove(id_back)
        os.remove(selfie)
        return
    
    # Simulate Success
    
    email = EmailMessage(
            subject = subject,
            body = "Your Account is Activated",
            from_email=from_email,
            to = [to]
        )
    
    user.is_active = True
    user.save()
    os.remove(id_front)
    os.remove(id_back)
    os.remove(selfie)
    return