import pyotp
from flask import flash
from random import randint
from ..pairingConfig import PIN_COUNTER_THERSHOLD, PIN_COUNTER_LIMIT

class PinManager:
    '''
    Service offering server-side otp pins with token regenerated with each restart
    '''
    def __init__(self):
        self.hotp = pyotp.HOTP('base32secret3232')
        # self.counter = randint(PIN_COUNTER_THERSHOLD,PIN_COUNTER_LIMIT)
        # self.used_pin = ''

    def get_pin(self):
        self.counter= self.new_counter()
        return self.hotp.at(self.counter)

    def check_pin(self, pin):
        if self.hotp.verify(pin, self.counter):
            self.counter=self.new_counter()
            return True
        flash("Wrong PIN given. Start pairing again")
        self.counter=self.new_counter()
        return False
    
    def new_counter(self):
        return randint(PIN_COUNTER_THERSHOLD,PIN_COUNTER_LIMIT)
    

pin = PinManager()