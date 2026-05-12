from django.urls import path
from . import views

# Mounted at /api/forum/ in finproject/urls.py
urlpatterns = [
    path('threads/',                       views.thread_list,   name='thread_list'),
    path('threads/create/',                views.thread_create, name='thread_create'),
    path('threads/<int:pk>/',              views.thread_detail, name='thread_detail'),
    path('threads/<int:pk>/edit/',         views.thread_edit,   name='thread_edit'),
    path('threads/<int:thread_pk>/replies/', views.reply_create,  name='reply_create'),
    path('replies/<int:pk>/edit/',         views.reply_edit,    name='reply_edit'),
    path('replies/<int:pk>/delete/',       views.reply_delete,  name='reply_delete'),
]
