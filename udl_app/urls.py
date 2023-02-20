from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register_view'),
    path('logout/', views.user_logout, name='logout'),
    path('<username>/', views.UserDetailView.as_view(), name='user_profile_page'),
]
