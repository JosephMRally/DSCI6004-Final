from __future__ import division
import nose
#from nose.tools import assert_equal, assert_not_equal
from nose.tools import *
import Mongo
import os

import srt_parser
import engines.mrrogers_tfidf


class test_Mrrogers_Tfidf(object):

    def setup(self):
        parser = srt_parser.Srt_Parser(di_path='/Users/Mac/GitHub/DSCI6004-Final')
        self.engine = engines.mrrogers_tfidf.Mrrogers_Tfidf(di_corpus=parser)

    def test_analyze_zero(self):
        x = self.engine.analyze("zero")
        assert (x.startswith(r"Sorry I don't have an answer for you.")), x

    def test_analyze_plants(self):
        x = self.engine.analyze("plants")
        assert (x.startswith(r"https://youtube.com/embed/")), x


    def test_analyze_table(self):
        x = self.engine.analyze("table")
        assert (x.startswith(r"https://youtube.com/embed/VyLgiPItJj0")), x


    def test_analyze_tabl(self):
        x = self.engine.analyze("tabl")
        assert (x.startswith(r"Sorry I don't have an answer for you.")), x


    def test_analyze_kitten(self):
        x = self.engine.analyze("kitten")
        assert (x.startswith(r"Sorry I don't have an answer for you.")), x


    def test_popular_words(self):
        x = self.engine.analyze("popular words")
        print(x)
        assert x != ""
        assert x.startswith('cereal shoe orange'), x
        assert x.endswith('tape lambs random'), x # TODO: why is this not a constant answer, it should be deterministic
        assert x == "cereal shoe orange serial snow juice globe ingredients purple practice sifter mixture string quartet jimmy puppets panda tape bins pipes lambs hopper 0 dough random"
