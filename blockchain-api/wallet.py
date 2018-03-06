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
        private_key = SigningKey.generate(curve=SECP256k1, hashfunc=sha256)
        public_key = self._private_key.get_verifying_key()
        self._private_key = private_key.to_string()
        self._public_key = public_key.to_string()


    #TODO
    #def get_balance(self):


    def send_crypto(self, receipient_addr, signature, amount):
        new_transaction = transaction.Transaction(self._public_key, receipient_addr, amount)
        #serialized_transaction = utils.serialize(new_transaction)
        signature = new_transaction.generate_signature(self._private_key)
