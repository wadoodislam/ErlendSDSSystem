from django.urls import path, include
from rest_framework import routers

from .views import *


urlpatterns = [
    path('api/', include('core.api.urls'), name='core_api'),
    path('', dashboard_with_pivot, name='dashboard_with_pivot'),
]

