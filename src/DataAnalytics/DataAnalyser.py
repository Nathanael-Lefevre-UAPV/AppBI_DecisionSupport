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

        labels = np.array([i for i in range(profil.shape[0])])
        width = 0.35

        fig, ax = plt.subplots()
        nb_place_pos += 1
        shift = np.arange(nb_place_pos) - nb_place_pos / 2
        input(shift)
        for place_pos, add in zip(range(1, nb_place_pos+1), [-6, 0, 6]):
            rects = ax.bar(2*labels + (add * width / nb_place_pos), rank[place_pos], width, label=place_pos)
            ax.bar_label(rects, padding=3)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('NB Vote')
        ax.set_title('Number of votes by candidate and rank')
        ax.set_xticks(2*labels, labels)
        ax.legend()

        fig.tight_layout()

        plt.show()

        print(rank)

