import time

from user.utils import encrypt


class Result(object):
    __slots__ = ('_status', '_code', '_message', '_data', '_token', '_created')

    def __init__(self):
        self._status = True
        self._code = None
        self._message = None
        self._data = None
        self._token = encrypt.digest_random()
        self._created = str(round(time.time() * 1000))

    def serializer(self):
        d = dict()
        for k in self.__slots__:
            v = self.__getattribute__(k)
            if v or k == '_status':
                k = k[1:]
                d[k] = v
        return d

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
        self._status = False
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

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def created(self):
        return self._created
