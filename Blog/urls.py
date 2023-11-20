from .views import (
    AddComment, FindOne, FindMany, Home, HomeWebsite, NoSuchTable, NoSuchObject,
    Search, SubscribeToNewLetter, UnSubscribeToNewLetter, ContactUs
)
from django.urls import path


urlpatterns = [
    path('', Home),
    path('view', HomeWebsite),
    path('search', Search),
    path('notable/<str:model>', NoSuchTable, name='no_such_table'),
    path('noobject/', NoSuchObject, name='no_such_object'),
    path('findone/<str:ModelLabel>/<int:pk>', FindOne),
    path('findmany/<str:ModelLabel>', FindMany),
    path('comment_on_post/<int:pk>', AddComment),
    path('subscribe-newsletter', SubscribeToNewLetter),
    path('unsubscribe-newsletter', UnSubscribeToNewLetter),
    path('contactus', ContactUs)
]
