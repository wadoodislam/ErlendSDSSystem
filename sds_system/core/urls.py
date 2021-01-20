from django.urls import path, include

from .views import *

urlpatterns = [
    path('api/', include('core.api.urls'), name='core_api'),
    path('search', search, name='search'),
    path('', dashboard_with_pivot, name='dashboard_with_pivot'),
]

