from rest_framework import serializers
from .models import MealServingLog

class ServeMealSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()
    portions = serializers.IntegerField(min_value=1)

class MealServingLogSerializer(serializers.ModelSerializer):
    recipe = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    class Meta:
        model = MealServingLog
        fields = ['id', 'recipe', 'user', 'served_at', 'portions'] 