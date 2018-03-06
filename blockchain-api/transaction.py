from ecdsa import SECP256k1, rfc6979, BadSignatureError, VerifyingKey, SigningKey
from hashlib import sha256
from six import b

from utils import hash

class Transaction(object):

#Creates a new transaction to go into the next mined Block
    def __init__(self, sender, recipient, amount):
        self.sender_addr = hex_to_ecdsa(sender)
        self.recipient_addr = hex_to_ecdsa(recipient)
        self.amount = amount
        self._transaction = b(sender+recipient+str(self.amount))
        self.transaction_id = self.transaction_hash


    #verify the transaction
    def process_transaction(self, signature):
        if not self.verify_signature(signature):
            print("Failed to verify transaction")
            return false
        return True


    #returns the hashed transaction
    @property
    def transaction_hash(self):
        return hash(self._transaction, serialized=True)


    #generate signature to sign/process the transaction
    def generate_signature(self, sender_key):
        private_key = string_to_ecdsa(sender_key, type_private=True)
        signature = None
        while signature is None:
            try:
                signature = private_key.sign(self._transaction)
            except RuntimeError:
                pass
        return signature


    #verify valid signature
    #Needs to verify:
    #1) user has the amount that user wants to send
    #2) haven't already sent it to someone else.
    def verify_signature(self, signature):
        signature = hex_to_string(signature)
        verified = False
        try:
            verified = self.sender_addr.verify(signature, self._transaction)
        except BadSignatureError:
            verified = False
        return verified


def hex_to_string(key):
    return bytes.fromhex(key)


def hex_to_ecdsa(key, curve=SECP256k1, hashfunc=sha256, type_private=False):
    string_key = hex_to_string(key)
    ecdsa_key = None
    try:
        if(type_private):
            ecdsa_key = SigningKey.from_string(string_key, curve=SECP256k1, hashfunc=sha256)
        else:
            ecdsa_key = VerifyingKey.from_string(string_key, curve=SECP256k1, hashfunc=sha256)
    except AssertionError:
        raise
    return ecdsa_key
