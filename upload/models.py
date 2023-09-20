import os.path
import uuid

from django.db import models, transaction
from django.conf import settings
from django.utils import timezone

from upload.utils import convert_size


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def generate_chunk_filename(instance, filename):
    upload_dir = settings.UPLOAD_PATH + "/" + str(instance.file.id)
    filename = os.path.join(upload_dir, f"{str(instance.order)}.part")
    return filename


def generate_file_name(file_id, file_name):
    upload_dir = settings.UPLOAD_PATH + "\\" + str(file_id)
    filename = os.path.join(upload_dir, file_name)
    return filename

class FileModel(models.Model):
    UPLOADING = 1
    COMPLETE = 2
    STATUS_CHOICES = (
        (UPLOADING, 'Incomplete'),
        (COMPLETE, 'Complete'),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    file = models.FileField(
        max_length=255,
        null=True,
    )
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=UPLOADING,
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def delete_file(self):
        if self.file:
            storage, path = self.file.storage, self.file.path
            storage.delete(path)
        self.file = None

    @transaction.atomic
    def delete(self, delete_file=True, *args, **kwargs):
        super().delete(*args, **kwargs)
        if delete_file:
            self.delete_file()

    def __repr__(self):
        return '<{} - upload_id: {} - bytes: 0 - status: {}>'.format(
            self.filename,
            self.id,
            self.status,
        )

    @transaction.atomic
    def completed(self):
        completed_at = timezone.now()
        self.file = self.file_path
        self.status = self.COMPLETE
        self.completed_at = completed_at
        self.save()

    def chunks_size(self):
        return self.chunks.all().aggregate(
            total_size=models.Sum('size')
            )['total_size'] or 0
    
    @property
    def size(self):
        return convert_size(self.chunks_size())

    @property
    def file_path(self):
        return generate_file_name(self.pk, self.filename)


class ChunkModel(models.Model):
    file = models.ForeignKey(
        FileModel, 
        on_delete=models.CASCADE, 
        related_name="chunks"
    )
    chunk = models.FileField(
        max_length=255,
        upload_to=generate_chunk_filename,
        null=True,
    )
    size = models.BigIntegerField()
    order = models.IntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
