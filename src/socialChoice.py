import pandas as pd
from Data import *
from VoteMethodes.OneRoundVote import OneRoundVote
from VoteMethodes.Borda import Borda
from VoteMethodes.Condorcet import Condorcet

if __name__ == "__main__":
    print("Dataframe")
    profile_1 = pd.read_csv(f"{dataPaths[CHOIX_SOCIAL]}/profil3.csv", header=None)
    print(profile_1)
    print()
    print("----------------------")
    print()

    print("OneRoundVote")
    v1t = OneRoundVote(profile_1)
    v1t.vote()

    print()
    print("----------------------")
    print()

    print("Borda")
    vBorda = Borda(profile_1)
    resBorda = vBorda.vote()
    print(resBorda)

    print()
    print("----------------------")
    print()

    print("Condorcet")
    vCondorcet = Condorcet(profile_1)
    resCondorcet = vCondorcet.vote()
    print()
    print(resCondorcet)