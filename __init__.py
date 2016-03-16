#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import bisect
import json
import argparse
import requests
import pokerHandler

args = {}
loginFile = None

DOMAINE = 'http://420.cstj.qc.ca/alainmartel/pokernirvana'
URL_JEU = '/texas/texas.php'
URL_LOBBY = '/GestionPartie.php'
PARAM_JEU = 'partieEnCours'
login = {'pokerman': '', 'MotDePasse': '', 'valider': ''}
NO_TOURNAMENT = '-1'
listTournoi = None

def login_parser(name):
    if os.path.exists(name):
        with open(name) as data:
            try:
                data = json.load(data)
            except:
                sys.exit("Erreur lors du chargement du fichier \"" + data + "\"")
    else:
        sys.exit("Fichier \"" + name + "\" n'existe pas.")

    if ('username' not in data) or ('password' not in data):
        sys.exit("Fichier \"" + name + "\" ne contient pas un champ login ou password.")
    global loginFile
    loginFile = data

def setParser():
    parser = argparse.ArgumentParser(description='C\'est un script permettant l\'automatisation du jeu PokerNirvana d\'Alain.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-g', '--game', help='Spécifie qu\'elle partie jouer', required=False)
    group.add_argument('-t', '--tournament', help='Spécifie quel tournoi jouer', required=False)

    parser.add_argument('-u', '--username', help='Le nom d\'utilisateur', required=False)
    parser.add_argument('-p', '--password', help='Le mot de passe du compte utilisateur', required=False)
    parser.add_argument('-i', '--input', type=login_parser, help='Fichier json contenant le login', required=False)
    parser.add_argument('-o', '--output', help='Fichier de sortie pour le journal', required=False)
    global args
    args = parser.parse_args()

    if loginFile is not None:
        args.username = loginFile['username']
        args.password = loginFile['password']

def PartieSpecifique(r, s, num):
    global listTournoi
    exist = False

    for key, value in listTournoi.items():
        if num in value:
            exist = True
            print("Partie #", num, " sélectionné.\n")
            print("Partie: ", num, "en cours:")

            paramGET = {PARAM_JEU: num}

            r = s.get(DOMAINE + URL_JEU, params=paramGET)
            r.encoding = 'UTF-8'

            paramAction = pokerHandler.Jouer(r.text)

            print(paramAction)
            r = s.post(DOMAINE + URL_JEU, params=paramGET, data=paramAction)
            break
    if exist is False:
        print("Vous ne pouvez pas jouer à la partie #", num, ".\n")
        return

def TournoiSpecifique(r,s, num):
    global listTournoi
    exist = False

    for key, value in listTournoi.items():
        if num is key:
            exist = True
            print("Tournoi #", num, " sélectionné.\n")
            print("Tournoi: ", num, "en cours:")

            for partiNum in value:
                PartieSpecifique(r, s, partiNum)

            print("Tournoi #", num, " terminé.\n")
            break
    if exist is False:
        print("Vous ne pouvez pas jouer au tournoi #", num, ".\n")
        return

def TouteLesParties(r, s):
    global listTournoi
    print("Parties à votre tour:\n")
    parties = list()
    for listPartie in listTournoi.values():
        for partie in listPartie:
            bisect.insort(parties, partie)
    if len(parties) == 0:
        print("Aucune partie\n")
    else:
        print(parties, "\n")

    for key, listPartie in listTournoi.items():

        for partie in listPartie:
            print("Partie: ", partie, "en cours:")

            paramGET = {PARAM_JEU: partie}

            r = s.get(DOMAINE + URL_JEU, params=paramGET)
            r.encoding = 'UTF-8'

            paramAction = pokerHandler.Jouer(r.text)

            print(paramAction)

            r = s.post(DOMAINE + URL_JEU, params=paramGET, data=paramAction)

            print("Partie suivante.\n")


def main():
    global listTournoi

    login['pokerman'] = args.username
    login['MotDePasse'] = args.password

    print("Début de la session...\n")
    s = requests.Session()

    print("[Connexion]")
    r = s.post(DOMAINE + '/index.php', data=login)

    r.encoding = 'UTF-8'

    if r.status_code == 200:
        print("[Connecté]\n")
    else:
        print("Échec de connexion\n")

    listTournoi = pokerHandler.TournoiPartie(r.text, args.username)

    print("Participe aux tournois:\n")

    if len(listTournoi) == 0:
        print("Aucun")
    else:
        for key in listTournoi.keys():
            if key == NO_TOURNAMENT:
                continue
            else:
                print(key, end="\t")
        print("\n", end="\n")
        if args.game is not None and args.game.isdigit():
            PartieSpecifique(r, s, int(args.game))
        elif args.tournament is not None and args.tournament.isdigit():
            TournoiSpecifique(r, s, int(args.tournament))
        else:
            TouteLesParties(r, s)
    print("[Déconnexion...]")
    #r = s.post(DOMAINE + URL_LOBBY)
    print("[Déconnecté]\n")
    print("Fin\n")

    return

if __name__ == '__main__':
    setParser()
    if args.username is None or args.password is None:
        sys.exit("Nom d'utilisateur et mot de passe non fourni.")
    main()
    input("Appuyez sur une touche\n")