from __future__ import division
import os

class test_echoserver(object):
    obj = None # object to test

    def setup(self):
        os.environ["MONGODB_URI"] = "XXXX"
        import echoserver
        self.obj = echoserver

    def test_send_message(self):
        token = "xxxxxx"
        recipient = obj.PAT
        text = "http://cnn.com"
        response = self.obj.send_message()

