import hashlib
import json

#Creates a SHA-256 hash of provided data
def hash(data, serialized=False):
    if not serialized:
        data = serialize(data)
    return hashlib.sha256(data).hexdigest()


def serialize(data):
    if isinstance(data, dict):
        return json.dumps(data, sort_keys=True).encode()
    return json.dumps(data.__dict__, sort_keys=True).encode()

def deserialize(data):
    return json.loads(data).decode()
