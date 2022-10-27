import pandas as pd
from Data import *

if __name__ == "__main__":
    profile_1 = pd.read_csv(f"{dataPaths[CHOIX_SOCIAL]}/profil1.csv")
    print(profile_1.transpose())