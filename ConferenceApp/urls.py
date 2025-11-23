from django.urls import path
from . import views

urlpatterns = [
    path('', views.conference_list, name='conference_list'),
    path('create/', views.conference_create, name='conference_create'),
    path('<int:id>/', views.conference_detail, name='conference_detail'),
    path('<int:id>/update/', views.conference_update, name='conference_update'),
    path('<int:id>/delete/', views.conference_delete, name='conference_delete'),
]
