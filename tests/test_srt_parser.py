from __future__ import division
import nose
from nose.tools import assert_equal, assert_not_equal

import srt_parser


class test_srt_parser(object):
    parser = None

    def setup(self):
        print("setup")
        self.parser = srt_parser.Srt_Parser(di_path='/Users/Mac/GitHub/DSCI6004-Final')

    def test_parser(self):
        print("test_class_freq")
        assert len(self.parser.episodes)==2
        assert len(self.parser.episodes[0].words_unaltered)>1000
        assert self.parser.episodes[0].words_unaltered.startswith("Oh Oh it's a beautiful day in the neighborhood")
        assert self.parser.episodes[0].words[0:5] == ['Oh', 'Oh', 'it', "'s",'a']
        assert self.parser.episodes[0].line_number[0:5] == [1, 2, 3, 4, 5]
