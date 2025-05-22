from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from meals.models import MealServingLog
from recipes.models import RecipeIngredient
from django.db.models import Sum
from datetime import datetime
from .serializers import NotificationSerializer
from .models import Notification
from .permissions import IsManagerOrAdmin

# Create your views here.

class IngredientConsumptionAPIView(APIView):
    permission_classes = [IsManagerOrAdmin]
    def get(self, request):
        # Группировка по продукту и месяцу
        data = []
        for product in Product.objects.all():
            consumption = MealServingLog.objects.filter(
                recipe__ingredients__product=product
            ).values('served_at__year', 'served_at__month').annotate(
                total_used=Sum('portions')
            ).order_by('served_at__year', 'served_at__month')
            data.append({
                'product': product.name,
                'consumption': list(consumption)
            })
        return Response(data)

class ProductDeliveryDatesAPIView(APIView):
    permission_classes = [IsManagerOrAdmin]
    def get(self, request):
        data = Product.objects.values('name', 'delivery_date', 'quantity')
        return Response(list(data))

class NotificationListAPIView(APIView):
    permission_classes = [IsManagerOrAdmin]
    def get(self, request):
        notifications = Notification.objects.all().order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class NotificationMarkReadAPIView(APIView):
    permission_classes = [IsManagerOrAdmin]
    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk)
            notification.is_read = True
            notification.save()
            return Response({'detail': 'Оповещение отмечено как прочитанное.'})
        except Notification.DoesNotExist:
            return Response({'detail': 'Оповещение не найдено.'}, status=404)
