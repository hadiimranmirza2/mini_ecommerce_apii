from rest_framework import serializers
from .models import Category, Product, Order, OrderItem



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        # we make slug read_only mecause model auto-generates it 
        read_only_fields =['slug']



class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ['id', 'name', 'price', 'stock_quantity', 'category', 'created_at']     
        read_only_fields = ['created_at']



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']       


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True) 

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'created_at', 'status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            # Fix: Use item_data (the loop variable)
            product = item_data['product'] 
            quantity = item_data['quantity'] 

            # Challenge 3: Stock Validation [cite: 45-47]
            if product.stock_quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. Available: {product.stock_quantity}"
                )           

            product.stock_quantity -= quantity
            product.save()

            OrderItem.objects.create(order=order, **item_data)

        return order