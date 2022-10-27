class Vote():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def select_round(self, n_tour):
        return self.dataframe.loc[n_tour]

    def vote(self):
        """

        :return: {"winner": numWinner, "elimination" : [FirstEliminatedCandidates, second..]}
        """
        pass
