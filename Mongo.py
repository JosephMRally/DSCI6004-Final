from pymongo import MongoClient
import os

class DB:

    s = os.environ['MONGODB_URI']
    _client = MongoClient(s)
    _db = _client['heroku_7bgx0zzv']
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

