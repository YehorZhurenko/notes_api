from django.urls import path
from . import views

urlpatterns = [

    path('notes/create', views.NoteUpload.as_view()),

    #File_gen
    path('notes/post_gen/<int:pk>', views.post_gen, name = 'post_gen'),
    path('notes/temp_gen/<int:pk>', views.temp_gen, name = 'temp_gen'),
    path('notes/bio_gen/<int:pk>', views.bio_gen, name = 'bio_gen'),
    path('notes/pdf_res/<int:pk>', views.gen_pdf_res, name = 'venue_pdf_res'),
      
    path('', views.getRoutes),
    path('notes/', views.getNotes),
    path('notes/create_no_pic', views.createNote),
    path('notes/<str:pk>/update', views.updateNote),
    path('notes/<str:pk>/delete', views.deleteNote),
    path('notes/<str:pk>', views.getNote),
    path('notes/pdf/<int:pk>', views.gen_pdf, name = 'venue_pdf'),  
   

]