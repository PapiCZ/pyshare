import mimetypes
import random
import string

from .uploader import FileStreamUploader
import requests


class TransferSh(FileStreamUploader):
    boundary: str

    def __init__(self, *args, **kwargs):
        self.url = 'https://transfer.sh'

        super(TransferSh, self).__init__(*args, **kwargs)

    def queue_http_start(self):
        self.boundary = ''.join(random.choice(string.digits + string.ascii_letters) for i in range(30))
        start = bytes('--' + self.boundary + '\r\n', 'utf-8')
        start += bytes('Content-Disposition: form-data; name="file"; filename="' + self.filename + '"' + '\r\n', 'utf-8')
        start += bytes('Content-Type: ' + str(mimetypes.guess_type(self.filename)) + '\r\n', 'utf-8')
        start += bytes('\r\n', 'utf-8')
        self.queue.append(start)

    def queue_file(self):
        self.queue.append(open(self.filename, 'rb'))

    def queue_http_end(self):
        self.queue.append(bytes('\r\n--' + self.boundary + '--\r\n', 'utf-8'))

    def upload_file(self):
        r = requests.post(self.url, data=self, headers={
            'Content-Type': 'multipart/form-data; boundary=' + self.boundary
        })

        return r.text
