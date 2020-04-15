from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<int:image_id>", views.detail, name="detail"),
    path("download/<int:image_id>/<str:color>", views.download, name="download"),
]
