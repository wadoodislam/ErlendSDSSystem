from rest_framework import routers
from django.urls import path, include

from .api_views import *

router = routers.DefaultRouter()
router.register('user', UserViewSet)
# router.register('provider', ProviderViewSet)
router.register('language', LanguageViewSet)
router.register('product', ProductViewSet)
# router.register('producer', ProducerOfSDSViewSet)

urlpatterns = [
    path('', dashboard_with_pivot, name='dashboard_with_pivot'),
]

urlpatterns += router.urls
