from .views import Home, WriteOne, FindOne, FindMany, EOInterest
from django.urls import path


urlpatterns = [
    path('', Home),
    path('findone/<str:ModelLabel>/<int:pk>', FindOne),
    path('findmany/<str:ModelLabel>', FindMany),
    path('write/<str:ModelLabel>', WriteOne),
    path('eointerest', EOInterest)
]
