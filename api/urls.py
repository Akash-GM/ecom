from django.urls import path
from . import views


urlpatterns = [
    path("products/", views.product_list),
    path("products/info/", views.product_info),
    path("products/<int:pk>/", views.ProductDetail.as_view()),
    path("orders/", views.order_list),
]
