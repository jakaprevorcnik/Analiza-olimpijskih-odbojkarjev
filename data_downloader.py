import os
import requests
from config import volleyball_frontpage_url, volleyball_directory, frontpage_filename


def download_url_to_string(url):

    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try: #probamo prit do kode
        # del kode, ki morda sproži napako 
        # headers = {"User-Agent": "Chrome/111.0.5563.111"}
        page_content = requests.get(url) # , headers = headers)
    except requests.exceptions.RequestException: #gledamo primere ko se zgodi kaksna napaka (requestexeptions je samo nek 'objekt' v kateremu so vse izjeme ki se lahko zgodijo ( kot naprimer prazen seznam...))
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Spletna stran trenuto ni dosegljiva")
        return None
        # nadaljujemo s kodo če ni prišlo do napake
    return page_content.text

def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


# Definirajte funkcijo, ki prenese glavno stran in jo shrani v datoteko.


def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    text = download_url_to_string(page)
    save_string_to_file(text, directory, filename)
# save_frontpage(volleyball_frontpage_url, volleyball_directory, frontpage_filename)