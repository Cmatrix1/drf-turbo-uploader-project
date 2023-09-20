from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import HttpRequest

from upload.models import FileModel, ChunkModel
from upload.serializers import FileCreateSerializer, FileSerializer, ChunkCreateSerializer
from upload.exceptions import ChunkedUploadError
from upload.utils import write_chunks_in_file


class FileCreateView(APIView):
    model = FileModel
    serializer_class = FileCreateSerializer
    response_serializer_class = FileSerializer

    def post(self, request: HttpRequest):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        file = serializer.save()
        data = self.response_serializer_class(file).data
        return Response(status=status.HTTP_200_OK, data=data)


class ChunkUploadView(APIView):
    model = ChunkModel
    serializer_class = ChunkCreateSerializer
    response_serializer_class = FileSerializer
    file_field_name = "file"
    max_bytes = 100_000_000

    def post(self, request: HttpRequest, pk: str):
        try:
            # Add Extra Logic ...
            return self._post(request, pk)
        except ChunkedUploadError as exp:
            return Response(status=exp.status_code, data=exp.data)

    def validate_max_bytes(self, chunk_size: int, file: FileModel):
        if chunk_size + file.chunks_size() > self.max_bytes:
            raise ChunkedUploadError(status=status.HTTP_400_BAD_REQUEST,
                                     detial=f"Size of file exceeds the limit ({self.max_bytes} bytes)")

    def validate_chunk_file(self, request_data) -> InMemoryUploadedFile:
        chunk = request_data.get(self.file_field_name)
        if chunk:
            return chunk
        raise ChunkedUploadError(status=status.HTTP_400_BAD_REQUEST,
                                 detial='No chunk file was submitted')
    
    def validate_order(self, file: FileModel, order: int):
        if file.chunks.filter(order=order).exists():
            raise ChunkedUploadError(status=status.HTTP_400_BAD_REQUEST,
                                detial='A chunk with this order already exists')


    def _post(self, request: HttpRequest, pk: str):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = get_object_or_404(FileModel.objects.only("pk"), pk=pk)
        
        self.validate_order(file, serializer.validated_data.get("order"))
        chunk = self.validate_chunk_file(request.data)
        self.validate_max_bytes(chunk.size, file)

        chunk_object = serializer.save(file=file, size=chunk.size, chunk=chunk)
        file.chunks.add(chunk_object)
        file.save()

        return Response(
            self.response_serializer_class(file).data,
            status=status.HTTP_200_OK,
        )


class CompleteUploadView(APIView):
    model = FileModel
    response_serializer_class = FileSerializer

    def get(self, request: HttpRequest, pk: str):
        try:
            file = self._get(request, pk)
            return Response(
                self.response_serializer_class(file).data,
                status=status.HTTP_200_OK,
            )
        except ChunkedUploadError as exp:
            return Response(status=exp.status_code, data=exp.data)

    def get_file_chunks(self, file: FileModel) -> list[ChunkModel]:
        chunks = file.chunks.order_by("order").all()
        if chunks.exists():
            return chunks
        raise ChunkedUploadError(status=status.HTTP_404_NOT_FOUND,
                                 detail='No chunks found for this file')

    def _get(self, request: HttpRequest, pk: str) -> FileModel:
        file = get_object_or_404(FileModel, pk=pk)
        if file.status == 2:
            raise ChunkedUploadError(status=status.HTTP_204_NO_CONTENT,
                                     detail='File already completed')

        chunks = self.get_file_chunks(file)
        file_writer = write_chunks_in_file(file.file_path)
        for chunk_object in chunks:
            file_writer.send(chunk_object.chunk.read())
            chunk_object.chunk.delete()
        file_writer.close()

        file.completed()

        return file