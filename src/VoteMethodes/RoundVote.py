from VoteMethodes.Vote import Vote


class RoundVote(Vote):
    def __init__(self, dataframe):
        super(RoundVote, self).__init__(dataframe)

        self.n_candidates, self.n_elector = dataframe.shape
        self.all_eliminated = set()
        self.n_round = None

        # dictionnaires {candidat : {electeur: [choix ordonné]}}
        self.electors_per_candidate = dict()
        firstVote = self.dataframe.loc[0]  # Premier vote par candidat
        for candidate in range(1, self.n_candidates + 1):
            # df : Liste des electeur ayant voté pour candidate en premier
            df = self.dataframe[firstVote.index[firstVote == candidate]]
            self.electors_per_candidate[candidate] = {elector: df[elector].tolist() for elector in df.keys()}
        self.current_round = 1

    def next_round(self, eliminated):
        self.all_eliminated.update(eliminated)
        for candidate in eliminated:  # Pour tous les candidats éliminés à ce tour
            if candidate in self.electors_per_candidate.keys():
                for elector in self.electors_per_candidate[candidate].keys():
                    elector_choice = self.electors_per_candidate[candidate][elector]
                    # recherche du premier choix non éliminé
                    first_choice = -1
                    for first_choice in elector_choice:
                        if first_choice not in self.all_eliminated:  # Si le candidat n'as jamais été éliminé
                            break
                    assert first_choice != -1, "Tous les choix du candidat ont été éliminés"
                    # Ajout de l'électeur dans la liste des électeurs de son candidat préféré
                    try:
                        self.electors_per_candidate[first_choice][elector] = elector_choice
                    except Exception as e:
                        print(e)
                        print("eliminated", eliminated)
                        print("first_choice", first_choice)
                        print("elector", elector)
                        input()
                # Le candidat est éliminé
                del self.electors_per_candidate[candidate]
        self.current_round += 1

    def vote(self):
        log = dict()

        for round in range(1, self.n_round + 1):
            vote_per_candidate = {i: len(self.electors_per_candidate[i])
                                  for i in self.electors_per_candidate.keys()}
            percent_per_candidate = {i: vote_per_candidate[i] * 100 / self.n_elector
                                     for i in self.electors_per_candidate.keys()}
            candidate_order = [c[0] for c in sorted(vote_per_candidate.items(), key=lambda item: item[1], reverse=True)]
            best_candidates = candidate_order[:self.n_round + 1 - round]
            eliminated = candidate_order[self.n_round + 1 - round:]

            log[round] = {"vote_per_candidate": vote_per_candidate,
                                    "percent_per_candidate": percent_per_candidate,
                                    "candidate_order": candidate_order,
                                    "best_candidates": best_candidates,
                                    "eliminated": eliminated}
            if round != self.n_round:
                self.next_round(eliminated=eliminated)

            #'''
            if percent_per_candidate[best_candidates[0]] > 50.:
                break
            #'''

        winner = {"candidate": best_candidates[0],
                  "vote": vote_per_candidate[best_candidates[0]],
                  "percentage": percent_per_candidate[best_candidates[0]]}
        return {"winner": winner,
                "log": log}


class OneRoundVote(RoundVote):
    def __init__(self, dataframe):
        super(OneRoundVote, self).__init__(dataframe)
        self.n_round = 1


class TwoRoundVote(RoundVote):
    def __init__(self, dataframe):
        super(TwoRoundVote, self).__init__(dataframe)
        self.n_round = 2


class AlternativeRoundVote(RoundVote):
    def __init__(self, dataframe):
        super(AlternativeRoundVote, self).__init__(dataframe)
        self.n_round = dataframe.shape[0] - 1
