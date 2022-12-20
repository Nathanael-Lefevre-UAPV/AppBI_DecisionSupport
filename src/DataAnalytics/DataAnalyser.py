import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from tqdm import trange

from Utils.pathsDefinition import *
from Utils.ColorPrinter import *

from VoteMethodes.RoundVote import OneRoundVote, TwoRoundVote, AlternativeRoundVote
from VoteMethodes.Borda import Borda
from VoteMethodes.Condorcet import Condorcet

class DataAnalyser:
    def __init__(self, profil, profil_name):
        self.profil = profil
        self.profilName = profil_name

    def plot_candidates_vote_ranking(self):
        nb_place_pos = 3
        width = 0.35
        shift_factor = 5  # facteur pour le décalage des rangs (1er, 2nd, ...) dans l'histogramme
        label_factor = 2
        rank = {}

        for place_pos in range(nb_place_pos):
            rank[place_pos+1] = []
            for candidate_num in range(self.profil.shape[0]):
                rank[place_pos+1].append(sum(self.profil.loc[place_pos] == candidate_num+1))

        labels = np.array([i for i in range(1, self.profil.shape[0]+1)])

        fig, ax = plt.subplots()
        shift = shift_factor * (np.arange(nb_place_pos) - (nb_place_pos-1) * 0.5)
        for place_pos, add in zip(range(1, nb_place_pos+1), shift):
            rects = ax.bar(label_factor*labels + (add * width / nb_place_pos), rank[place_pos], width, label=place_pos)
            ax.bar_label(rects, padding=3, rotation=-90)

        ax.set_ylabel('NB Vote')
        title = "Number of votes by candidate and rank"
        ax.set_title(title)
        ax.set_xticks(label_factor*labels, labels)
        ax.legend()
        plt.margins(.02, .15)

        fig.tight_layout()
        plt.savefig(figPath / f"{self.profilName}-{title.replace(' ', '_')}.png")
        plt.show()

        print(rank)


    def plot_candidates_ranking_mean(self):
        nb_candidates = self.profil.shape[0]
        nb_votes = self.profil.shape[1]
        mean_rank = [0 for _ in range(nb_candidates)]
        for num_candidate in range(nb_candidates):
            for place_pos in range(nb_candidates):
                mean_rank[num_candidate] += sum(self.profil.loc[place_pos] == num_candidate+1) * (place_pos+1)
            mean_rank[num_candidate] /= nb_votes

        fig, ax = plt.subplots()
        labels = [i for i in range(1, nb_candidates+1)]
        plt.scatter(labels, mean_rank)

        ax.set_ylabel('rank mean')
        title = "Rank mean by candidate"
        ax.set_title(title)
        ax.set_xticks(labels)
        ax.invert_yaxis()

        fig.tight_layout()

        plt.savefig(figPath / f"{self.profilName}-{title.replace(' ', '_')}.png")
        plt.show()
        print(mean_rank)

    def update_all_rank(self, all_rank, nb_candidates, nb_place_pos, new_df):
        # for nb vote by candidate by rank
        for place_pos in range(nb_place_pos):
            for candidate_num in range(nb_candidates):
                all_rank[place_pos + 1][candidate_num] += sum(new_df.loc[place_pos] == candidate_num + 1)

    def update_all_mean_rank(self, all_mean_rank, nb_candidates, nb_votes, new_df):
        # for mean_rank
        mean_rank = [0 for _ in range(nb_candidates)]
        for num_candidate in range(nb_candidates):
            for place_pos in range(nb_candidates):
                mean_rank[num_candidate] += sum(new_df.loc[place_pos] == num_candidate + 1) * (place_pos + 1)
            mean_rank[num_candidate] /= nb_votes
        all_mean_rank.append(mean_rank.copy())

    def plot_bootstrap_mean_rank(self, means_means, n_strap, nb_candidates, n_frac_votes):
        # for mean_rank

        fig, ax = plt.subplots()
        ax.set_ylabel('rank mean')
        n_frac_votes_title = n_frac_votes if isinstance(n_frac_votes, int) else f"{n_frac_votes * 100}%"
        title = f"Mean of rank mean by candidate (boostrap {n_strap} - vote {n_frac_votes_title})"
        ax.set_title(title)
        labels = [i for i in range(1, len(means_means) + 1)]
        plt.scatter(labels, means_means)
        ax.invert_yaxis()
        plt.savefig(figPath / f"{self.profilName}-{title.replace(' ', '_')}.png")
        plt.show()

    def plot_bootstrap_nb_vote_by_candidate_and_rank(self, all_rank, nb_candidates, nb_place_pos, n_strap, n_frac_votes):
        width = 0.35
        shift_factor = 5  # facteur pour le décalage des rangs (1er, 2nd, ...) dans l'histogramme
        label_factor = 2

        # for nb vote / candidate-rank
        for key in all_rank.keys():
            all_rank[key] = np.array(all_rank[key]) / n_strap

        labels = np.array([i for i in range(1, nb_candidates + 1)])
        fig, ax = plt.subplots()
        shift = shift_factor * (np.arange(nb_place_pos) - (nb_place_pos - 1) * 0.5)
        for place_pos, add in zip(range(1, nb_place_pos + 1), shift):
            rects = ax.bar(label_factor * labels + (add * width / nb_place_pos), all_rank[place_pos], width,
                           label=place_pos)
            ax.bar_label(rects, padding=3, rotation=-90)
        ax.set_ylabel('NB Vote')
        n_frac_votes_title = n_frac_votes if isinstance(n_frac_votes, int) else f"{n_frac_votes * 100}%"
        title = f"Number of votes by candidate and rank (boostrap {n_strap} - vote {n_frac_votes_title})"
        ax.set_title(title)
        ax.set_xticks(label_factor * labels, labels)
        ax.legend()
        plt.margins(.02, .15)
        fig.tight_layout()
        plt.savefig(figPath / f"{self.profilName}-{title.replace(' ', '_')}.png")
        plt.show()

    def boostrap_analysis(self, n_strap=10):
        blueprint("Analyse de robustesse Bootstrap")
        vote_methods = [OneRoundVote, TwoRoundVote, AlternativeRoundVote, Borda, Condorcet]
        winners_by_method = {vote_method.__name__: [] for vote_method in vote_methods}
        means_mean_rank_by_candidate = {candidate + 1: [] for candidate in range(self.profil.shape[0])}
        stds_mean_rank_by_candidate = {candidate + 1: [] for candidate in range(self.profil.shape[0])}
        to_plot = [10, 50, 100]
        tbar = trange(1, 101, 1)#self.profil.shape[1])
        for i in tbar:
            nb_votes = int(i/100 * self.profil.shape[1])
            tbar.set_postfix_str(f"Bootstrap analysis for {nb_votes} votes, {n_strap} straps")
            bootstrap_res = self._boostrap_analysis(n_strap, i / 100, plot=i in to_plot)
            for key in winners_by_method.keys():
                winners_by_method[key].append(bootstrap_res["winners_by_method"][key])
            for candidate in bootstrap_res["mean_mean_rank_by_candidate"].keys():
                means_mean_rank_by_candidate[candidate].append(bootstrap_res["mean_mean_rank_by_candidate"][candidate])
            for candidate in bootstrap_res["std_mean_rank_by_candidate"].keys():
                stds_mean_rank_by_candidate[candidate].append(bootstrap_res["std_mean_rank_by_candidate"][candidate])

        # plot means_rank and std
        for candidate in stds_mean_rank_by_candidate.keys():
            plt.plot(stds_mean_rank_by_candidate[candidate], label=f"candidate {candidate}")
        title = "standard deviation of rank mean by candidate\n"+ f"by percentage of vote (bootstrap {n_strap})"
        plt.title(title)
        ax = plt.gca()
        ax.set_ylabel('Standard deviation of rank mean')
        ax.set_xlabel('Percentage of the original number of votes')
        ax.set_xticklabels([f"{y}%" for y in ax.get_xticks()])
        plt.legend()
        title = title.replace(' ', '_').replace('\n', '_')
        plt.savefig(figPath / f"{self.profilName}-{title}.png")
        plt.show()

        for candidate in means_mean_rank_by_candidate.keys():
            plt.plot(means_mean_rank_by_candidate[candidate])
        title = "Mean of rank mean by candidate\n" + f"by percentage of vote (bootstrap {n_strap})"
        plt.title(title)
        ax = plt.gca()
        ax.set_ylabel('Mean of rank mean')
        ax.set_xlabel('Percentage of the original number of votes')
        ax.set_xticklabels([f"{y}%" for y in ax.get_xticks()])
        plt.legend()
        title = title.replace(' ', '_').replace('\n', '_')
        plt.savefig(figPath / f"{self.profilName}-{title}.png")
        plt.show()

        #pprint(winners_by_method)

        # Plot by methods
        for vote_method in vote_methods:
            x = []
            y = []
            c = []
            for i, line in enumerate(winners_by_method[vote_method.__name__]):
                offsets = {i: 0 for i in set(line)}
                for element in line:
                    x.append(i)
                    offsets[element] += 0.05
                    if element is None:
                        y.append(0 + offsets[element])
                        c.append("#ff7f0e")
                    else:
                        y.append(element + offsets[element])
                        c.append("#1f77b4")
            plt.scatter(x, y, c=c, marker="s")
            ax = plt.gca()

            title = f"Sturdiness Analysis for {vote_method.__name__} (Bootstrap {n_strap})"
            plt.title(title)
            plt.yticks(np.arange(0, self.profil.shape[0]))
            ax.set_xticklabels([f"{y}%" for y in ax.get_xticks()])
            ax.set_ylabel('Candidate')
            ax.set_xlabel('Percentage of the original number of votes')
            plt.savefig(figPath / f"{self.profilName}-{title.replace(' ', '_')}.png")
            plt.show()

    def _boostrap_analysis(self, n_strap=10, n_frac_votes=1., plot=True):
        df = pd.DataFrame(self.profil)
        nb_candidates = self.profil.shape[0]
        if isinstance(n_frac_votes, int):
            nb_votes = n_frac_votes
        else:
            nb_votes = int(n_frac_votes * self.profil.shape[1])
        assert nb_votes <= self.profil.shape[1]

        all_mean_rank = []  # for mean_rank
        if plot:
            # for nb vote / candidate-rank
            nb_place_pos = 3
            all_rank = {place_pos + 1: [0 for _ in range(nb_candidates)] for place_pos in range(nb_place_pos)}

        vote_methods = [OneRoundVote, TwoRoundVote, AlternativeRoundVote, Borda, Condorcet]
        winners_by_method = {vote_method.__name__: [] for vote_method in vote_methods}
        for _ in range(n_strap):
            new_df = df.sample(n=nb_votes, replace=True, axis=1)
            new_df = new_df.set_axis(range(nb_votes), axis=1)

            self.update_all_mean_rank(all_mean_rank, nb_candidates, nb_votes, new_df)  # for mean_rank
            if plot:
                self.update_all_rank(all_rank, nb_candidates, nb_place_pos, new_df)  # for nb vote / candidate-rank

            for vote_method in vote_methods:
                voter = vote_method(new_df)
                winners_by_method[vote_method.__name__].append(voter.vote()["winner"]["candidate"])

        mean_mean_rank_by_candidate = {}
        std_mean_rank_by_candidate = {}
        all_mean_rank = np.array(all_mean_rank).T
        means_means = []
        for candidate in range(nb_candidates):
            means_means.append(np.mean(all_mean_rank[candidate]))
            mean_mean_rank_by_candidate[candidate + 1] = np.mean(all_mean_rank[candidate])
            std_mean_rank_by_candidate[candidate + 1] = np.std(all_mean_rank[candidate])

        if plot:
            for candidate in range(nb_candidates):
                print(f"candidate {candidate + 1} - std {std_mean_rank_by_candidate[candidate+1]:.5} \tmean {mean_mean_rank_by_candidate[candidate+1]:.5}")
            self.plot_bootstrap_mean_rank(means_means, n_strap, nb_candidates, n_frac_votes)
            self.plot_bootstrap_nb_vote_by_candidate_and_rank(all_rank, nb_candidates, nb_place_pos, n_strap, n_frac_votes)

        res = {"winners_by_method": winners_by_method,
               "mean_mean_rank_by_candidate": mean_mean_rank_by_candidate,
               "std_mean_rank_by_candidate": std_mean_rank_by_candidate}

        return res




