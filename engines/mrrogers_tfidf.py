import re
import random

import srt_parser
import IR.tfidf

class mrrogers_tfidf:
    _corpus = None
    _tfidf = None

    def __init__(self, di_corpus=None):
        if di_corpus is None:
            self._corpus = srt_parser.Srt_Parser()
        else:
            self._corpus = di_corpus

        self._tfidf = IR.tfidf.TFIDF()
        self._tfidf.read_data(self.parser.episodes)
        self._tfidf.index()
        self._tfidf.compute_tfidf()

    # main routine to process requests
    def analyze(self, statement):
        print("METHOD: Analyze")
        print("statement", statement)
        statement = statement.lower()

        # hard coded commands
        # TODO: encapsulate commands in rule based engine?
        if "episodes" in statement:
            return self._command_episode()
        if statement.startswith("transcript of"):
            return self._command_transcript_of_episode(statement)
        if "help" in statement:
            return self._command_help()

        #Match user's input to responses in psychobabble. Then reflect candidate response."
        responses = self._tfidf.query_rank(statement)

        #if we have a query use if
        if len(responses)>0:
            response_message = "hit but not implemented"
        #else show a puppet show with an apology
        else:
            response_message = "Sorry I don't have an answer for you. Try 'popular questions'. In the mean time, enjoy this puppet show"

        # return the response
        response = random.choice(response_message)
        print("analyze complete")
        return response

    # helper method
    def _command_episode(self):
        response = "episode id : episode name\n"
        for n, episode in enumerate(self._corpus.episodes):
            response += "{0} : {1}\n".format(n, episode.name)
        response += "Hint: 'transcript of episode (XX)'."
        return response

    # helper method
    def _command_transcript_of_episode(self, statement):
        response = None
        try:
            print(statement)
            match_group = re.search(r"(\d+)", statement, re.IGNORECASE)
            print(match_group)
            capture_group = match_group.groups(0)[0] if len(match_group.groups()) > 0 else ""
            episode_id = int(capture_group)
            episode = self._corpus.episodes[episode_id]
            response = "{0}\n{1}".format(episode.name, episode.words_unaltered)
        except Exception as err:
            print(err)
            response = "I am sorry neighbor, I didn't understand which episode id you wanted"
        finally:
            pass
        return response

    # helper method
    def _reflect(self, fragment):
        fragment = fragment.lower()
        tokens = fragment.split(" ")
        tokens = list(map(lambda x: self.reflections[x] if x in self.reflections else x, tokens))
        return ' '.join(tokens)

    def _command_help(self):
        s = "Try words 'episodes', 'transcript of episode (XX)'," \
            "'popular questions', 'history', 'credits'. "
        return s


