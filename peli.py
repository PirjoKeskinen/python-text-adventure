import time
import sys
import threading
from paikat import paikat
from pelaaja import Pelaaja

# Lukee tekstitiedoston sisällön ja palauttaa sen merkkijonona
def lue_tiedosto(tiedostonnimi):
    with open(tiedostonnimi, 'r', encoding='utf-8') as f:
        teksti = f.read()
    return teksti

# Tulostaa tekstin kirjain kerrallaan
def tulosta_hitaasti(teksti, viive = 0.05):
    keskeyta = False
    # Intron voi keskeyttää painamalla enter
    def kuuntele_enter():
        nonlocal keskeyta
        input()
        keskeyta = True

    thread = threading.Thread(target=kuuntele_enter)
    thread.start()

    for kirjain in teksti:
        if keskeyta:
            print("\nIntro ohitettu")
            break
        sys.stdout.write(kirjain)
        sys.stdout.flush()
        time.sleep(viive)
    else:
        print()

# Näyttää pelin intron
tulosta_hitaasti(lue_tiedosto('intro.txt'))

# Tulostaa ohjetekstin
def nayta_ohjeet():
    teksti = lue_tiedosto("apua.txt")
    print(teksti)

# Tulostaa paikan kuvauksen, tarkemman kuvauksen ja paikan esineet
def nayta_paikka(paikka, katsele=False):
    kuvaus = paikat[paikka]['kuvaus']
    if not katsele:
        if "Katsele:" in kuvaus:
            print(kuvaus.split("Katsele:")[0].strip())
        else:
            print(kuvaus)
    else:
        if "Katsele:" in kuvaus:
            print(kuvaus.split("Katsele:")[1].strip())
        else:
            print("Paikalta ei löydy mitään erityistä.")

        esineet = paikat[paikka]['esineet']
        if esineet:
            print("\nTäältä löytyy: ")
            for e in esineet:
                print(f"- {e}")

def peli():
    # Pelaajan aloituspaikka
    nykyinen_paikka = 'kasvihuone'
    pelaaja = Pelaaja()

    print("Peli alkaa!\nSaat tarvittaessa apua kirjoittamalla 'apua'\n")
    nayta_paikka(nykyinen_paikka)

    # Paikat, joissa tarvitaan suojapuku ja happipullo
    ulkopaikat = {
        "roskameri",
        "ulkomaailma",
        "myrkkylammikko",
        "ranta",
        "mökki",
        "pelto",
        "autiomaa",
        "metsä",
        "kaupunki",
        "torni",
        "tasanne",
        "hylätty_kasvihuone"
    }

    # Pelin pääsilmukka
    while True:
        komento = input("\n>>> ").strip().lower()

        # Liikkuminen
        if komento.startswith("mene "):
            suunta = komento.split(" ", 1)[1]

            # Pelaaja autiomaassa, happi vähenee -5% ja muistettava reitti takaisin
            if pelaaja.autiomaassa:
                pelaaja.happi -= 5
                if pelaaja.happi <= 0:
                    pelaaja.happi = 0
                    tulosta_hitaasti(lue_tiedosto("happi_loppu.txt"))
                    print("\nPELI PÄÄTTYI.")
                    print(f"\nLoppupisteesi: {pelaaja.pisteet}/494")
                    break

                if not pelaaja.autiomaa_reitti:
                    pelaaja.autiomaa_reitti.append(suunta)
                    continue

                viimeisin = pelaaja.autiomaa_reitti[-1]
                vastakkainen = pelaaja.vastakkainen_suunta(viimeisin)

                if suunta == vastakkainen:
                    pelaaja.autiomaa_reitti.pop()
                    print("Kuljet takaisinpäin. Maisema tuntuu tutummalta...")

                    if not pelaaja.autiomaa_reitti:
                        pelaaja.poistu_autiomaasta()
                        nykyinen_paikka = "pelto"
                        print("Sumu väistyy. Olet selvinnyt pois autiomaasta.")
                        nayta_paikka(nykyinen_paikka)
                    continue

                else:
                    pelaaja.autiomaa_reitti.append(suunta)
                    continue

            suunnat = paikat[nykyinen_paikka]['suunnat']

            if suunta not in suunnat or suunnat[suunta] is None:
                print("Tuli seinä vastaan tai suunta ei ole mahdollinen!")
                continue

            edellinen_paikka = nykyinen_paikka
            seuraava_paikka = suunnat[suunta]

            # Kulkukortti hissiin
            if nykyinen_paikka == "hissi" and seuraava_paikka == "ulkomaailma":
                if "kulkukortti" not in pelaaja.esineet:
                    print("Hissi ei liiku, koska sinulla ei ole kulkukorttia!")
                    continue

            # Vaihtoehtoinen loppu, triggeri
            if seuraava_paikka == "meri":
                tulosta_hitaasti(paikat["meri"]["kuvaus"])
                print("\nPELI PÄÄTTYI.")
                print(f"\nLoppupisteesi: {pelaaja.pisteet}/494")
                break

            # Autiomaahan eksyminen
            if nykyinen_paikka == "pelto" and suunta == "itä":
                if not pelaaja.autiomaassa:
                    pelaaja.aloita_autiomaa()
                    nykyinen_paikka = "autiomaa"
                    print("Astut autiomaahan. Sumun keskellä suuntavaistosi pettää...")
                    nayta_paikka("autiomaa")
                    continue

            # Liikkuminen
            nykyinen_paikka = seuraava_paikka
            print(f"\nLiikuit suuntaan: {suunta}.\n")

            # Loukkaantuminen
            if edellinen_paikka == "myrkkylammikko" and seuraava_paikka == "pelto":
                if not pelaaja.loukkaantunut:
                    pelaaja.loukkaantunut = True
                    tulosta_hitaasti(lue_tiedosto("loukkaantunut.txt"))

            nayta_paikka(nykyinen_paikka)

            # Jos pelaajalla ei ole pukenut suojapukua ja happipulloa mennessä ulkomaailmaan
            if nykyinen_paikka in ulkopaikat:
                if not {"suojapuku", "happipullo"}.issubset(pelaaja.varusteet):
                    tulosta_hitaasti(lue_tiedosto("ulkomaailma_kuolema.txt"))
                    print("\nPELI PÄÄTTYI.")
                    print(f"\nLoppupisteesi: {pelaaja.pisteet}/494")
                    break

            # Hapen kulutus ja jos happi loppuu
            if nykyinen_paikka in ulkopaikat and not pelaaja.autiomaassa:
                kulutus = pelaaja.hapen_kulutus()
                pelaaja.happi -= kulutus
                if pelaaja.happi <= 0:
                    pelaaja.happi = 0
                    tulosta_hitaasti(lue_tiedosto("happi_loppu.txt"))
                    print("\nPELI PÄÄTTYI.")
                    print(f"\nLoppupisteesi: {pelaaja.pisteet}/494")
                    break

            if pelaaja.happi is not None and pelaaja.happi <= 0:
                tulosta_hitaasti(lue_tiedosto("happi_loppu.txt"))
                print("\nPELI PÄÄTTYI.")
                print(f"\nLoppupisteesi: {pelaaja.pisteet}/494")
                break

        # Katsele
        elif komento == "katsele":
            nayta_paikka(nykyinen_paikka, katsele=True)
            if nykyinen_paikka == "autiomaa" and pelaaja.autiomaassa:
                tulosta_hitaasti(lue_tiedosto("autiomaa_eksynyt.txt"))

        # Ota
        elif komento.startswith("ota "):
            esine = komento.split(" ", 1)[1]
            if esine in paikat[nykyinen_paikka]['esineet']:
                paikat[nykyinen_paikka]['esineet'].remove(esine)
                pelaaja.ota(esine)
            else:
                print("Täällä ei ole sellaista esinettä.")

        # Pudota
        elif komento.startswith("pudota "):
            esine = komento.split(" ", 1)[1]
            if esine in pelaaja.esineet:
                pelaaja.pudota(esine)
                paikat[nykyinen_paikka]['esineet'].append(esine)

                # Jos pelaaja pudottaa omenan mökille
                if esine == "omena" and nykyinen_paikka == "mökki":
                    pelaaja.lisaa_pisteet(20, "Olipa se kauniisti ajateltu!")
            else:
                print("Sinulla ei ole tätä esinettä.")

        # Jos pelaaja syö omenan
        elif komento.startswith("syö "):
            esine = komento.split(" ", 1)[1]
            if esine == "omena" and esine in pelaaja.esineet:
                pelaaja.esineet.remove(esine)
                pelaaja.lisaa_pisteet(10, "Nam, olipa makea omena!")
            elif esine in pelaaja.esineet:
                print(f"Et voi syödä tätä.")
            else:
                print("Sinulla ei ole tätä esinettä.")

        # Kasvihuoneen komponenttien asentaminen
        elif komento.startswith("asenna "):
            esine = komento.split(" ", 1)[1]
            vaaditut = {"rele", "korjausmoduuli", "sulake"}
            if nykyinen_paikka != "kasvihuone":
                print("Täällä ei ole mitään, mihin voisit käyttää tätä.")
            elif esine not in pelaaja.esineet:
                print("Sinulla ei ole tätä esinettä.")
            elif esine not in vaaditut:
                print("Tätä esinettä ei voi käyttää täällä.")
            else:
                pelaaja.asenna(esine)
                if vaaditut.issubset(set(pelaaja.palautetut)):
                    tulosta_hitaasti("\nKasvihuoneen järjestelmät käynnistyvät...")
                    tulosta_hitaasti("\nValot syttyvät, ilma puhdistuu...")
                    tulosta_hitaasti("\nKasvihuone on jälleen toiminnassa!")

                    # Jäljelle jäänyt happi muunnetaan pisteiksi
                    if pelaaja.happi is not None and pelaaja.happi > 0:
                        happibonus = pelaaja.happi * 2
                        pelaaja.lisaa_pisteet(happibonus, f"Jäljellä ollut happi ({pelaaja.happi} %)")
                    print(f"\nLoppupisteesi: {pelaaja.pisteet}/494")
                    print("\nPELI LÄPI!")
                    break

        # Varusteiden pukeminen
        elif komento.startswith("pue "):
            esine = komento.split(" ", 1)[1]
            pelaaja.pue(esine)

        # Hapen määrän tarkistaminen
        elif komento == "tarkista":
            if pelaaja.happi is not None:
                print(f"Happi: {pelaaja.happi} %")
            else:
                print(f"Happijärjestelmä ei ole käytössä.")
            if pelaaja.loukkaantunut:
                print("Olet loukkaantunut: hengitys kuluttaa enemmän happea.")
            else:
                print("Sinulla ei ole varusteita päällä.")

        # Mukana olevat tavarat
        elif komento in ("mukana", "esineet"):
            pelaaja.mukana()

        # Lue
        elif komento.startswith("lue "):
            esine = komento.split(" ", 1)[1]
            if esine == "päiväkirja" and esine in pelaaja.esineet:
                teksti = lue_tiedosto("päiväkirja.txt")
                tulosta_hitaasti(teksti)
                pelaaja.lisaa_pisteet(10, "Olipa se surullinen kirjoitus...")

            elif esine in pelaaja.esineet:
                print(f"Et voi lukea tämän esineen sisältöä.")
            else:
                print(f"Sinulla ei ole tätä esinettä.")

        # Lopeta
        elif komento == "lopeta":
            print("Peli lopetettu.")
            break

        # Apua
        elif komento == "apua":
            nayta_ohjeet()

        else:
            print("Tuntematon komento.")

if __name__ == "__main__":
    peli()
