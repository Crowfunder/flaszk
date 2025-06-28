import pyotp

class PinManager:
    '''
    Service offering server-side otp pins with token regenerated with each restart
    '''
    def __init__(self):
        self.secret = pyotp.random_base32()
        self.totp = pyotp.TOTP(self.secret)
        self.used_pin = ''

    def get_pin(self):
        return self.totp.now()

    def check_pin(self, pin):
        ok = pin == self.totp.now() and pin != self.used_pin
        if ok:
            self.used_pin = pin
        return ok
    

pin = PinManager()