from rest_framework.routers import DefaultRouter

from views.user import UserView

router = DefaultRouter()
router.register('user', UserView, basename='user')

urlpatterns = router.urls