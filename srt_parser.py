import os
import logging
import collections
import time
import datetime
from textblob import TextBlob
import IR.PorterStemmer

class Srt_Parser:
    # instance variables
    """
    episodes.name
    episodes.words_unaltered
    episodes.words
    episodes.line_number
    episodes.timing
    episodes.youtubeurl
    """
    episodes = None
    _path = os.getcwd()
    _p = IR.PorterStemmer.PorterStemmer()

    # constructor
    def __init__(self, di_path=None):
        """
        :param di_path: dependency-injection method to override path, for testing only
        """
        self.episodes = []
        if (di_path!=None): self._path = di_path
        self._load_episodes()

    # instance methods
    def _load_episodes(self):
        path_and_directory = self._path + "/episodes"
        for filename in os.listdir(path_and_directory):
            logging.info("loading episode " + filename)
            textfile = open(path_and_directory + "/" + filename, 'r')
            text = str(textfile.read())

            #create our data structure to hold stuff
            #extract the name and you tube url
            entry = Expando() # dynamic object - cuz i love prototype languages
            x = filename.replace(".srt","").split("|")
            entry.name = x[0]
            entry.youtubeurl = x[1]
            self._transform_srt_to_tokens(entry, text)
            self.episodes.append(entry)

    def _transform_srt_to_tokens(self, entry, srt_text_file, ):
        # goal is to have a format that is compatible with NLTK / spaCy / TextBlob
        # and still contain the timing info

        # init 'entry'
        entry.words_unaltered = "" # TODO: make this into a first class data structure

        entry.words = []
        entry.words_stemmed = [] # same size as .words
        #entry.words_lemonized = [] # same size as .words
        entry.line_number = [] # same size as .words
        entry.timing = [] # (s_timing, t_timing)

        lines = srt_text_file.split("\n")
        for line_number, timing_info, text, line4 in zip(*[iter(lines)]*4):
            logging.info("processing text: " + text)
            s_start_time, s_end_time = [_.strip().replace(",",".") for _ in timing_info.split("-->")]
            dt_start_time = datetime.datetime.strptime(s_start_time, "%H:%M:%S.%f")
            dt_end_time = datetime.datetime.strptime(s_end_time, "%H:%M:%S.%f")
            segment_start_end = (dt_start_time, dt_end_time)

            # all to full text
            entry.words_unaltered += " " + text

            blob = TextBlob(text) #TODO: why is it splitting on "'s"
            words = blob.words

            if len(words)>0: # sometimes no words
                # special entry for the first word. record timing info
                entry.words.append(words[0])
                # entry.timing.append((len(entry.words)-1, s_start_time, t_start_time))
                entry.timing.append(segment_start_end)
                entry.line_number.append(int(line_number))
                entry.words_stemmed.append(self._p.stem(words[0]))

            if len(words)>2: # more than one word
                # do the middle words
                entry.words.extend(words[1:-1])
                entry.timing.extend([segment_start_end]*len(words[1:-1]))
                entry.words_stemmed.extend([self._p.stem(_) for _ in words[1:-1]])

            if len(words)>1: # someones only one word
                # special entry for the last word. record timing info
                entry.words.append(words[-1])
                # entry.timing.append((len(entry.words) - 1, s_end_time, t_end_time))
                entry.timing.append(segment_start_end)
                entry.words_stemmed.append(self._p.stem(words[-1]))

        # polish
        entry.words_unaltered = entry.words_unaltered.strip()

class Expando(object):
    pass
