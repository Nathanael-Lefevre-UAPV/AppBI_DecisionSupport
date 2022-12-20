from VoteMethodes.Vote import Vote

import numpy as np


class Borda(Vote):
    def __init__(self, dataframe):
        super(Borda, self).__init__(dataframe - 1)
        self.nb_candidates = len(self.dataframe)
        self.candidates_score = [0 for c in range(self.nb_candidates)]

    def vote(self):
        for i in range(self.nb_candidates):  # construct table of candidates' score
            bonus = self.nb_candidates - i
            for candidate in self.dataframe.loc[i]:
                self.candidates_score[candidate] += bonus

        candidates_score = {key+1: self.candidates_score[key] for key in range(len(self.candidates_score))}
        return {"winner": {"candidate": np.argmax(self.candidates_score) + 1},  # real number of the winner (index winner+1 in list)
                "log": {"candidates_score": candidates_score}}  # score list
