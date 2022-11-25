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

        return {"winner": np.argmax(self.candidates_score) + 1,  # real number of the winner (index winner+1 in list)
                "log": self.candidates_score}  # score list
