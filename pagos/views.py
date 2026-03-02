from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import date as date_type

from .models import Gasto
from .serializers import GastoSerializer

# IMPORTANTE → ingresos vienen de pedidos
from pedidos.models import Pedido


class GastoViewSet(ModelViewSet):
    serializer_class = GastoSerializer

    def get_queryset(self):
        """
        Si viene ?fecha=YYYY-MM-DD filtra ese día.
        Sin fecha devuelve todos los gastos del mes actual (modo Ver Todo).
        """
        fecha_param = self.request.query_params.get("fecha")
        qs = Gasto.objects.all()

        if fecha_param:
            try:
                dia = date_type.fromisoformat(fecha_param)
                qs = qs.filter(fecha=dia)
            except ValueError:
                pass
        else:
            hoy = timezone.now().date()
            qs = qs.filter(fecha__year=hoy.year, fecha__month=hoy.month)

        return qs.order_by("-fecha")


@api_view(["GET"])
def reporte_hoy(request):
    # Fecha del query param o hoy por defecto (igual que Reportes)
    fecha_param = request.query_params.get("fecha")
    try:
        hoy = date_type.fromisoformat(fecha_param) if fecha_param else timezone.now().date()
    except ValueError:
        hoy = timezone.now().date()

    if fecha_param:
        # Día específico seleccionado
        ingresos = (
            Pedido.objects
            .filter(fecha__date=hoy, estado='pagado')
            .aggregate(total=Sum("total"))["total"] or 0
        )
        gastos = (
            Gasto.objects
            .filter(fecha=hoy)
            .aggregate(total=Sum("monto"))["total"] or 0
        )
    else:
        # Ver Todo → acumula el mes completo
        ingresos = (
            Pedido.objects
            .filter(fecha__year=hoy.year, fecha__month=hoy.month, estado='pagado')
            .aggregate(total=Sum("total"))["total"] or 0
        )
        gastos = (
            Gasto.objects
            .filter(fecha__year=hoy.year, fecha__month=hoy.month)
            .aggregate(total=Sum("monto"))["total"] or 0
        )

    ganancia = ingresos - gastos

    return Response({
        "ingresos": ingresos,
        "gastos": gastos,
        "ganancia": ganancia
    })
