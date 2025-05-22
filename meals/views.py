from django.shortcuts import render
from django.db import transaction
from django.core.exceptions import ValidationError
from inventory.models import Product, Notification
from recipes.models import Recipe, RecipeIngredient
from .models import MealServingLog
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ServeMealSerializer, MealServingLogSerializer
from datetime import datetime
from django.db.models import Sum
from .permissions import IsChefOrAdmin
from inventory.permissions import IsManagerOrAdmin

# Create your views here.

def serve_meal(recipe_id, portions, user):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    products_to_update = []
    # Проверка наличия ингредиентов
    for ingredient in ingredients:
        required_qty = ingredient.quantity * portions
        if ingredient.product.quantity < required_qty:
            raise ValidationError(f"Недостаточно продукта: {ingredient.product.name}")
        products_to_update.append((ingredient.product, required_qty))
    # Списание ингредиентов
    with transaction.atomic():
        for product, required_qty in products_to_update:
            product.quantity -= required_qty
            product.save()
            # Оповещение, если остаток ниже min_threshold
            if product.quantity < product.min_threshold:
                Notification.objects.create(
                    message=f'Остаток продукта "{product.name}" ниже минимума: {product.quantity} г',
                    user=None
                )
        MealServingLog.objects.create(
            recipe=recipe,
            user=user,
            portions=portions
        )

class ServeMealAPIView(APIView):
    permission_classes = [IsChefOrAdmin]
    def post(self, request):
        serializer = ServeMealSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serve_meal(
                    recipe_id=serializer.validated_data['recipe_id'],
                    portions=serializer.validated_data['portions'],
                    user=request.user
                )
                return Response({'detail': 'Блюдо успешно подано!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MealServingLogListAPIView(APIView):
    permission_classes = [IsChefOrAdmin|IsManagerOrAdmin]
    def get(self, request):
        logs = MealServingLog.objects.all().order_by('-served_at')
        serializer = MealServingLogSerializer(logs, many=True)
        return Response(serializer.data)

class MonthlyReportAPIView(APIView):
    permission_classes = [IsManagerOrAdmin]
    def get(self, request):
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
        served = MealServingLog.objects.filter(
            served_at__year=year, served_at__month=month
        ).aggregate(total=Sum('portions'))['total'] or 0
        possible = 0
        for recipe in Recipe.objects.all():
            possible += recipe.possible_portions()
        percent = 0
        flag = False
        if possible > 0:
            percent = abs(served - possible) / possible * 100
            flag = percent > 15
            if flag:
                Notification.objects.create(
                    message=f'Отклонение между приготовленными и возможными порциями за {month}.{year} составило {round(percent,2)}%',
                    user=None
                )
        return Response({
            'year': year,
            'month': month,
            'served_portions': served,
            'possible_portions': possible,
            'percent_difference': round(percent, 2),
            'flag': flag
        })
