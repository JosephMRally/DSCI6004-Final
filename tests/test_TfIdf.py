from __future__ import division
import nose
from nose.tools import assert_equal, assert_not_equal

import IR.tfidf

class test__tfidf(object):
    obj = None # object to test

    def setup(self):
        pass

    def test_command_episode(self):
        document = [ 'a b c d a', 'a b c' ]
        tf = IR.tfidf.TfIdf()
        tf.index(document)
        x = tf.query('a')

