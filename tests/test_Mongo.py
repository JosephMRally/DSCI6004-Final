from __future__ import division
import nose
from nose.tools import assert_equal, assert_not_equal
import Mongo
import os

class test_Mongo(object):

    def setup(self):
        self.db = Mongo.DB()

    def test_command_episode(self):
        self.db.record_outgoing_message({'message': {'text': 'bbb'}, 'recipient': {'id': 'aaa'}})
        self.db.record_incoming_message({"test":["a"]})
        pass


