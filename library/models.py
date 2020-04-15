import os

from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    alt_text = models.CharField(max_length=200)
    image = models.FileField(upload_to="svg/")
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def filename(self):
        name = os.path.basename(self.image.name)
        return os.path.splitext(name)[0]

    def __str__(self):
        return self.title
