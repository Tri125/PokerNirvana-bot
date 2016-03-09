# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup


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


def Partie(html):
    listParties = []

    soup = BeautifulSoup(html, 'html.parser')
    elementsNomAfficher = soup.find_all('td', class_="AccueilParoleALog")

    #print(elementsParti)

    for each in elementsNomAfficher:
        boutonParti = each.find_parent("tr").find("button")
        listParties.append(boutonParti.get_text())
    return listParties


def LogiqueJeu(actions):
    postParams = {}
    if 'GRATOS' in actions:
        postParams[actions['GRATOS']] = 'GRATOS'
    if 'SUIVRE' in actions:
        postParams[actions['SUIVRE']] = 'SUIVRE'
    if 'ValeurRelance' in actions:
        postParams['ValeurRelance'] = actions['ValeurRelance']
    return postParams


def Jouer(html):
    formulaire = dict()
    soup = BeautifulSoup(html, 'html.parser')
    elementsInput = soup.find('form').find_all('input')
    #print(elementsActions)

    for each in elementsInput:
        #print(each)
        if each.has_attr('name'):
            #print(each['name'])
            formulaire[each['value']] = each['name']
    elementsSelect = soup.find('form').find_all('select')

    for each in elementsSelect:
        #print(each)
        if each.has_attr('name'):
            #print(each['name'])
            formulaire[each['name']] = each.find('option').get_text()

    #for k, v in formulaire.items():
        #print(k, v)
    action = LogiqueJeu(formulaire)
    #print(action)

    return action

#DECISION: GRATOS ABANDONNER RELANCER ValeurRelance

#NouvelleMain ,Position, Passer la prochain main