import pandas as pd
from Data import *
from VoteMethodes.OneRoundVote import OneRoundVote

if __name__ == "__main__":
    profile_1 = pd.read_csv(f"{dataPaths[CHOIX_SOCIAL]}/profil1.csv", header=None)
    print(profile_1.transpose())

    v1t = OneRoundVote(profile_1)
    v1t.vote()