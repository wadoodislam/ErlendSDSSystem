from django.urls import path, include

from .views import *

urlpatterns = [
    path('api/', include('core.api.urls'), name='core_api'),
    path('search', search, name='search'),

]

