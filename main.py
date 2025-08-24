import os
from config import (volleyball_directory,
                    frontpage_filename,
                    csv_filename,
                    volleyball_frontpage_url)

from data_downloader import save_frontpage
from data_parser import mens_volleyball_data_from_file  
from csv_writer import write_volleyball_data_to_csv


def main(redownload=True, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Podatke prenese iz wikipedije
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """
    #Shranimo stran v html datoteko
    path = os.path.join(volleyball_directory, frontpage_filename)
    if redownload or not os.path.exists(path):
        save_frontpage(volleyball_frontpage_url, volleyball_directory, frontpage_filename)
    else:
        print('Datoteka html ze obstaja')
    
    # Podatke preberemo v lepšo obliko (seznam slovarjev)
    if reparse or not os.path.exists(path):
        data = mens_volleyball_data_from_file(frontpage_filename, volleyball_directory)
        print(f"Extracted data for {len(data)} Olympic years")
        
        # Podatke shranimo v csv datoteko
        write_volleyball_data_to_csv(data, volleyball_directory, csv_filename)
    else:
        print('Datoteka html ze obstaja')



if __name__ == '__main__':
    main(False, True)