from django.urls import path, include

from .views import *

urlpatterns = [
    path('api/', include('core.api.urls'), name='core_api'),
    path('harvest/run/<slug:id>', run_harvest, name='run'),
    path('match/<int:id>', match, name='match'),
    path('match/pair/<int:wishlist_id>', pair, name='pair'),
]

