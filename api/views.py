from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note

from django.http import FileResponse, HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics

@api_view(['GET'])
def getNotes(request):

    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getNote(request, pk):

    notes = Note.objects.get(id = pk)
    serializer = NoteSerializer(notes, many = False)
    return Response(serializer.data)


class NoteUpload(APIView):

    
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (permissions.AllowAny,)

    """ @api_view(['POST'])
    def post(self, request, format=None):
        data = request.data
        note = Note.objects.create(body=data['body'])
        serializer = NoteSerializer(note, many = False)
        return Response(serializer.data) """

    def post(self, request, format=None):   

        print(request.data)
        serializer = NoteSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createNote(request):
    data = request.data
    note = Note.objects.create(title=data['title'], body=data['body'], grade=data['grade'])
    serializer = NoteSerializer(note, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateNote(request, pk):
    data = request.data
    note = Note.objects.get(id = pk)
    serializer = NoteSerializer(note, data = request.data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)    

@api_view(['DELETE'])
def deleteNote(request, pk):
    note = Note.objects.get(id = pk)
    note.delete()
    return Response('done') 

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {

            'EP_1_notesList': '/notes/',
            'EP_2_newNote': 'notes/create',
            'EP_3_updNote': 'notes/<str:pk>/update',
            'EP_4_delNote': 'notes/<str:pk>/delete',
            'EP_5_detailNote': 'notes/<str:pk>',
            'EP_6_PDF_gen': 'notes/pdf/<str:pk>',
         
        },

            ]
    return  Response(routes)

@api_view(['GET'])
def gen_pdf(request, pk):
      
    note = Note.objects.get(pk=pk)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    lines = []
        
    lines.append('Body: ' + note.body)
    lines.append("  ")
            
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='report_note.pdf')
