
class NotFileError(Exception):
    def __init__(self, message):
        self.message = message

class FormatError(Exception):
    def __init__(self, message = "format warning"):
        print(message)
        self.message = message

class UserExistsError(Exception):
    def __init__(self, message):
        self.message = message