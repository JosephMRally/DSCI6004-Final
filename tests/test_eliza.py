from __future__ import division

import srt_parser
from engines import eliza


class test_eliza(object):
    obj = None # object to test

    def setup(self):
        parser = srt_parser.Srt_Parser(di_path='/Users/Mac/GitHub/DSCI6004-Final')
        self.obj = eliza.Eliza(di_corpus=parser)

    def test_command_episode(self):
        response = self.obj._command_episode()
        print(response)
        assert response is not None
        assert "0 : 1384" in response
        assert "1 : 1463" in response


    def test_command_transcript_of_episode(self):
        response = self.obj._command_transcript_of_episode("transcript of episode 0")
        print(response)
        assert response is not None
        assert "1384" in response
