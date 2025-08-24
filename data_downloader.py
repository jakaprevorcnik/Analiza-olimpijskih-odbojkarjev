import os
import requests
from config import volleyball_frontpage_url, volleyball_directory, frontpage_filename


def download_url_to_string(url):

    """Funkcija prenese vsebino spletne strani na naslovu "url" in vrne vsebino kot niz."""
    try: 
        page_content = requests.get(url)
    except requests.exceptions.RequestException: 
        print("Spletna stran trenuto ni dosegljiva")
        return None
    return page_content.text

def save_string_to_file(text, directory, filename):
    """Funkcija shrani niz "text" v datoteko "directory"/"filename"."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


def save_frontpage(page, directory, filename):
    """Funkcija shrani glavno stran odbojkarjev v datoteko."""
    text = download_url_to_string(page)
    save_string_to_file(text, directory, filename)
