import matplotlib.pyplot as plt
import numpy as np


class DataAnalyser:
    def plot_candidates_vote_ranking(self, profil):
        rank = {}
        nb_place_pos = 3
        for place_pos in range(nb_place_pos):
            rank[place_pos+1] = []
            for candidate_num in range(profil.shape[0]):
                rank[place_pos+1].append(sum(profil.loc[place_pos] == candidate_num+1))

        labels = [i for i in range(profil.shape[0])]
        width = 0.20
        x = [i-width/nb_place_pos for i in range(nb_place_pos+1)]
        fig, ax = plt.subplots()
        for place_pos in range(1, nb_place_pos+1):
            rects = ax.bar(x[place_pos], rank[place_pos], width, label=place_pos)
            ax.bar_label(rects, padding=3)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Scores')
        ax.set_title('Scores by group and gender')
        ax.set_xticks(labels, labels)
        ax.legend()

        fig.tight_layout()

        plt.show()

        print(rank)

