# -*- coding: utf-8 -*-

import bisect
import re
from bs4 import BeautifulSoup

NO_TOURNAMENT = '-1'


def filter_form_game(element):
    return element.name == 'input' or element.name == 'select'


def hasMultipleSubmit(elements):
    nbrSubmit = 0

    for element in elements:
        if element.has_attr('type') and element['type'] == 'submit':
            nbrSubmit += 1
    return nbrSubmit > 1


def jeuChangementStatut(formulaire):
    requeteFormer = {}

    for each in formulaire:
        if each.has_attr('name'):
            requeteFormer[each['name']] = (each['value'] if each.has_attr('value') else '')
        elif each.has_attr('type') and each['type'] == 'submit':
            requeteFormer[each['value']] = ''
    return requeteFormer


def Tournoi(html):
    numTournoi = []

    soup = BeautifulSoup(html, 'html.parser')
    elementsTournoi = soup.find_all('td', text=re.compile("Tournoi"))
    #print(elementsTournoi)

    regexTournoi = re.compile("[0-9]+")

    for each in elementsTournoi:
        text = each.get_text()
        #print(text)
        numTournoi.append(regexTournoi.search(text).group(0))
    return numTournoi

def TournoiPartie(html, username):
    games = {NO_TOURNAMENT: list()}
    soup = BeautifulSoup(html, 'html.parser')
    elementsTable = soup.find_all('table')
    regexNum = re.compile("[0-9]+")
    dernierTournoi = NO_TOURNAMENT

    for table in elementsTable:
        tds = table.find('td', text=re.compile('tournoi', re.IGNORECASE))
        #Table tournoi
        if tds is not None:
            numTournoi = int(regexNum.search(tds.get_text()).group(0))
            games[numTournoi] = list()
            dernierTournoi = numTournoi
        #Table des Parties d'un tournoi
        elif table.find('th', text=re.compile('partie', re.IGNORECASE)) is not None:
            #Partie d'un tournoi
            elementsPartie = table.find_all('td', string=username)

            for partie in elementsPartie:
                btnPartie = partie.find_parent('').find('button')
                numPartie = int(regexNum.search(btnPartie.get_text()).group(0))
                bisect.insort(games[dernierTournoi], numPartie)
            dernierTournoi = NO_TOURNAMENT

    return games


def Partie(html):
    listParties = []

    soup = BeautifulSoup(html, 'html.parser')
    elementsNomAfficher = soup.find_all('td', class_="AccueilParoleALog")

    for each in elementsNomAfficher:
        boutonParti = each.find_parent("tr").find("button")
        listParties.append(boutonParti.get_text())
    return listParties


def jeuDecision(formulaire):
    requeteFormer = {}
    premierChoix = formulaire.pop(0)

    if premierChoix.has_attr('name'):
        requeteFormer[premierChoix['name']] = (premierChoix['value'] if premierChoix.has_attr('value') else '')
    for element in formulaire:
        if element.has_attr('name') and element['name'] == 'Decision' and 'Decision' in requeteFormer:
            #On a déjà une décision
            continue
        else:
            if element.name == 'select' and element.has_attr('name'):
                requeteFormer[element['name']] = element.find('option').get_text()
            else:
                print("Problème jeuDecision")
    return requeteFormer


def PriseDeDecision(info):
    return


def Jouer(html):
    soup = BeautifulSoup(html, 'html.parser')
    elementsInput = soup.find('form').find_all(filter_form_game)
    #print(elementsInput)
    if hasMultipleSubmit(elementsInput):
        #Cas d'un jeu avec Decision (GRATOS ABANDONNER RELANCER ValeurRelance)
        print("Décision à prendre.\n")
        return jeuDecision(elementsInput)
    else:
        #Cas de changement d'état de la partie: #NouvelleMain ,Position, Passer la prochain main
        print("Changement de statut de la partie.\n")
        return jeuChangementStatut(elementsInput)
    return

#DECISION: GRATOS ABANDONNER RELANCER ValeurRelance

#NouvelleMain ,Position, Passer la prochain main