"""
Operaatio Anthophila – Python Text Adventure
© 2026 Pirjo Keskinen. Original work. All rights reserved.

All story elements, locations, and characters are original creations.
"""

class Pelaaja:
    def __init__(self):
        self.esineet = []           # Esineet, joita pelaajalla on
        self.pisteet = 0            # Pelaajan pisteet
        self.palautetut = []        # Kasvihuoneeseen palautetut esineet
        self.varusteet = set()      # Päällä olevat varusteet (suojapuku, happipullo)
        self.happi = None           # Hapen määrä
        self.loukkaantunut = False  # Onko pelaaja loukkaantunut
        self.autiomaa_reitti = []   # Reitti autiomaassa (eksymisen seuranta)
        self.autiomaassa = False    # Onko pelaaja autiomaassa
        self.piste_esineet = set()  # Mistä esineistä pisteet on jo annettu

    # Pisteet
    def lisaa_pisteet(self, maara, syy=""):
        self.pisteet += maara
        if syy:
            print(f"{syy} +{maara} pistettä")

    # Ota
    def ota(self, esine):
        if esine in self.esineet:
            print("Sinulla on jo tämä esine.")
            return
        self.esineet.append(esine)
        if esine not in self.piste_esineet:
            if esine == "suojapuku":
                self.lisaa_pisteet(10, "Otit suojapuvun")
            elif esine == "omena":
                self.lisaa_pisteet(10, "Otit omenan")
            elif esine == "sulake":
                self.lisaa_pisteet(20, "Otit sulakkeen")
            elif esine == "kulkukortti":
                self.lisaa_pisteet(10, "Otit kulkukortin")
            elif esine == "happipullo":
                self.lisaa_pisteet(10, "Otit happipullon")
            elif esine == "päiväkirja":
                self.lisaa_pisteet(10, "Otit päiväkirjan")
            elif esine == "korjausmoduuli":
                self.lisaa_pisteet(20, "Otit korjausmoduulin")
            elif esine == "rele":
                self.lisaa_pisteet(20, "Otit releen")
            self.piste_esineet.add(esine)

    # Pudota
    def pudota(self, esine):
        if esine in self.esineet:
            self.esineet.remove(esine)
            print(f"Pudotit esineen: {esine}")
            return True
        return False

    # Mukana
    def mukana(self):
        print(f"Pisteet: {self.pisteet}")
        if self.esineet:
            print("Mukanasi on: ")
            for e in self.esineet:
                print(f"- {e}")
        else:
            print("Sinulla ei ole mitään.")

    # Asenna
    def asenna(self, esine):
        if esine in self.esineet:
            self.esineet.remove(esine)
            self.palautetut.append(esine)
            self.lisaa_pisteet(50, f"Asensit {esine}")
            return True
        return False

    # Pue
    def pue(self, esine):
        if esine not in self.esineet:
            print("Sinulla ei ole tätä esinettä.")
            return False
        if esine in self.varusteet:
            print("Sinulla on tämä jo puettuna.")
            return False
        if esine not in ("suojapuku", "happipullo"):
            print("Tätä esinettä ei voi pukea.")
            return False

        self.varusteet.add(esine)
        self.lisaa_pisteet(20, f"Puit päälle: {esine}")
        if {"suojapuku", "happipullo"}.issubset(self.varusteet):
            if self.happi is None:
                self.happi = 100
                print("Happijärjestelmä aktivoitu! Happi: 100 %")
        return True

    # Hapen kulutus
    def hapen_kulutus(self):
        if self.loukkaantunut:
            return 3
        return 2

    # Seuraataan pelaajan liikeet autiomaassa ja tallennetaan reitti taulukkoon
    def aloita_autiomaa(self):
        self.autiomaassa = True
        self.autiomaa_reitti = []

    def poistu_autiomaasta(self):
        self.autiomaassa = False
        self.autiomaa_reitti = []

    def vastakkainen_suunta(self, suunta):
        vastakkaiset = {
            "pohjoinen": "etelä",
            "etelä": "pohjoinen",
            "itä": "länsi",
            "länsi": "itä"
        }
        return vastakkaiset.get(suunta)
