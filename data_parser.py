import os
import re
from config import volleyball_directory, frontpage_filename


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz."""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding = "utf-8") as file_in:
        text = file_in.read()
    return text

def extract_mens_indoor_volleyball_medalists(html_content):
    """Funkcija izvozi moške odbojkarje, ki so osvojili medalje na olimpijskih igrah."""
    
    # Poiscemo zacetek moskih odbojkarjev
    men_section_start = html_content.find('<h3 id="Men">Men</h3>')
    if men_section_start == -1:
        print("Men's section not found in HTML")
        return []
    
    # Poiscemo zacetek podatkov o medaljah
    table_start = html_content.find('<table class="wikitable plainrowheaders"', men_section_start)
    if table_start == -1:
        print("Medalists table not found")
        return []
    
    # posicemo konec tabele
    table_end = html_content.find('</table>', table_start)
    if table_end == -1:
        print("End of table not found")
        return []
    
    table_html = html_content[table_start:table_end + 8]  # +8 za '</table>'
    
    # izvozimo vse vrstice tabele (razen glave)
    rows_pattern = r'<tr valign="top">(.*?)</tr>'
    rows = re.findall(rows_pattern, table_html, re.DOTALL)
    
    medalists_by_year = []
    
    for row in rows:
        # izvozimo olimpijsko leto in lokacijo
        year_pattern = r'<td><a href=".*?".*?>(.*?)</a>'
        year_match = re.search(year_pattern, row)
        if not year_match:
            continue
            
        olympic_year = year_match.group(1)
        
       
        medal_columns = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        
        if len(medal_columns) >= 4:  # potrebujemo vsaj 4: leto + 3 medalje
            year_data = {
                'year': olympic_year,
                'gold': extract_medalists_from_column(medal_columns[1]),    
                'silver': extract_medalists_from_column(medal_columns[2]),  
                'bronze': extract_medalists_from_column(medal_columns[3])   
            }
            medalists_by_year.append(year_data)
    
    return medalists_by_year


def extract_medalists_from_column(column_html):
    """Funkcija iz stolpca tabele izlušči podatke o državi in igralcih, ki so osvojili določeno medaljo."""
    
    # ime drzave in kratica
    country_pattern = r'<a href=".*?".*?>(.*?)</a>.*?\((.*?)\)'
    country_match = re.search(country_pattern, column_html)
    
    if not country_match:
        return {'country': 'Unknown', 'code': 'UNK', 'players': []}
    
    country = country_match.group(1)
    country_code = country_match.group(2)
    
    # Igralci so navedeni kot <a href="...">Player Name</a><br />
    player_pattern = r'<a href="/wiki/.*?".*?>(.*?)</a>'
    players = re.findall(player_pattern, column_html)
    
    # Odstranimo linke do drzav
    if players and players[0] == country:
        players = players[1:]
    
    # uredimo imena igralcev
    cleaned_players = []
    for player in players:
        # Odstranimo dodatne informacije v oklepajih, npr. (c) za kapetana
        clean_name = re.sub(r'\s*\([^)]*\)', '', player)
        clean_name = clean_name.strip()
        
        # Dodamo samo, ce ime ni prazno in ni ze na seznamu
        if clean_name and len(clean_name) > 1 and clean_name not in cleaned_players:
            cleaned_players.append(clean_name)
    
    return {
        'country': country,
        'code': country_code, 
        'players': cleaned_players
    }


def mens_volleyball_data_from_file(filename, directory):
    """Funkcija prebere lokalno html datoteko in izlušči podatke o moških odbojkarjih,
      ki so osvojili medalje na olimpijskih igrah."""
    
    html_content = read_file_to_string(directory, filename)
    return extract_mens_indoor_volleyball_medalists(html_content)
