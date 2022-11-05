import pandas as pd
from Data import *
from VoteMethodes.RoundVote import OneRoundVote, TwoRoundVote, AlternativeRoundVote
from pprint import pprint
from VoteMethodes.Borda import Borda
from VoteMethodes.Condorcet import Condorcet
from Utils.ColorPrinter import *

def printSep(colorPrinter):
    print()
    colorPrinter("-" * 150)
    print()


if __name__ == "__main__":
    for numProfil in range(1, 4):
        printSep(blueprint)
        print(f"profil{numProfil}.csv")
        printSep(blueprint)
        profil = pd.read_csv(f"{dataPaths[CHOIX_SOCIAL]}/profil{numProfil}.csv", header=None)
        blueprint("Dataframe ")
        print(profil)

        for voteMethod in [OneRoundVote, TwoRoundVote, AlternativeRoundVote, Borda, Condorcet]:
            printSep(greenprint)
            blueprint(voteMethod.__name__)
            voter = voteMethod(profil)
            pprint(voter.vote())

        print()
