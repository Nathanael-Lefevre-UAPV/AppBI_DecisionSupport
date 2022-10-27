import os

# Keys
CHOIX_SOCIAL = "CHOIX_SOCIAL"
HEVEA = "HEVEA"
PAYS = "PAYS"
TRAITEMENT_DECHETS = "TRAITEMENT_DECHETS"
VOITURE = "VOITURE"

dataRoot = os.path.dirname(__file__)
dataPaths = {CHOIX_SOCIAL: f"{dataRoot}/Choix social-20221027",
             HEVEA: f"{dataRoot}/Hevea-20221027",
             PAYS: f"{dataRoot}/Pays-20221027",
             TRAITEMENT_DECHETS: f"{dataRoot}/Traitement Déchets-20221027",
             VOITURE: f"{dataRoot}/Voiture-20221027"}
