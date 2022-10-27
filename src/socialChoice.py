import pandas as pd
from Data import *
from VoteMethodes.RoundVote import OneRoundVote, TwoRoundVote, AlternativeRoundVote
from pprint import pprint
from VoteMethodes.Borda import Borda
from VoteMethodes.Condorcet import Condorcet
from Utils.ColorPrinter import *

def printSep():
    print()
    greenprint("----------------------")
    print()

if __name__ == "__main__":
    profile_1 = pd.read_csv(f"{dataPaths[CHOIX_SOCIAL]}/profil3.csv", header=None)
    blueprint("Dataframe")
    print(profile_1)

    for voteMethod in [OneRoundVote, TwoRoundVote, AlternativeRoundVote, Borda, Condorcet]:
        printSep()
        blueprint(voteMethod.__name__)
        voter = voteMethod(profile_1)
        pprint(voter.vote())
