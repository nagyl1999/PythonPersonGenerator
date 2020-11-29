import sys
import pandas
import random
import requests

# Nevek listájának URL-jei
vez_url = "https://nyilvantarto.hu/letoltes/statisztikak/kozerdeku_csaladnev_2020.xlsx"
fiu_url = "http://www.nytud.mta.hu/oszt/nyelvmuvelo/utonevek/osszesffi.txt"
lany_url = "http://www.nytud.mta.hu/oszt/nyelvmuvelo/utonevek/osszesnoi.txt"

class Domain:
    """ Népszerű email szolgáltatók domainjei """
    domain = ["gmail.com", "outlook.com", "wow.com", "ymail.com", "inbox.com", "yahoo.com", "hotmail.com", "mail.com", "msn.com", "live.com", "me.com", "hotmail.co.uk"]

class Person:
    """ Egy személy modellje """
    def __init__(self, sur, name):
        """ Véletlenszerű születési idő """
        self.born = random.randint(1950, 2010)
        self.name = [sur.getName(), name.getName()]
        self.age = 2020 - self.born
        self.email = self.genEmail()
        self.fullname = self.genName()

    def genName(self):
        """ Név formátum """
        return " ".join(self.name)

    def genEmailStr(self):
        """ Véletlenszerű email név generálás """
        addr = [text.lower() for text in [random.choice(self.name), random.choice([str(self.age), str(self.born)])]]
        random.shuffle(addr)
        return "{}".format("".join(addr))

    def genEmail(self):
        """ Email cím <-> egyik név, születés vagy kor, és egy népszerű domain """
        return "{}@{}".format(self.genEmailStr(), random.choice(Domain.domain))

    def __str__(self):
        """ Sztring formátum """
        return "{} {}".format(self.fullname, self.email)

class Name:
    """ Közös ős a neveket tároló osztályok számára """
    def __init__(self, url):
        """ Közös adatok, és függvények, de különböző feldolgozás """
        self.url = url
        self.names = list()

    def getName(self):
        """ Egy véletlenszerű név visszaadása """
        return random.choice(self.names)

class Firstname(Name):
    """ Keresztneveket tároló osztály """
    def __init__(self, url):
        """ Nevek letöltése és megfelelő adatszerkezetbe rendezése """
        super().__init__(url)
        self.names = [name.strip() for name in requests.get(self.url).text.split('\n')[1:] if name.strip()]

class Lastname(Name):
    """ Vezetékneveket tároló osztály """
    def __init__(self, url):
        """ Nevek letöltése és megfelelő adatszerkezetbe rendezése """
        super().__init__(url)
        self.names = [name.capitalize() for name in pandas.read_excel(self.url, "2020_CSALADINEV")['Születési családi név'].tolist()]

class Generate:
    """ A generálásért felelős osztály """
    def __init__(self):
        """ Nevek letöltése """
        self.name = (Lastname(vez_url), [Firstname(fiu_url), Firstname(lany_url)])

    def generatePerson(self, db):
        """ Véletlenszerű adatok generálása """
        return [Person(self.name[0], random.choice(self.name[1])) for _ in range(db)]

def main():
    """ Fő metódus """
    people = Generate().generatePerson(10)
    for person in people:
        print(person)

main()
