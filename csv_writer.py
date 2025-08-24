import os
import csv


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
