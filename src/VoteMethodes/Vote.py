class Vote():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def vote(self):
        """

        :return: {"winner": numWinner, "elimination" : [FirstEliminatedCandidates, second..]}
        """
        winner = 1
        log = {"tour_1": {"votes": {}}}
        return {"winner": winner,
                "log": log}
