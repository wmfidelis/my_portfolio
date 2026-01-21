# apps/portfolio_site/utils.py
import threading
from django.core.mail import send_mail

def send_email_async(subject, message, from_email, recipient_list, fail_silently=True):
    """Send an email in a separate thread to avoid blocking Gunicorn workers."""
    threading.Thread(
        target=send_mail,
        args=(subject, message, from_email, recipient_list),
        kwargs={'fail_silently': fail_silently}
    ).start()
