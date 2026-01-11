"""
Operaatio Anthophila – Python Text Adventure
© 2026 Pirjo Keskinen. Original work. All rights reserved.

All story elements, locations, and characters are original creations.
"""

def lue_tiedosto(tiedostonnimi):
    with  open(tiedostonnimi, 'r', encoding='utf-8') as f:
        return f.read()

paikat = {
    'kasvihuone': {
        'nimi': 'kasvihuone',
        'kuvaus': lue_tiedosto('kasvihuone.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'huoltovarasto',
            'itä': 'aula',
            'etelä': None,
            'länsi': None
        }
    },
    'aula': {
        'nimi': 'aula',
        'kuvaus': lue_tiedosto('aula.txt'),
        'esineet': ['suojapuku'],
        'suunnat': {
            'pohjoinen': 'hissi',
            'itä': 'keittiö',
            'etelä': None,
            'länsi': 'kasvihuone'
        }
    },
    'keittiö': {
        'nimi': 'keittiö',
        'kuvaus': lue_tiedosto('keittiö.txt'),
        'esineet': ['omena'],
        'suunnat': {
            'pohjoinen': 'huone',
            'itä': 'elintila',
            'etelä': None,
            'länsi': 'aula'
        }
    },
    'elintila': {
        'nimi': 'elintila',
        'kuvaus': lue_tiedosto('elintila.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'lääkintä',
            'itä': None,
            'etelä': None,
            'länsi': 'keittiö'
        }
    },
    'huoltovarasto': {
        'nimi': 'huoltovarasto',
        'kuvaus': lue_tiedosto('huoltovarasto.txt'),
        'esineet': ['sulake'],
        'suunnat': {
            'pohjoinen': None,
            'itä': 'hissi',
            'etelä': 'kasvihuone',
            'länsi': None
        }
    },
    'hissi': {
        'nimi': 'hissi',
        'kuvaus': lue_tiedosto('hissi.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'ulkomaailma',
            'itä': 'huone',
            'etelä': 'aula',
            'länsi': 'huoltovarasto'
        }
    },
    'huone': {
        'nimi': 'huone',
        'kuvaus': lue_tiedosto('huone.txt'),
        'esineet': ['kulkukortti'],
        'suunnat': {
            'pohjoinen': None,
            'itä': 'lääkintä',
            'etelä': 'keittiö',
            'länsi': 'hissi'
        }
    },
    'lääkintä': {
        'nimi': 'lääkintä',
        'kuvaus': lue_tiedosto('lääkintä.txt'),
        'esineet': ['happipullo'],
        'suunnat': {
            'pohjoinen': None,
            'itä': None,
            'etelä': 'elintila',
            'länsi': 'huone'
        }
    },
    'roskameri': {
        'nimi': 'roskameri',
        'kuvaus': lue_tiedosto('roskameri.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'ranta',
            'itä': 'ulkomaailma',
            'etelä': None,
            'länsi': None
        }
    },
    'ulkomaailma': {
        'nimi': 'ulkomaailma',
        'kuvaus': lue_tiedosto('ulkomaailma.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'mökki',
            'itä': 'myrkkylammikko',
            'etelä': 'hissi',
            'länsi': 'roskameri'
        }
    },
    'myrkkylammikko': {
        'nimi': 'myrkkylammikko',
        'kuvaus': lue_tiedosto('myrkkylammikko.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'pelto',
            'itä': None,
            'etelä': None,
            'länsi': 'ulkomaailma'
        }
    },
    'meri': {
        'nimi': 'meri',
        'kuvaus': lue_tiedosto('meri.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': None,
            'itä': None,
            'etelä': None,
            'länsi': None
        }
    },
    'ranta': {
        'nimi': 'ranta',
        'kuvaus': lue_tiedosto('ranta.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'metsä',
            'itä': 'mökki',
            'etelä': 'roskameri',
            'länsi': 'meri'
        }
    },
    'mökki': {
        'nimi': 'mökki',
        'kuvaus': lue_tiedosto('mökki.txt'),
        'esineet': ['päiväkirja'],
        'suunnat': {
            'pohjoinen': 'kaupunki',
            'itä': 'pelto',
            'etelä': 'ulkomaailma',
            'länsi': 'ranta'
        }
    },
    'pelto': {
        'nimi': 'pelto',
        'kuvaus': lue_tiedosto('pelto.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'hylätty_kasvihuone',
            'itä': 'autiomaa',
            'etelä': 'myrkkylammikko',
            'länsi': 'mökki'
        }
    },
    'autiomaa': {
        'nimi': 'autiomaa',
        'kuvaus': lue_tiedosto('autiomaa.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'autiomaa',
            'itä': 'autiomaa',
            'etelä': 'autiomaa',
            'länsi': 'autiomaa'
        }
    },
    'metsä': {
        'nimi': 'metsä',
        'kuvaus': lue_tiedosto('metsä.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': None,
            'itä': 'kaupunki',
            'etelä': 'ranta',
            'länsi': None
        }
    },
    'kaupunki': {
        'nimi': 'kaupunki',
        'kuvaus': lue_tiedosto('kaupunki.txt'),
        'esineet': ['korjausmoduuli'],
        'suunnat': {
            'pohjoinen': None,
            'itä': 'torni',
            'etelä': 'mökki',
            'länsi': 'metsä'
        }
    },
    'torni': {
        'nimi': 'torni',
        'kuvaus': lue_tiedosto('torni.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': 'tasanne',
            'itä': 'hylätty_kasvihuone',
            'etelä': 'pelto',
            'länsi': 'kaupunki'
        }
    },
    'tasanne': {
        'nimi': 'tasanne',
        'kuvaus': lue_tiedosto('tasanne.txt'),
        'esineet': [],
        'suunnat': {
            'pohjoinen': None,
            'itä': None,
            'etelä': 'torni',
            'länsi': None
        }
    },
    'hylätty_kasvihuone': {
        'nimi': 'hylätty_kasvihuone',
        'kuvaus': lue_tiedosto('hylätty_kasvihuone.txt'),
        'esineet': ['rele'],
        'suunnat': {
            'pohjoinen': None,
            'itä': None,
            'etelä': 'pelto',
            'länsi': 'torni'
        }
    },
}
