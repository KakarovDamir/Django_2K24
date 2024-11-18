from rest_framework.routers import DefaultRouter
from .views import GradeViewSet

router = DefaultRouter()
router.register(r'grades', GradeViewSet)

urlpatterns = router.urls

