import time

from user.utils import encrypt


class Result(object):
    __slots__ = ('_status', '_code', '_message', '_data', '_token', 'created')

    def __init__(self):
        self._status = True
        self._token = encrypt.digest()
        self.created = str(round(time.time() * 1000))

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if not isinstance(status, bool):
            raise ValueError('status必须是bool')
        self._status = status

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def token(self):
        return self._token
