from rest_framework.routers import DefaultRouter

from views.shorturl import ShortURLView

router = DefaultRouter()
router.register(r'shorturl', ShortURLView, basename='shorturl')

urlpatterns = router.urls