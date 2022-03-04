import os

from pathlib import Path

from django.conf import settings as dj_settings


class BaseFileUploadBackend:

    @classmethod
    def upload(cls, file, file_name):
        pass

    @classmethod
    def remove(cls, file_name):
        pass


class LocalFileUploadBackend:

    @classmethod
    def get_upload_root_directory(self):
        return dj_settings.MEDIA_ROOT

    @classmethod
    def upload(cls, file, file_name):
        file_name = cls.get_upload_root_directory() + file_name
        path = Path(file_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('wb') as f:
            f.write(file)

    @classmethod
    def remove(cls, file_name):
        file_name = cls.get_upload_root_directory() + file_name
        try:
            os.remove(file_name)
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}.')
