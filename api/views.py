from api.models import Product, Order, OrderItem
from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import (
    ProductSerializer,
    OrderSerializer,
    OrderItemSeralizer,
    ProductInfoSerializer,
)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer]


@api_view(["GET"])
def product_list(request):
    """
    returns list of all products
    like ProductList class
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"data": serializer.data})


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["GET"])
def product_detail(request, pk):
    """
    single product_detail
    """
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def order_list(request):
    """
    returns list of all products
    like ProductList class
    """
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer(
        {
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"],
        }
    )
    return Response(serializer.data)
