from datetime import timedelta

from django.conf import settings


# Path where uploading files will be stored until completion
DEFAULT_UPLOAD_PATH = 'chunked_uploads'
UPLOAD_PATH = getattr(settings, 'upload_PATH', DEFAULT_UPLOAD_PATH)


# File extensions for upload files
COMPLETE_EXT = getattr(settings, 'upload_COMPLETE_EXT', '.done')
INCOMPLETE_EXT = getattr(settings, 'upload_INCOMPLETE_EXT', '.part')

# Storage system
STORAGE = getattr(settings, 'upload_STORAGE_CLASS', lambda: None)()

# Boolean that defines if the ChunkedUpload model is abstract or not
ABSTRACT_MODEL = getattr(settings, 'upload_ABSTRACT_MODEL', False)

# Boolean that defines if users beside the creator can access an upload record
USER_RESTRICTED = getattr(settings, "upload_USER_RESTRICTED", True)

# Max amount of data (in bytes) that can be uploaded. `None` means no limit
DEFAULT_MAX_BYTES = None
MAX_BYTES = getattr(settings, 'upload_MAX_BYTES', DEFAULT_MAX_BYTES)

