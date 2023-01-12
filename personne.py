class Personne:
    id:int
    firstName:str
    lastName:str
    solde:float

    def __init__(self, firstName, lastName, solde):
        self.firstName = firstName
        self.lastName = lastName
        self.solde = solde
