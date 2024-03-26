from django.urls import path
from .views import image_view

urlpatterns = [
    path('photos/<str:image_name>/', image_view, name='image_view'),
]