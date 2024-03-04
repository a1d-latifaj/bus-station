import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import VerificationToken

def verify_account(user, code):
    """Verify the user's account using the verification code."""
    try:
        verification_token = VerificationToken.objects.get(user=user, token=code, is_active=True)
        user.is_active = True
        user.save()
        verification_token.is_active = False
        verification_token.save()
        return True
    except VerificationToken.DoesNotExist:
        return False

def generate_verification_code(length=6):
    """Generate a random verification code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_verification_email(email, code):
    """Send a verification email with the verification code."""
    subject = 'Account Verification'
    message = f'Hello,\n\nYour verification code is: {code}\n\nPlease use this code to verify your account.\n\nThank you!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
