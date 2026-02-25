from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet


app_name = 'local_pedidos'
api_version = "api/v01/"

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'admin/pedidos', PedidoViewSet, basename='admin-pedidos')


# URLs nueva API RESTFUL
api_urls = [
    path(api_version, include(router.urls)),
]

urlpatterns = router.urls