from django.urls import path
from upload.views import FileCreateView, ChunkUploadView, CompleteUploadView



urlpatterns = [
    path("", FileCreateView.as_view(), name="upload-create"),
    path("<str:pk>", ChunkUploadView.as_view(), name="upload-chunk"),
    path("complete/<str:pk>", CompleteUploadView.as_view(), name="upload-complete")
]
