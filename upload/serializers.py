from rest_framework import serializers
from rest_framework.reverse import reverse

from upload.models import FileModel, ChunkModel


class ChunkedUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileModel
        fields = '__all__'
        read_only_fields = ('status', 'completed_at')



class FileSerializer(serializers.ModelSerializer):
    chunks_count = serializers.SerializerMethodField()

    class Meta:
        model = FileModel
        fields = '__all__'

    def get_chunks_count(self, obj):
        return obj.chunks.count()


class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ["filename"]


class ChunkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChunkModel
        fields = ['order']
    
