import os
import logging
import collections
import time
import datetime
from textblob import TextBlob


class Corpus: #TODO: rename to srt_parser
    def __init__(self):
        self.episodes = []

    def load_episodes(self):
        path = os.getcwd() + "/episodes"
        for filename in os.listdir(path):
            logging.info("loading episode " + filename)
            textfile = open(path + "/" + filename, 'r')
            text = str(textfile.read())
            entry = Expando()
            entry.name = filename
            result = self.transform_srt_to_tokens(entry, text)
            self.episodes.append(entry)

    def transform_srt_to_tokens(self, entry, srt_text_file, ):
        # goal is to have a format that is compatible with NLTK / spaCy / TextBlob
        # and still contain the timing info


        #init 'entry'
        entry.words_unaltered = "" #TODO: make this into a first class data structure

        entry.words = []
        entry.words_stemmed = [] #same size as .words
        entry.words_lemonized = [] #same size as .words

        entry.timing = [] #(index at .words, s_timing, t_timing)


        lines = srt_text_file.split("\n")
        for line_number, timing_info, text, line4 in zip(*[iter(lines)]*4):
            logging.info("processing text: " + text)
            s_start_time, s_end_time = [_.strip().replace(",",".") for _ in timing_info.split("-->")]
            dt_start_time = datetime.datetime.strptime(s_start_time, "%H:%M:%S.%f")
            dt_end_time = datetime.datetime.strptime(s_end_time, "%H:%M:%S.%f")
            t_start_time = dt_start_time.time()
            t_end_time = dt_end_time.time()

            #all to full text
            entry.words_unaltered += " " + text

            blob = TextBlob(text) #TODO: why is it splitting on "'s"
            words = blob.words

            if len(words)>0: #sometimes no words
                #special entry for the first word. record timing info
                entry.words.append(words[0])
                entry.timing.append((len(entry.words)-1, s_start_time, t_start_time))

            if len(words)>2: #more than one word
                #do the middle words
                entry.words.extend(words[1:-1])

            if len(words)>1: #someones only one word
                #special entry for the last word. record timing info
                entry.words.append(words[-1])
                entry.timing.append((len(entry.words) - 1, s_end_time, t_end_time))
        #polish
        entry.words_unaltered = entry.words_unaltered.strip()

class Expando(object):
    pass

