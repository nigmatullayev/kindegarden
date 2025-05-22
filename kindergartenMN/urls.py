"""
URL configuration for kindergartenMN project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import UserListAPIView
from django.contrib.auth.decorators import login_required
from kindergartenMN import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/meals/', include('meals.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/users/', UserListAPIView.as_view(), name='user-list'),
    path('inventory/', login_required(TemplateView.as_view(template_name='inventory.html')), name='inventory'),
    path('reports/', login_required(TemplateView.as_view(template_name='reports.html')), name='reports'),
    path('users/', login_required(TemplateView.as_view(template_name='users.html')), name='users'),
    path('dashboard/', login_required(TemplateView.as_view(template_name='dashboard.html')), name='dashboard'),
    path('', login_required(TemplateView.as_view(template_name='dashboard.html')), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
