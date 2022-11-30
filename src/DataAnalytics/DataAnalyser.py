import matplotlib

import matplotlib.pyplot as plt
import numpy as np


class DataAnalyser:
    def __init__(self, profil, profil_name):
        self.profil = profil
        self.profilName = profil_name

    def plot_candidates_vote_ranking(self):
        nb_place_pos = 9
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
            ax.bar_label(rects, padding=3)

        ax.set_ylabel('NB Vote')
        title = "Number of votes by candidate and rank"
        ax.set_title(title)
        ax.set_xticks(label_factor*labels, labels)
        ax.legend()

        fig.tight_layout()
        plt.savefig(f"src/fig/{self.profilName}-{title.replace(' ', '_')}.png")
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

        plt.savefig(f"src/fig/{self.profilName}-{title.replace(' ', '_')}.png")
        plt.show()
        print(mean_rank)