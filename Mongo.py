from pymongo import MongoClient
import os

class DB:

    _client = MongoClient(os.environ['MONGODB_URI'])
    _db = _client['mrrogers']
    _incoming = _db['incoming']
    _outgoing = _db['outgoing']

    def does_user_exist(self):
        return True

    def record_incoming_message(self, payload):
        self._incoming.insert_one(payload)
        return True

    def record_outgoing_message(self, payload):
        self._outgoing.insert_one(payload)
        return True

