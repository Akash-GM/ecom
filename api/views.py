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


@api_view(["GET"])
def product_list(request):
    """
    returns list of all products
    like ProductList class
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"data": serializer.data})


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
    orders = Order.objects.prefetch_related("items", "items__product")
    # add "items" or not it will anyway be prefetched when "items__product"
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


"""
Generics
"""


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    # queryset = Product.objects.filter(stock__gt=0)
    # if you wanna filter out something

    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    # by default it will look for pk argument in the url
    # if in the url its something else (like product_id) then you have to
    # mention that in the lookup_url_kwarg


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
