class Vote():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def select_round(self, n_tour):
        return self.dataframe.loc[n_tour]

class OneRoundVote(Vote):
    def vote(self):
        n_candidats = 9
        df = self.select_round(0)
        print(df.uniq())

        df = df - 1
        print(df)
        res_per_candidate = {}
        for i in range(n_candidats):
            print("_" * 100)
            print(i)
            print(df[df == i])
            res_per_candidate[i] = df[df == i].sum()

        print(res_per_candidate)