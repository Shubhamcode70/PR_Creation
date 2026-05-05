from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pr/new/', views.pr_create, name='pr_create'),
    path('pr/<int:pk>/', views.pr_detail, name='pr_detail'),
    path('pr/<int:pk>/approve/', views.pr_approve, name='pr_approve'),
]
