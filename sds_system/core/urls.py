from django.urls import path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('manufacturer', ManufacturerViewSet)
router.register('language', LanguageViewSet)
router.register('product', ProductViewSet)
router.register('producer', ProducerOfSDSViewSet)
router.register('sds', SDSViewSet)

urlpatterns = [
    path('', dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', pivot_data, name='pivot_data'),
]

urlpatterns += router.urls
