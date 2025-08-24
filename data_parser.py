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
