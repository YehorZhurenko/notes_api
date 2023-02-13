from django.db import models
from django.utils.translation import gettext_lazy as _

def upload_to(instance, filename):
    return 'posts/{filename}'. format(filename=filename)

class Note(models.Model):
    title = models.TextField(default="empty")
    body = models.TextField(default="empty")
    grade = models.IntegerField(default=2)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(_("Image"), upload_to=upload_to, default="pic")

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated']