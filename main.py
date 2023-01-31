from flask import Flask, request
from Personne import Personne
from operator import itemgetter
import csv
import os
import sys
import hashlib

app = Flask(__name__)

#Declaration d'une liste de personnes que qui stocjera des objets de type Personne 
listPersonne = []
P1 = Personne(1, "Younes", "KAMLI", 50)
listPersonne.append(P1)
P2 = Personne(2, "Loann", "LE THIES", 60)
listPersonne.append(P2)
P3 = Personne(3, "Naofel", "EL ALOUANI", 70)
listPersonne.append(P3)

#Fonction donnant le hash sha256
def getHash(P1 : str, P2 : str, s : str, t : str):
    input_string = P1 + P2 + s + t
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode())
    return sha256.hexdigest()

#Fonction permmettant de retrouver le nom et prénom d'une personne depuis son id
def getNameById(id : int):
    nom = ""
    prenom = ""
    for element in listPersonne:
        if element.id == id :
            nom = element.lastName
            prenom = element.firstName
    return nom + " " + prenom + " "

#Ajout d'une liste de transactions avec des transactions par défaut
listTransac = [(1, 2, 6, 11, getHash(str(1), str(2), str(11), str(6))), (1, 3, 3, 1, getHash(str(1), str(3), str(1), str(3))), (2, 3, 16, 19, getHash(str(2), str(3), str(19), str(16)))]

#Affiche le tuple sous la forme d'un string
def tuple_display(tuple: tuple):
    string = str(getNameById(tuple[0])) + " a donné " + str(tuple[3]) + " euros à " + getNameById(tuple[1]) + " à " + str(tuple[2]) + " heures. Le hash correspondant est : " + str(tuple[4])
    return string

#Affiche une liste de tuple sous la forme d'un string
def display_list(list: list):
    string = ""
    list = sort_list(list)
    for element in list:
        string += "<p>" + tuple_display(element) + "</p> \n"
    return string

#Trier une liste de tuple selon leur date (3eme element du tuple)
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
        hash = getHash(str(personne1), str(personne2), str(somme), str(temps))
        tuplet = (personne1, personne2, temps, somme, hash)
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

#Route pour E4
@app.route('/solde', methods=['GET'])
def getSolde():
    solde_personne = ""
    personne = int(request.args.get("personne"))
    for element in listPersonne:
        if element.id == personne:
            solde_personne += str(element.solde)
            
    return solde_personne

#Route pour E5
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
                        tuplet = (P1, P2, t, s, getHash(str(P1), str(P2), str(s), str(t)))
                        listTransac.append(tuplet)
                    compteur += 1
        else:
            print("Error")
    return display_list(listTransac)

#Checker si une transaction existe déjà ou non
@app.route('/integrity', methods=['POST', 'GET'])
def integrity():
    if request.method == "POST":
        personne1 = request.form.get("personne1")
        personne2 = request.form.get("personne2")
        temps = request.form.get("temps")
        somme = request.form.get("somme")
        for transaction in listTransac:
            if(getHash(personne1, personne2, somme, temps) == getHash(str(transaction[0]), str(transaction[1]), str(transaction[3]), str(transaction[2]))):
                return "<p> La transaction existe </p> \n"
        return "<p> La transaction n'existe pas </p> \n"
    return "<p> En attente d'une transaction... </p> \n"

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

#Liste des commandes (resp E1/E2, E3, E4, E5, integrite)
#curl -X POST -d "personne1=1&personne2=2&temps=10&somme=50" http://localhost:5000/transaction
#http://localhost:5000/personne?personne=<id>
#http://localhost:5000/solde?personne=<id>
#curl -X POST -F 'file=@transaction.csv' http://localhost:5000/csv
#curl -X POST -d "personne1=1&personne2=2&temps=10&somme=50" http://localhost:5000/integrity