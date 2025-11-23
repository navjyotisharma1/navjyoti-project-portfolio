from django.db import models

class UploadedDocument(models.Model):
    file = models.FileField(upload_to='uploads/')
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file.name
