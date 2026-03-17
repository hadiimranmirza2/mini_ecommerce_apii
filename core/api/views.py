from rest_framework import viewsets, status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend # Needs pip install django-filter
from rest_framework.filters import SearchFilter

from core.api.models import Category, Product, Order
from core.api.serializers import CategorySerializer, ProductSerializer, OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Challenge #4: Filtering and Search [cite: 48, 49]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Challenge #2: Custom Action for Order Status [cite: 41, 42, 43]
    # This creates the endpoint: /api/orders/{id}/status/ [cite: 34]
    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
    
        valid_choices = ['pending', 'shipped', 'delivered']
    
        if new_status in valid_choices:
            order.status = new_status
            order.save()
            return Response({'status': f'Order is now {new_status}'})
    
        return Response(
           {'error': f'Invalid status. Use: {valid_choices}'}, 
           status=400 # Using the number directly avoids the 'status' name conflict
    )