from django.urls import path
from .views import *

urlpatterns = [
    path('', maps_view, name='maps'),
    path('location/<int:history_id>/', delete_history, name='delete_history'),
    path('delete/', delete_page, name='delete_page'),
]
