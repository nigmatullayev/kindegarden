from django.urls import path
from .views import IngredientConsumptionAPIView, ProductDeliveryDatesAPIView, NotificationListAPIView, NotificationMarkReadAPIView

urlpatterns = [
    path('consumption/', IngredientConsumptionAPIView.as_view(), name='ingredient-consumption'),
    path('deliveries/', ProductDeliveryDatesAPIView.as_view(), name='product-deliveries'),
    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', NotificationMarkReadAPIView.as_view(), name='notification-mark-read'),
] 