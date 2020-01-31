CODE_SYS_CONNECTION_ERROR = 'SYS.0001'

CODE_WRONG_AUTHENTICATION_INFO = 'USER.0001'

ERROR_CODES = {
    'SYS.0001': {
        'CN': '请求错误',
        'EN': 'connection error',
    },
    'USER.0001': {
        'CN': '错误的账号或密码',
        'EN': 'wrong name or password',
    }

}


def get_error_message(code, language):
    return ERROR_CODES[code][language]
