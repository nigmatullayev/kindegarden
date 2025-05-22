from .models import Recipe
from rest_framework import serializers

class RecipeSerializer(serializers.ModelSerializer):
    possible_portions = serializers.SerializerMethodField()
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'possible_portions']

    def get_possible_portions(self, obj):
        return obj.possible_portions() 