from VoteMethodes.Vote import Vote

import numpy as np


class Condorcet(Vote):
    def __init__(self, dataframe):
        dataframe = dataframe - 1
        super(Condorcet, self).__init__(dataframe.transpose())
        self.nb_candidates = len(dataframe)
        self.nb_elector = len(self.dataframe)
        self.res_battles = [[1 for i in range(self.nb_candidates)] for j in range(self.nb_candidates)]

    def vote(self):
        for i in range(self.nb_candidates):
            for j in range(i + 1, self.nb_candidates):  # consider only the half of matrix
                cnt_win_i = 0
                cnt_win_j = 0
                for elector in range(self.nb_elector):  # for each vote, compare two candidates
                    vote = self.dataframe.loc[elector].values.tolist()
                    if vote.index(i) < vote.index(j):
                        cnt_win_i += 1
                    else:
                        cnt_win_j += 1

                if cnt_win_i < cnt_win_j:  # if i loses against j
                    self.res_battles[i][j] = 0
                else:
                    self.res_battles[j][i] = 0

        res_battles_summed = [sum(line) for line in self.res_battles]
        winner = None
        best = np.argmax(res_battles_summed)
        if res_battles_summed[best] == self.nb_candidates:  # there is a winner only if he wins all battles
            winner = best + 1  # real number of the winner (because list starts with index 0)

        res_battles_summed = {key+1: res_battles_summed[key] for key in range(len(res_battles_summed))}
        return {"winner": {"candidate": winner},  # winner
                "log": {"candidates_score": res_battles_summed,
                        "battles_matrix": self.res_battles}}  # list of number of wins
