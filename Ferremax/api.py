from .models import producto
from rest_framework import viewsets, permissions, generics
from .serializers import ProductoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductoFilter

""" class ProductoViewSet(viewsets.ModelViewSet):
  queryset = producto.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = ProductoSerializer """

class ProductoListView(generics.ListAPIView):
    queryset = producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductoFilter


class ProductoDetailView(generics.RetrieveAPIView):
    queryset = producto.objects.all()
    serializer_class = ProductoSerializer


class ProductoUpdateView(generics.UpdateAPIView):
    queryset = producto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductoSerializer