"""
WSGI config for my_portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_portfolio.settings')

application = get_wsgi_application()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Serve static files (already works if you have WhiteNoise configured)
application = WhiteNoise(
    application,
    root=str(BASE_DIR / 'staticfiles'),  # static files collected via collectstatic
    prefix='static/'
)

# Serve media files (user-uploaded blog images)
application.add_files(
    str(BASE_DIR / 'media'),  # MEDIA_ROOT
    prefix='media/'            # MEDIA_URL
)
