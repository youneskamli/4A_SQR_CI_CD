from flask import Flask, request
from Personne import Personne
from operator import itemgetter


app = Flask(__name__)

listTransac = []
P1 = Personne("Younes", "KAMLI", 50)
P2 = Personne("Loann", "LE THIES", 100)

def tuple_display(tuple: tuple):
    string = tuple[0] + " a donné " + tuple[3] + " euros à " + tuple[1] + " à " + tuple[2] + " heures"
    return string

def display_list(list: list):
    string = ""
    list = sort_list(list)
    for element in list:
        string += tuple_display(element) + "\n"
    return string
    
def sort_list(list: list):
    list = sorted(list, key=itemgetter(2))
    return list


@app.route('/', methods=['GET'])
def get():
    return 'pouet'
#Faire les transactions avec les ID
@app.route('/transaction', methods=['POST', 'GET'])
def display():
    tuplet =("", "", "", "")
    if request.method == "POST":
        personne1 = request.form.get("personne1")
        personne2 = request.form.get("personne2")
        temps = request.form.get("temps")
        somme = request.form.get("somme")

        tuplet = (personne1, personne2, temps, somme)
        listTransac.append(tuplet)
    return display_list(listTransac)

#curl -X POST -d "personne1=Loann&personne2=Younes&temps=10&somme=50" http://localhost:5000/transaction