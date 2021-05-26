import hashlib


class FileHash:

    def __init__(self, BUF_SIZE=65536):

        # BUF_SIZE is totally arbitrary, change for your app!
        # BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
        self.BUF_SIZE = BUF_SIZE

    def _reader(self, filename, hash_object):

        with open(filename, 'rb') as f:
            while True:
                data = f.read(self.BUF_SIZE)
                if not data:
                    break
                hash_object.update(data)

        return hash_object.hexdigest()

    def md5(self, filename):
        return self._reader(filename, hashlib.md5())

    def sha1(self, filename):
        return self._reader(filename, hashlib.sha1())

    def sha256(self, filename):
        return self._reader(filename, hashlib.sha256())
