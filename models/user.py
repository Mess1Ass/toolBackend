class User:
    def __init__(self, username: str, password: str, code: str = ''):
        self.username = username
        self.password = password
        self.code = code

    def to_form_data(self):
        return {
            'username': self.username,
            'password': self.password,
            'code': self.code
        }
