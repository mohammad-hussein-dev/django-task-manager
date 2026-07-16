from rest_framework.routers import DefaultRouter

from api.views import TaskViewSet

router = DefaultRouter()

router.register(
    r"tasks",
    TaskViewSet,
    basename="task",
)

urlpatterns = router.urls
