from django.urls import path
from . import views

urlpatterns = [

    path('', views.getRoutes),
    path('notes/', views.getNotes),
    path('notes/create', views.createNote),
    path('notes/<str:pk>/update', views.updateNote),
    path('notes/<str:pk>/delete', views.deleteNote),
    path('notes/<str:pk>', views.getNote),
    path('notes/pdf/<int:pk>', views.gen_pdf, name = 'venue_pdf')
    
]