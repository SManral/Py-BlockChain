import utils

class Miner():

    def __init__(self, block):
        self.block = block

    # Mine the given block
    def mine(self):
        block = self.block
        block.block_header['merkle_root'] = generate_merkle_root(block.block_body['transactions']) #probably needs to go elsewhere :/
        block.block_header['nonce'] = proof_of_work(block, block.block_header['difficulty'])
        block.block_header['hash'] = block.hash()
        return block


# Proof of Work Algorithm(Mathematical problem that the miner will solve)
# - Find a number p' such that hash(pp') contains x number of leading zeroes,
#where p is the previous proof, p' is the new proof and x is level of difficulty
def proof_of_work(block, difficulty):
    previous_hash = block.block_header['previous_hash']
    nonce = 0
    while valid_proof(nonce, previous_hash, difficulty) is False:
        nonce += 1
    return nonce


#Validates the Proof: Checks if computed hash(last_proof, proof)ends with 4 zeroes?
def valid_proof(nonce, previous_hash, difficulty):
    data = f'{nonce}{previous_hash}'.encode()
    guess_hash = utils.hash(data, serialized=True)
    return guess_hash[-difficulty:] == "0"*difficulty


#Merkle root, used to verify a set of transactions included in the block
def generate_merkle_root(transactions):
    txn_size = len(transactions)

    #if there is only 1 transaction then merkle root is the transaction id itself
    if txn_size == 1:
        return transactions[0]['transaction_id']

    top_tree_layer = []
    tree_layer = []

    #if there are odd number of transactions in transactions list then double up the last one
    if txn_size%2 != 0:
        transactions.append(transactions[-1])

    for transaction in transactions:
        top_tree_layer.append(transaction['transaction_id'])

    while txn_size != 1:
        tree_layer[:] = []
        for i in range(0,txn_size,2):
            txn_duo = f'{top_tree_layer[i]}{top_tree_layer[i+1]}'.encode()
            tree_layer.append(utils.hash(txn_duo,serialized=True))
        txn_size = len(tree_layer)
        top_tree_layer[:] = tree_layer

    return tree_layer[0]
