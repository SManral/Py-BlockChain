from ecdsa import SigningKey, SECP256k1, rfc6979, BadSignatureError
from hashlib import sha256
from six import b

from utils import hash

class Transaction(object):

#Creates a new transaction to go into the next mined Block
    def __init__(self, sender, recipient, amount):
        self.sender_addr = sender
        self.recipient_addr = recipient
        self.amount = amount
        self._transaction = b(
                self.sender_addr.to_string().hex()+
                self.recipient_addr.to_string().hex()+
                str(self.amount)
                )
        self.transaction_id = self.transaction_hash


    #verify the transaction
    def process_transaction(self):
        if not self.verify_signature():
            print("Failed to verify transaction")
            return false
        return True


    #returns the hashed transaction
    @property
    def transaction_hash(self):
        return hash(self._transaction, serialize=False)


    #generate signature to sign/process the transaction
    def generate_signature(self, private_key):
        signature = None
        secexp = int("9d0219792467d7d37b4d43298a7d0c05", 16)
        k = rfc6979.generate_k(SECP256k1.generator.order(), secexp, sha256, sha256(self._transaction).digest())
        while signature is None:
            try:
                signature = private_key.sign(self._transaction, k=k)
            except RuntimeError:
                pass
        return signature


    #verify valid signature
    def verify_signature(self, signature):
        verified = False
        try:
            verified = self.sender_addr.verify(signature, self._transaction)
        except BadSignatureError:
            verified = False
        return verified
