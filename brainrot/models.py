from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

class Video(models.Model):
    video_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='videos_uploaded', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    user = models.ForeignKey(User,on_delete= models.CASCADE)

    def __str__(self):
        return self.video_name


class Pdf(models.Model):
    upload_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='pdfs', null=True, blank=True)
    user = models.ForeignKey(User,on_delete= models.CASCADE)