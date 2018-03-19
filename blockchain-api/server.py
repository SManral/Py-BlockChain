from urllib.parse import urlparse
from flask import Flask, jsonify, request
import json

import block
from blockchain import Blockchain
from mine import Miner
from transaction import Transaction

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain
    }
    return jsonify(response), 200


@app.route('/mine/<block>', methods=['GET'])
def mine(block):
    #previous_block = blockchain.last_block
    miner = Miner(block)
    mined_block = miner.mine(block).__dict__

    #add the newly mined block to the chain
    blockchain.chain.append(mined_block)
    print("Hooray, a new block is mined!")

    response = json.dumps(mined_block)
    return jsonify(response), 200


@app.route('/transaction', methods=['GET','POST'])
def transaction():
    txn_sender = request.form.get('sender')
    txn_recipient = request.form.get('recipient')
    txn_amount = request.form.get('amount')
    txn_signature = request.form.get('signature')

    txn = Transaction(txn_sender, txn_recipient, txn_amount)
    txn_id = txn.transaction_id
    txn_verify = txn.process_transaction(txn_signature)

    response = {
        "Transaction Sender": txn_sender,
        "Transaction Receiver": txn_recipient,
        "Transaction Amount": txn_amount,
        "Transaction Signature": txn_signature,
        "Transaction ID": txn_id,
        "Verified": txn_verify
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'The chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'The chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
