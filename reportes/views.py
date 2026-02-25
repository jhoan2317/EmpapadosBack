from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Reporte
from .serializers import ReporteSerializer


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all().order_by('fecha_generacion')
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated]
