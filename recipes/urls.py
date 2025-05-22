from django.urls import path
from .views import RecipeListAPIView

urlpatterns = [
    path('list/', RecipeListAPIView.as_view(), name='recipe-list'),
] 