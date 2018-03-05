from urllib.parse import urlparse
from flask import Flask, jsonify, request
import json

import block
import blockchain
import mine
from transaction import Transaction

app = Flask(__name__)

blockchain = blockchain.Blockchain()

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain
    }
    return jsonify(response), 200


@app.route('/mine/<block>', methods=['GET'])
def mine(block):
    previous_block = blockchain.last_block
    difficulty = 2
    mined_block = miner.mine(block,previous_block,difficulty)

    #add the newly mined block to the chain
    blockchain.chain.append(block)
    print("Hooray, a new block is mined!")

    response = json.dumps(mined_block.__dict__)
    return jsonify(response), 200


@app.route('/transaction', methods=['GET','POST'])
def transaction():
    txn_amount = request.form.get('receiver_address')
    txn_receiver = request.form.get('amount')
    txn_sender = request.form.get('sender_address')
    txn = Transaction(txn_amount, txn_receiver, txn_sender)
    txn_id = txn.transaction_id
    response = {
        "Transaction Amount": txn_amount,
        "Transaction ID": txn_id,
        "Transaction Receiver": txn_receiver,
        "Transaction Sender": txn_sender,
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
    app.run(debug=True, host='0.0.0.0', port=8080)
