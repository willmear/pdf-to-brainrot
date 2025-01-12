from django.urls import path

from . import views

app_name = 'brainrot'
urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_pdf, name="upload_pdf"),
]