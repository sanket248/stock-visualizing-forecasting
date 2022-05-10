"""
WSGI config for visualize_forecast_of_stock_price project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visualize_forecast_of_stock_price.settings')

application = get_wsgi_application()
