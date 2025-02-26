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
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView


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
Generics alternative for above FBVs
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


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)


# CBV API View , alternative to product_info FBV


class ProductInfoAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)


class ProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
