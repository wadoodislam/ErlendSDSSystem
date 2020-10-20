from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('manufacturer', ManufacturerViewSet)
router.register('language', LanguageViewSet)
router.register('product', ProductViewSet)
router.register('producerofsds', ProducerOfSDSViewSet)
router.register('sds', SDSViewSet)

urlpatterns = router.urls
