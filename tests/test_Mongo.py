from __future__ import division
import nose
from nose.tools import assert_equal, assert_not_equal
import Mongo
import os

class test__Mongo(object):

    def setup(self):
        self.db = Mongo.DB()

    def test_command_episode(self):
        self.db.record_outgoing_message({"test":["a"]})
        self.db.record_incoming_message({"test":["a"]})
        pass


