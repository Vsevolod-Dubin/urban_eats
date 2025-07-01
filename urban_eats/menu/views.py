# menu/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Category, Dish, Order
from .serializers import (
    CategorySerializer,
    DishSerializer,
    OrderSerializer,
    RegisterSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishListView(generics.ListAPIView):
    queryset = Dish.objects.select_related("category").all()
    serializer_class = DishSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
