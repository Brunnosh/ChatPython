class User:
    def __init__(self, nickname, email, password):
        self.nickname = nickname
        self.email = email
        self.password = password

class Message:
    def __init__(self, nickname_from, nickname_to, content):
        self.nickname_from = nickname_from
        self.nickname_to = nickname_to
        self.content = content

