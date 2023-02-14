from django.db import models
from django.utils.translation import gettext_lazy as _

def upload_to(instance, filename):
    return 'posts/{filename}'. format(filename=filename)

    

class Note(models.Model):
    title = models.TextField(default="empty")
    content_1 = models.TextField(default="empty")
    content_2 = models.TextField(default="empty")
    content_3 = models.TextField(default="empty")
    grade_1 = models.IntegerField(default=0)
    grade_2 = models.IntegerField(default=0)
    grade_3 = models.IntegerField(default=0)
    image_1 = models.ImageField(_("Image"), upload_to=upload_to, default="pic")
    image_2 = models.ImageField(_("Image"), upload_to=upload_to, default="pic")
    image_3 = models.ImageField(_("Image"), upload_to=upload_to, default="pic")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated']