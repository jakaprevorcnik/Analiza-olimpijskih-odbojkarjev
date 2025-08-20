import csv
import os
import requests
import re

#--------------------------------Defining constants--------------------------------

# definirajte URL glavne strani bolhe za oglase z mačkami
volleyball_frontpage_url = 'https://en.wikipedia.org/wiki/List_of_Olympic_medalists_in_volleyball'
# mapa, v katero bomo shranili podatke
volleyball_directory = '/home/user/Fmf/UVP/projektna/Analiza-odbojkarjev-1'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'statistika.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'statistika.csv'

#--------------------------------Scraping files--------------------------------

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

#----------------------------------------Reading files-----------------------------------------------------

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz."""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding = "utf-8") as file_in:
        text = file_in.read()
    return text

def extract_mens_indoor_volleyball_medalists(html_content):
    """Function extracts men's indoor volleyball Olympic medalists from HTML content.
    Returns a list where each element represents one Olympic year with all medalists and their medals."""
    
    # Find the start of the men's indoor volleyball section
    men_section_start = html_content.find('<h3 id="Men">Men</h3>')
    if men_section_start == -1:
        print("Men's section not found in HTML")
        return []
    
    # Find the table that contains the medalists data
    table_start = html_content.find('<table class="wikitable plainrowheaders"', men_section_start)
    if table_start == -1:
        print("Medalists table not found")
        return []
    
    # Find the end of the table
    table_end = html_content.find('</table>', table_start)
    if table_end == -1:
        print("End of table not found")
        return []
    
    table_html = html_content[table_start:table_end + 8]  # +8 for '</table>'
    
    # Extract all table rows (excluding the header)
    rows_pattern = r'<tr valign="top">(.*?)</tr>'
    rows = re.findall(rows_pattern, table_html, re.DOTALL)
    
    medalists_by_year = []
    
    for row in rows:
        # Extract the Olympic year and location
        year_pattern = r'<td><a href=".*?".*?>(.*?)</a>'
        year_match = re.search(year_pattern, row)
        if not year_match:
            continue
            
        olympic_year = year_match.group(1)
        
        # Extract the three medal columns (Gold, Silver, Bronze)
        medal_columns = re.findall(r'<td valign="top">(.*?)</td>', row, re.DOTALL)
        
        if len(medal_columns) >= 3:
            year_data = {
                'year': olympic_year,
                'gold': extract_medalists_from_column(medal_columns[0]),
                'silver': extract_medalists_from_column(medal_columns[1]), 
                'bronze': extract_medalists_from_column(medal_columns[2])
            }
            medalists_by_year.append(year_data)
    
    return medalists_by_year


def extract_medalists_from_column(column_html):
    """Extract country and player names from a medal column."""
    
    # Extract country name and code
    country_pattern = r'<a href=".*?".*?>(.*?)</a>.*?\((.*?)\)'
    country_match = re.search(country_pattern, column_html)
    
    if not country_match:
        return {'country': 'Unknown', 'code': 'UNK', 'players': []}
    
    country = country_match.group(1)
    country_code = country_match.group(2)
    
    # Extract all player names (they appear as links after the country info)
    # Players are listed as <a href="...">Player Name</a><br />
    player_pattern = r'<a href="/wiki/.*?".*?>(.*?)</a>'
    players = re.findall(player_pattern, column_html)
    
    # Remove the country from the players list (first match is usually the country link)
    if players and players[0] == country:
        players = players[1:]
    
    # Clean up player names - remove any HTML entities and extra text
    cleaned_players = []
    for player in players:
        # Remove parenthetical information like "(c)" for captain
        clean_name = re.sub(r'\s*\([^)]*\)', '', player)
        if clean_name and clean_name not in cleaned_players:
            cleaned_players.append(clean_name.strip())
    
    return {
        'country': country,
        'code': country_code, 
        'players': cleaned_players
    }


def mens_volleyball_data_from_file(filename, directory):
    """Function reads HTML file and extracts men's indoor volleyball Olympic medalists data.
    Returns a list of dictionaries, one for each Olympic year."""
    
    html_content = read_file_to_string(directory, filename)
    return extract_mens_indoor_volleyball_medalists(html_content)

#----------------------------------------Saving files in csv--------------------------------

def write_volleyball_data_to_csv(data, directory, filename):
    """Write volleyball medalists data to CSV file in a format ready for analysis.
    Each row represents one player with their Olympic year, medal, country, and name."""
    
    os.makedirs(directory, exist_ok=True) # V primeru, da mapa ze obstaja, jo ne bomo ponovno ustvarili
    path = os.path.join(directory, filename)
    
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['olympic_year', 'medal_type', 'country', 'country_code', 'player_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Process each Olympic year
        for year_data in data:
            olympic_year = year_data['year']
            
            # Process each medal type (gold, silver, bronze)
            for medal_type in ['gold', 'silver', 'bronze']:
                medal_data = year_data[medal_type]
                country = medal_data['country']
                country_code = medal_data['code']
                
                # Write a row for each player
                for player_name in medal_data['players']:
                    writer.writerow({
                        'olympic_year': olympic_year,
                        'medal_type': medal_type,
                        'country': country,
                        'country_code': country_code,
                        'player_name': player_name
                    })
    
    print(f"Data successfully written to {path}")
    total_players = sum(len(year_data['gold']['players']) + len(year_data['silver']['players']) + len(year_data['bronze']['players']) for year_data in data)
    print(f"Total players written: {total_players}")


#---------------------------------------Main function--------------------------------

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