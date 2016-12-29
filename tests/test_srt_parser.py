from __future__ import division
import nose
from nose.tools import assert_equal, assert_not_equal

import srt_parser


class test_srt_parser(object):
    parser = None

    def setup(self):
        print("setup")
        self.parser = srt_parser.Srt_Parser(di_path='/Users/Mac/GitHub/DSCI6004-Final')

    def test_parser_1633(self):
        print("test_class_freq")
        assert len(self.parser.episodes)==8

        episode = [_ for _ in self.parser.episodes if _.name == '1633'][0]
        assert len(episode.words_unaltered) == 14491
        assert episode.words_unaltered.startswith("it's a beautiful day in this neighborhood")
        assert episode.words[0:3] == ['it', "'s", 'a']
        assert episode.line_number[0:5] == [1, 2, 3, 4, 5]

    def test_lower_case_Kitty(self):
        document_of_episode = self.parser.episodes
        episode = [_ for _ in document_of_episode if _.name == '1633'][0]
        word_kitty = [_ for _ in episode.words_stemmed if _ == 'kitti' or _ == 'Kitti'][0]
        assert word_kitty == 'kitti'


