"""user_data_login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.conf.urls import include
from django.contrib import admin


def login(request):
    if request.user and request.user.is_authenticated and request.user.is_active and request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index', current_app='admin'))
    else:
        return HttpResponseRedirect(reverse('index', current_app='udl_app'))


admin.site.login = login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('udl_app.urls')),
]
