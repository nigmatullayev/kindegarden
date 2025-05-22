from .models import Recipe, RecipeIngredient
from django.contrib import admin
from meals.views import serve_meal
from django import forms
from django.contrib import messages
import os
from django.conf import settings
from django.template.loader import render_to_string

class ServeMealForm(forms.Form):
    portions = forms.IntegerField(min_value=1, label='Количество порций')

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'possible_portions_display')
    search_fields = ('name',)
    inlines = [RecipeIngredientInline]
    actions = ['serve_meal_action']

    def possible_portions_display(self, obj):
        return obj.possible_portions()
    possible_portions_display.short_description = 'Возможных порций'

    def serve_meal_action(self, request, queryset):
        if 'apply' in request.POST:
            portions = int(request.POST['portions'])
            for recipe in queryset:
                try:
                    serve_meal(recipe.id, portions, request.user)
                    self.message_user(request, f'Блюдо "{recipe.name}" подано ({portions} порций).', messages.SUCCESS)
                except Exception as e:
                    self.message_user(request, f'Ошибка для "{recipe.name}": {e}', messages.ERROR)
            return
        return self._serve_meal_form(request, queryset)
    serve_meal_action.short_description = 'Подать выбранные блюда (списать продукты)'

    # def _serve_meal_form(self, request, queryset):
    #     form = ServeMealForm()
    #     context = {'recipes': queryset, 'form': form}
    #     return render_to_string('admin/serve_meal_action.html', context=context, request=request)

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'product', 'quantity')
    list_filter = ('recipe', 'product')
