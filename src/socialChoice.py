import pandas as pd
from Data import *
from VoteMethodes.RoundVote import OneRoundVote, TwoRoundVote, AlternativeRoundVote
from pprint import pprint
from VoteMethodes.Borda import Borda
from VoteMethodes.Condorcet import Condorcet
from Utils.ColorPrinter import *


def print_sep(color_printer):
    print()
    color_printer("-" * 150)
    print()


if __name__ == "__main__":
    for numProfil in range(1, 4):
        print_sep(blueprint)
        print(f"profil{numProfil}.csv")
        print_sep(blueprint)
        profil = pd.read_csv(f"{dataPaths[CHOIX_SOCIAL]}/profil{numProfil}.csv", header=None)
        blueprint("Dataframe ")
        print(profil)

        for voteMethod in [OneRoundVote, TwoRoundVote, AlternativeRoundVote, Borda, Condorcet]:
            print_sep(greenprint)
            blueprint(voteMethod.__name__)
            voter = voteMethod(profil)
            pprint(voter.vote())

        print()
