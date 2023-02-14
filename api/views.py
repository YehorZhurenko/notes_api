import os
from rest_framework.decorators import api_view
from rest_framework.response import Response

from notes.settings import BASE_DIR
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

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from fpdf import FPDF 

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

            'BIO пофиль': '/notes/post_gen/<int:pk>',
            'На подобии визитки ADA': '/notes/temp_gen/<int:pk>',
            'Статья': '/notes/bio_gen/<int:pk>',
                     
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
        
    lines.append('Body: ' + note.content_1)
    lines.append("  ")
            
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='report_note.pdf')


@api_view(['GET'])
def gen_pdf_res(request, pk):
      
    note = Note.objects.get(pk=pk)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
   
    c.scale(1,1)
    c.saveState()

    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    lines = []

    c.setFillColorRGB(0,0,255)
    c.setFont("Courier-Bold", 18)
    c.drawCentredString(160,40, note.title)

    #lines.append('Body: ' + note.content_1)
    lines.append("  ")
            
    c.rotate(180)

    c.drawInlineImage(str(BASE_DIR) + "/media/posts/pic1.jpg", x=-250, y=-450, width = 200, height = 200)

    c.drawInlineImage(str(BASE_DIR) + "/media/posts/pic2.jpg", x=-300, y=-425, width = 70, height = 70)
    c.drawInlineImage(str(BASE_DIR) + "/media/posts/pic2.jpg", x=-230, y=-425, width = 70, height = 70)
    c.drawInlineImage(str(BASE_DIR) + "/media/posts/pic2.jpg", x=-160, y=-425, width = 70, height = 70)
    c.drawInlineImage(str(BASE_DIR) + "/media/posts/pic2.jpg", x=-90, y=-425, width = 70, height = 70)
    c.drawInlineImage(str(BASE_DIR) + "/media/posts/pic2.jpg", x=-370, y=-425, width = 70, height = 70)

    c.restoreState()

    c.showPage()
    c.save()
    buf.seek(0)

    os.remove(str(BASE_DIR) + "/media/posts/pic1.jpg")
    os.remove(str(BASE_DIR) + "/media/posts/pic2.jpg")
    os.remove(str(BASE_DIR) + "/media/posts/pic3.jpg")

    return FileResponse(buf, as_attachment=True, filename='report_note.pdf')

@api_view(['GET'])
def bio_gen(request, pk):
      
    note = Note.objects.get(pk=pk)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("arial", "B", 16)
    pdf.set_text_color(86,86,86) 

    spec = "Instructor"
    u_name = str(note.content_1)
    job = str(note.content_2)
    first_col = "Total students"
    second_col = "Reviews"
    first_col_number = str(note.grade_1)
    second_col_number = str(note.grade_2)
    about = str(note.content_3)
    TW_contact = "@BradColboW_tw"
    FB_contact = "@fb_BradColboW"

    #Spec
    pdf.set_xy(15, 32)
    pdf.multi_cell(w=80, h=8, border=0, txt = spec)

    #Name
    pdf.set_text_color(62,62,62)    
    pdf.set_font("arial", "B", 32)
    pdf.set_text_color(0,0,0) 
    pdf.set_xy(14.5, 40)
    pdf.multi_cell(w=80, h=12, border=0, txt = u_name)

    #Job
    pdf.set_font("arial", "B", 16)
    pdf.set_text_color(0,0,0) 
    pdf.set_xy(15, 53)
    pdf.multi_cell(w=105, h=12, border=0, txt = job)

    #Stats
    pdf.set_font("arial", "B", 14)
    pdf.set_text_color(86,86,86) 
    pdf.set_xy(15, 70)
    pdf.multi_cell(w=105, h=12, border=0, txt = first_col)
    pdf.set_xy(60, 70)
    pdf.multi_cell(w=105, h=12, border=0, txt = second_col)
    pdf.set_font("arial", "B", 24)
    pdf.set_text_color(0,0,0) 
    pdf.set_xy(15, 79)
    pdf.multi_cell(w=105, h=12, border=0, txt = first_col_number)
    pdf.set_xy(60, 79)
    pdf.multi_cell(w=105, h=12, border=0, txt = second_col_number)

    #About
    pdf.set_xy(85, 120)
    pdf.multi_cell(w=105, h=12, border=0, txt = "About me")
    pdf.set_xy(20, 145)
    pdf.set_font("arial", "", 14)
    pdf.multi_cell(w=170, h=10, border=0,  txt = about, align = "M")
    pdf.image(str(BASE_DIR) + "/media/icons/TW_logo.png", 90,250, w=15, h=15)
    pdf.image(str(BASE_DIR) + "/media/icons/FB_logo.png", 102,260, w=13, h=13)

    #Contact
    pdf.set_font("arial", "", 14)
    pdf.set_text_color(86,86,86) 
    pdf.set_xy(43, 251)
    pdf.multi_cell(w=105, h=12, border=0, txt = TW_contact)
    pdf.set_xy(120, 261)
    pdf.multi_cell(w=105, h=12, border=0, txt = FB_contact)

    #Icon
    im_size = 1.4
    pdf.image(str(BASE_DIR) + "/media/posts/pic1.jpg", 130,25, w=45*im_size, h=50*im_size)

    pdf.output(str(BASE_DIR) + "/media/posts/Bio.pdf")

    os.remove(str(BASE_DIR) + "/media/posts/pic1.jpg")
    os.remove(str(BASE_DIR) + "/media/posts/pic2.jpg")
    os.remove(str(BASE_DIR) + "/media/posts/pic3.jpg")

    return FileResponse(open(str(BASE_DIR) + "/media/posts/Bio.pdf", 'rb'))
   
@api_view(['GET'])
def post_gen(request, pk):
      
    note = Note.objects.get(pk=pk)

    pdf = FPDF()
    pdf.add_page()

    text1 = "WORTEX CO. CASE STUDY"
    text2 = note.content_1
    text3 = "OVERVIEW"
    text4 = note.content_2
    text5 = note.content_3
    text6 = "Quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo"

    pdf.set_fill_color(227, 186, 7)
    pdf.set_draw_color(41, 53, 50)
    pdf.rect(0, 0, 210, 100, 'F')

    pdf.set_font("Helvetica", "B", 34   )
    pdf.set_xy(25, 23)
    pdf.multi_cell(w=80, h=14, border=0, align = "L", txt=text1)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_xy(25, 56)
    pdf.multi_cell(w=80, h=6, border=0, align = "L", txt=text2)

    pdf.set_fill_color(62, 62, 62)
    pdf.set_draw_color(41, 53, 50)
    pdf.rect(0, 100, 210, 200, 'F')

    pdf.set_font("Helvetica", "B", 34)
    pdf.set_text_color(235, 235, 235)
    pdf.set_xy(25, 115)
    pdf.multi_cell(w=75, h=20, border=0, align = "L", txt = text3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(25, 140)
    pdf.multi_cell(w=75, h=8, border=0, align = "L", txt = text4)

    pdf.set_text_color(227, 186, 7)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_xy(110, 140)
    pdf.multi_cell(w=75, h=8, border=0, align = "L", txt = text5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(235, 235, 235)
    pdf.set_xy(110, 220)
    pdf.multi_cell(w=75, h=6, border=0, align = "L", txt = text6)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(235, 235, 235)
    pdf.set_xy(32, 270)
    pdf.multi_cell(w=150, h=6, border=0, align = "L", txt = text6)

    pdf.output(str(BASE_DIR) + "/media/posts/Post.pdf")

    os.remove(str(BASE_DIR) + "/media/posts/pic1.jpg")
    os.remove(str(BASE_DIR) + "/media/posts/pic2.jpg")
    os.remove(str(BASE_DIR) + "/media/posts/pic3.jpg")

    return FileResponse(open(str(BASE_DIR) + "/media/posts/Post.pdf", 'rb'))
    

@api_view(['GET'])
def temp_gen(request, pk):
      
    note = Note.objects.get(pk=pk)

    pdf = FPDF(orientation="landscape", format="A5")
    pdf.add_page()
    pdf.set_font("arial", "B", 9)
    pdf.set_text_color(0,0,0) 

    text_upper = note.content_1
    text_lower = note.content_2
    numb1 = str(note.grade_1)
    numb2 = str(note.grade_2)
    numb3 = str(note.grade_3)


    #Upper text block
    pdf.set_xy(115, 20)
    pdf.multi_cell(w=80, h=6, border=0, align = 'center', txt = text_upper)

    #Lower text block
    pdf.set_xy(10,100)
    pdf.multi_cell(w=190, h=5.6, border=0, align = 'center', txt = text_lower)

    #Dec_upper
    x=2.5
    y=0.5
    descr_up = -3

    pdf.set_font("arial", "B", 20)
    pdf.set_text_color(209,72,72) 

    pdf.set_xy(115,75)
    pdf.multi_cell(w=22+x, h=6+y, border=0, txt = numb1)
    pdf.set_xy(140+x,75)
    pdf.multi_cell(w=22+x, h=6+y, border=0, txt = numb1)
    pdf.set_xy(165+2*x,75)
    pdf.multi_cell(w=22+x, h=6+y, border=0, txt = numb1)

    #Descr_lover

    pdf.set_font("arial", "B", 9)
    pdf.set_text_color(0,0,0) 

    pdf.set_xy(115,83+y+descr_up)   
    pdf.multi_cell(w=18+x, h=6+y, border=0, txt = "experience")
    pdf.set_xy(140+x,83+y+descr_up)
    pdf.multi_cell(w=16+x, h=6+y, border=0, txt = "projects")
    pdf.set_xy(165+2*x,83+y+descr_up)
    pdf.multi_cell(w=20+x, h=6+y, border=0, txt = "happy clients")

    #Logo
    pdf.set_xy(15, 20)
    pdf.multi_cell(w=80, h=63, border=0, )
    pdf.image(str(BASE_DIR) + "/media/posts/pic1.jpg", 30,19, w=65, h=65)

    pdf.output(str(BASE_DIR) + "/media/posts/Temp.pdf")

    os.remove(str(BASE_DIR) + "/media/posts/pic1.jpg")
    os.remove(str(BASE_DIR) + "/media/posts/pic2.jpg")
    os.remove(str(BASE_DIR) + "/media/posts/pic3.jpg")

    return FileResponse(open(str(BASE_DIR) + "/media/posts/Temp.pdf", 'rb'))