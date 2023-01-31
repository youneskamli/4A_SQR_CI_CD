from flask import Flask, request
from Personne import Personne
from operator import itemgetter
import csv
import os
import sys

app = Flask(__name__)
 
listTransac = [(1, 2, 6, 11), (1, 3, 3, 1), (2, 3, 16, 19)]
listPersonne = []
P1 = Personne(1, "Younes", "KAMLI", 50)
listPersonne.append(P1)
P2 = Personne(2, "Loann", "LE THIES", 50)
listPersonne.append(P2)
P3 = Personne(3, "Naofel", "EL ALOUANI", 50)
listPersonne.append(P3)

#url = "transaction.csv"
#texte = pd.read_csv(url)

#Affiche le tuple sous la forme d'un string
def tuple_display(tuple: tuple):
    string = str(tuple[0]) + " a donné " + str(tuple[3]) + " euros à " + str(tuple[1]) + " à " + str(tuple[2]) + " heures"
    return string

#Affiche une liste de tuple sous la fomre d'un string
def display_list(list: list):
    string = ""
    list = sort_list(list)
    for element in list:
        string += "<p>" + tuple_display(element) + "</p> \n"
    return string

#Trie une liste de tuple selon leur date (3eme element du tuple)
def sort_list(list: list):
    list = sorted(list, key=itemgetter(2))
    return list

#Décrémenter le compte d'une personne après transaction 
def donate(id : int, somme : int):
    for element in listPersonne:
        if element.id == id:
            element.solde -= somme

#Incrémenter le compte d'une personne après transaction
def receive(id : int, somme : int):
    for element in listPersonne:
        if element.id == id:
            element.solde += somme

#Route pincipale
@app.route('/', methods=['GET'])
def get():
    return 'Projet'

#Route pour E1 et E2
@app.route('/transaction', methods=['POST', 'GET'])
def display():
    tuplet = ("", "", "", "")
    if request.method == "POST":
        personne1 = int(request.form.get("personne1"))
        personne2 = int(request.form.get("personne2"))
        temps = int(request.form.get("temps"))
        somme = int(request.form.get("somme"))
        tuplet = (personne1, personne2, temps, somme)
        listTransac.append(tuplet)

        donate(personne1, somme)
        receive(personne2, somme)
 
    return display_list(listTransac)

#Route pour E3
@app.route('/personne', methods=['GET'])
def getTransaction():
    listTransacPersonne = []
    personne = int(request.args.get("personne"))
    for element in listTransac:
        if element[0] == personne or element[1] == personne:
            listTransacPersonne.append(element)
            
    return display_list(listTransacPersonne)

@app.route('/solde', methods=['GET'])
def getSolde():
    solde_personne = ""
    personne = int(request.args.get("personne"))
    for element in listPersonne:
        if element.id == personne:
            solde_personne += str(element.solde)
            
    return solde_personne

@app.route('/csv', methods=['POST', 'GET'])
def getcsv():
    tuplet = ("", "", "", "")
    P1 = 0
    P2 = 0
    t = 0
    s = 0
    compteur = 0
    if request.method == "POST":
        if request.files:
            f = request.files['file']
            chemin = os.path.join(f.filename)
            f.save(chemin)

            with open(chemin) as file:
                cr = csv.reader(file, delimiter=';')
                for row in cr:
                    if compteur != 0:
                        P1 = int(row[0])
                        P2 = int(row[1])
                        t = int(row[2])
                        s = int(row[3])
                        tuplet = (P1, P2, t, s)
                        listTransac.append(tuplet)
                    compteur += 1
        else:
            print("Ca marche pas")
    return display_list(listTransac)

    '''tuplet = ("", "", "", "")
    if request.method == "POST":
        if request.files:
            f = request.files['file']

        with open('transaction.csv') as fichier_csv:
            lecteur_csv = csv.reader(fichier_csv)
            for ligne in lecteur_csv:
                if(ligne[0] != "Donneur"):
                    tuplet = (int(ligne[0]), int(ligne[1]), int(ligne[2]), int(ligne[3]))
                    listTransac.append(tuplet)
    return  display_list(listTransac)'''

#Check_syntax
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)

#curl -X POST -d "personne1=1&personne2=2&temps=10&somme=50" http://localhost:5000/transaction
#curl -X POST -F 'file=@transaction.csv' http://localhost:5000/csv
