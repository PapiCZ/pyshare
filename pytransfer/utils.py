import os
import random
import string
from collections import deque

import requests


class DataBuilder:
    queue = deque()

    def __init__(self, filename):
        # Build basic structure of HTTP body
        self.boundary = ''.join(random.choice(string.digits + string.ascii_letters) for i in range(30))
        start = bytes('--' + self.boundary + '\r\n', 'utf-8')
        start += bytes('Content-Disposition: form-data; filename="' + filename + '"' + '\r\n', 'utf-8')
        start += bytes('Content-Type: application/octet-stream' + '\r\n', 'utf-8')
        start += bytes('\r\n', 'utf-8')
        end = bytes('\r\n--' + self.boundary + '--\r\n', 'utf-8')

        self.queue.append(start)
        self.filename = filename
        self.queue.append(open(filename, 'rb'))
        self.queue.append(end)

    def __iter__(self):
        return self

    def __next__(self):
        output = b''
        remaining_size = 1024 * 1024

        if len(self.queue) == 0:
            raise StopIteration

        while remaining_size != 0:
            try:
                fragment = self.queue[0]
                if isinstance(fragment, bytes):
                    chunk = fragment[:remaining_size]
                    output += chunk
                    self.queue[0] = fragment[remaining_size:]

                    remaining_size -= len(chunk)

                    if len(self.queue[0]) == 0:
                        self.queue.popleft()

                    print(output)
                else:
                    data = fragment.read(remaining_size)
                    print(str(fragment.tell()) + '/' + str(os.stat(self.filename).st_size))

                    if len(data) < remaining_size:
                        self.queue.popleft()

                    remaining_size -= len(data)
                    output += data
            except Exception:
                return output
        return output


def upload_file(filename, url='http://127.0.0.1:8080'):
    databuilder = DataBuilder(filename)

    r = requests.post(url, data=databuilder, headers={
        'Content-Type': 'multipart/form-data; boundary=' + databuilder.boundary
    }, stream=True)

    return r.content
