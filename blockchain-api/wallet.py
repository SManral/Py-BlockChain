from ecdsa import SigningKey, SECP256k1
from hashlib import sha1, sha256, sha512
from six import b

from api import utils
from api import transaction

class Wallet(object):

    def __init__(self):
        self._private_key = None
        self._public_key = None
        self.generate_keys()

    #generate public and private key for the owner of this wallet
    def generate_keys(self):
        secexp = int("9d0219792467d7d37b4d43298a7d0c05", 16)
        self._private_key = SigningKey.from_secret_exponent(secexp, SECP256k1, sha256)
        self._public_key = self._private_key.get_verifying_key()


    #TODO
    #def get_balance(self):


    def send_crypto(self, receipient_addr, amount):
        new_transaction = transaction.Transaction(self._public_key, receipient_addr, amount)
        serialized_transaction = utils.serialize(new_transaction)
        signature = new_transaction.generate_signature(self._private_key)
