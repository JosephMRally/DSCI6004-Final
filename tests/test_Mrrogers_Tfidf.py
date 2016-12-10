from __future__ import division
import nose
from nose.tools import assert_equal, assert_not_equal
import Mongo
import os

import srt_parser
import engines.mrrogers_tfidf

class test__Mrrogers_Tfidf(object):

    def setup(self):
        parser = srt_parser.Srt_Parser(di_path='/Users/Mac/GitHub/DSCI6004-Final')
        self.engine = engines.mrrogers_tfidf.Mrrogers_Tfidf(di_corpus=parser)

    def test_analyze_zero(self):
        x = self.engine.analyze("zero")
        print(x)

    def test_analyze_plants(self):
        x = self.engine.analyze("plants")
        print(x)

