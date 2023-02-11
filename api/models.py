from django.db import models

class Note(models.Model):
    title = models.TextField(default="empty")
    body = models.TextField(default="empty")
    grade = models.IntegerField(default=2)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated']