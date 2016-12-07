from __future__ import division
import nose
from nose.tools import assert_equal, assert_not_equal

import srt_parser


class test__srt_parser(object):

    def setup(self):
        print("setup")
        parser = srt_parser.Srt_Parser(di_path='/Users/Mac/GitHub/DSCI6004-Final')

    def test_classfreq(self):
        print("test_class_freq")
        assert len(parser.episodes)==2
        assert_equal(1, 2)

def test():
    assert False
