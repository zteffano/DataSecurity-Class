class Rockyou(object):
    _instance = None
    _bad_passwords = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Rockyou, cls).__new__(cls)
            with open("./rockyou.txt", "r", errors="replace") as f:
                cls._bad_passwords = [line.rstrip() for line in f]
        return cls._instance

    def check_password(self, password):
        return password in self._bad_passwords
