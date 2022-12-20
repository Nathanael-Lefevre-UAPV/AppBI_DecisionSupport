import pandas as pd
from Data import *
from VoteMethodes.RoundVote import OneRoundVote, TwoRoundVote, AlternativeRoundVote
from pprint import pprint
from VoteMethodes.Borda import Borda
from VoteMethodes.Condorcet import Condorcet
from Utils.ColorPrinter import *

from DataAnalytics.DataAnalyser import DataAnalyser


def print_sep(color_printer):
    print()
    color_printer("-" * 150)
    print()


if __name__ == "__main__":
    winners = {}
    for numProfil in range(1, 4):
        print_sep(blueprint)
        print(f"profil{numProfil}.csv")
        print_sep(blueprint)
        profil = pd.read_csv(f"{dataPaths[CHOIX_SOCIAL]}/profil{numProfil}.csv", header=None)
        blueprint("Dataframe ")
        print(profil)
        blueprint("Data Analysis")
        dataAnalyser = DataAnalyser(profil, profil_name=f"profil{numProfil}")
        dataAnalyser.plot_candidates_vote_ranking()
        dataAnalyser.plot_candidates_ranking_mean()

        winners[numProfil] = dict()
        for voteMethod in [OneRoundVote, TwoRoundVote, AlternativeRoundVote, Borda, Condorcet]:
            print_sep(greenprint)
            blueprint(voteMethod.__name__)
            voter = voteMethod(profil)
            vote = voter.vote()
            pprint(vote)
            winners[numProfil][voteMethod.__name__] = vote['winner']
            print()

    print_sep(blueprint)
    print(f"Winners")
    print_sep(blueprint)

    pprint(winners)

    print_sep(greenprint)

    # Afficher tableau des winners
    for numProfile, infos in winners.items():
        print()
        print("Profile", numProfile)
        for method, winner in winners[numProfile].items():
            if type(winner) is dict:
                winner = winner['candidate']
            print(method.ljust(20), winner)

    # Analyse de robustesse

    redprint("Appuyez sur entrer pour procéder à l'analyse de Robustesse")
    redprint("Attention: procédure rapide pour le profil 1 (10 min)")
    redprint("Mais lente (> 70min) pour les autres profils")
    input("Entrer pour continuer")
    for numProfil in range(1, 4):
        profil = pd.read_csv(f"{dataPaths[CHOIX_SOCIAL]}/profil{numProfil}.csv", header=None)
        dataAnalyser = DataAnalyser(profil, profil_name=f"profil{numProfil}")
        dataAnalyser.boostrap_analysis()


