from rest_framework import routers

from .api_views import *

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('provider', ProviderViewSet)
router.register('language', LanguageViewSet)
router.register('product', ProductViewSet)

urlpatterns = []

urlpatterns += router.urls
