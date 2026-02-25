from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import GastoViewSet, reporte_hoy

router = DefaultRouter()
router.register(r"gastos", GastoViewSet, basename="gastos")

urlpatterns = [
    path("reporte-hoy/", reporte_hoy),
]

urlpatterns += router.urls
