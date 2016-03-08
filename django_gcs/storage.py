import StringIO
import mimetypes
from django.conf import settings
from django.core.files.storage import Storage
from gcloud import storage, exceptions


class GoogleCloudStorage(Storage):
    def __init__(self, bucket=None, project=None, credentials=None, http=None):
        """
        :type bucket_name: string
        :param bucket_name: name of the bucket

        :type project: string
        :param project: the project which the client acts on.

        :type credentials: OAuth2 credentials
        :param credentials: (optional)
                            Client init will fail
                            if not passed and no `http` object provided

        :type http: :class:`httplib2.Http`
                    or callable that returns :class:`httplib2.Http`
        :param http: (optional)
                     Client init will fail
                     if not passed and no `credentials` provided
        """
        bucket = bucket or settings.GOOGLE_CLOUD_STORAGE.get('bucket')
        project = project or settings.GOOGLE_CLOUD_STORAGE.get('project', '')
        credentials = credentials or settings.GOOGLE_CLOUD_STORAGE.get(
            'credentials')
        http = http or settings.GOOGLE_CLOUD_STORAGE.get('http')
        if callable(http):
            http = http()
        client = storage.Client(project=project, credentials=credentials,
                                http=http)
        self.bucket = client.get_bucket(bucket)

    def _open(self, name):
        """
        Writes blob contents into in-memory file and returns `StringIO` instance
        """
        output = StringIO.StringIO()
        self.bucket.get_blob(name).download_to_file(output)
        return output

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        if hasattr(content, 'content_type'):
            content_type = content.content_type
        else:
            content_type = mimetypes.guess_type(name)
        blob.cache_control = settings.GOOGLE_CLOUD_STORAGE.get('cache_control')
        blob.upload_from_file(content, True, content.size, content_type)
        blob.make_public()
        return name

    def delete(self, name):
        try:
            self.bucket.blob(name).delete()
        except exceptions.NotFound:
            return False
        return True

    def exists(self, name):
        return self.bucket.blob(name).exists()

    def listdir(self, path=None):
        return self.bucket.list_blobs()

    def size(self, name):
        return self.bucket.blob(name).size

    def created_time(self, name):
        return self.bucket.get_blob(name)._properties.get('timeCreated')

    def modified_time(self, name):
        return self.bucket.blob(name).updated

    def url(self, name):
        return self.bucket.blob(name).public_url
