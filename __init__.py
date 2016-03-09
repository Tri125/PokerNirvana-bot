# -*- coding: utf-8 -*-

import requests
import pokerHandler

UTILISATEUR = "tristan"
MOT_DE_PASSE = "1081849"
DOMAINE = 'http://420.cstj.qc.ca/alainmartel/pokernirvana'
URL_JEU = '/texas/texas.php'
URL_LOBBY = '/GestionPartie.php'
PARAM_JEU = 'partieEnCours'
login = {'pokerman': UTILISATEUR, 'MotDePasse': MOT_DE_PASSE, 'valider': ''}


def main():
    print("Début de la session...\n")
    s = requests.Session()

    print("[Connexion]")
    r = s.post(DOMAINE + '/index.php', data=login)

    r.encoding = 'UTF-8'

    if r.status_code == 200:
        print("[Connecté]\n")
    else:
        print("Échec de connexion\n")

    listTournoi = pokerHandler.Tournoi(r.text)

    print("Participe aux tournois:")

    if len(listTournoi) == 0:
        print("Aucun")
    else:
        print(listTournoi, "\n")
        print("Parties à votre tour:")

        listParties = pokerHandler.Partie(r.text)

        if len(listParties) == 0:
            print("Aucune partie\n")
        else:
            print(listParties, "\n")

            for parti in listParties:
                print("Partie: ", parti, "en cours:")

                paramGET = {PARAM_JEU: parti}

                r = s.get(DOMAINE + URL_JEU, params=paramGET)
                r.encoding = 'UTF-8'

                paramAction = pokerHandler.Jouer(r.text)

                print(paramAction)

                r = s.post(DOMAINE + URL_JEU, params=paramGET, data=paramAction)

                print("Partie suivante.\n")
                break
    print("[Déconnexion...]")
    #r = s.post(DOMAINE + URL_LOBBY)
    print("[Déconnecté]\n")
    print("Fin\n")

    return

if __name__ == '__main__':
    main()