import hashlib
import json
from time import time
from urllib.parse import urlparse

from block import Block
from mine import valid_proof
import utils

class Blockchain(object):

    #Chain consisting of blocks
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()
        self.nodes = set()
        self.height = len(self.chain)


    #returns the last block in the blockchain
    @property
    def last_block(self):
        return self.chain[-1]


    #creates the genesis(first block) block in the blockchain
    def generate_genesis_block(self):
        genesis_block = Block(1,0)
        serialized_block = genesis_block.__dict__
        self.chain.append(serialized_block)


    #Add a new node to the list of nodes on the network
    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')



    #Check if a given blockchain is valid
    def valid_chain(self, chain):
        last_block = chain[0] #initial block
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block.block_header['previous_hash'] != utils.hash(last_block.block_header):
                return False

            # Check that the Proof of Work is correct
            if not valid_proof(block.block_header['nonce'], block.block_header['previous_hash'], block.block_header['difficulty']):
                return False

            last_block = block
            current_index += 1

        return True


    #Replace the chain with the longest valid chain on network
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
