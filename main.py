from flask import Flask, request
from Personne import Personne
from operator import itemgetter
import sys

app = Flask(__name__)
 
listTransac = [(1, 2, 5, 10), (1, 3, 30, 15), (2, 3, 10, 11)]
listPersonne = []
P1 = Personne(1, "Younes", "KAMLI", 50)
listPersonne.append(P1)
P2 = Personne(2, "Loann", "LE THIES", 50)
listPersonne.append(P2)
P3 = Personne(3, "Naofel", "EL ALOUANI", 50)
listPersonne.append(P3)

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
#