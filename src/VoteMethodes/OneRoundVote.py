from VoteMethodes.Vote import Vote


class OneRoundVote(Vote):
    def vote(self):
        n_candidats = 9
        df = self.select_round(0)

        df = df - 1
        print(df)
        res_per_candidate = []
        for i in range(n_candidats):
            print("_" * 100)
            print(i)
            print(df[df == i])
            res_per_candidate.append(df[df == i].count())
            print(sum(res_per_candidate))

        print(res_per_candidate)
        winner = res_per_candidate.index(max(res_per_candidate)) + 1

        return {"winner": res_per_candidate.index(max(res_per_candidate)) + 1,
                "elimination" : [[i+1 for i in range(n_candidats) if i != winner-1]]}