from __future__ import division
import nose
from nose.tools import assert_equal, assert_not_equal

import IR.tfidf
import srt_parser


class test_tfidf(object):

    def setup(self):
        print("setup")
        self.parser = srt_parser.Srt_Parser(di_path='/Users/Mac/GitHub/DSCI6004-Final')
        self.tf = IR.tfidf.TFIDF()
        self.tf.read_data(self.parser.episodes)
        self.tf.index()
        self.tf.compute_tfidf()

    def test_command_episode(self):
        ranked = self.tf.query_rank("plant")
        print("plant :", ranked)

        ranked = self.tf.query_rank("almost")
        print("almost:", ranked)

        ranked = self.tf.query_rank("adult")
        print("adult:", ranked)

        ranked = self.tf.query_rank("almost adult")
        print("almost adult", ranked)

        ranked = self.tf.query_rank("zero")
        print(ranked)
        assert len(ranked) == 0

        ranked = self.tf.query_rank("table")
        print(ranked)
        assert len(ranked) == 1

