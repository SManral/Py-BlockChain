from urllib.parse import urlparse
from six import b
from time import time

import utils

class Block(object):


    #Chain consisting of blocks
    def __init__(self, previous_hash, height):
        self.block_header = {
            'difficulty': 4,
            'gas_limit': 10,
            'gas_used': 0,
            'height': height,
            'hash': '',
            'nonce': '',
            'merkle_root': '',
            'previous_hash': previous_hash,
            'timestamp': time()
        }
        self.block_body = {
            'transactions': []
        }


    #hash of current block
    def hash(self):
        return utils.hash(self.block_header)


    #Add new transaction to the block
    def add_tansaction(self, transaction):
        gas_limit = self.block_header['gas_limit']
        gas_used = len(self.block_body['transactions'])
        if transaction is None or gas_used == gas_limit:
            return False
        self.block_body['transactions'].append(transaction)
        return True
