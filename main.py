"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Ivana Kuttlerová
email: janickova.iva@seznam.cz

"""

import sys
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def server_response(url: str) -> BeautifulSoup:
    """Odešle GET request na zadanou URL a vrátí objekt BeautifulSoup."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_town_links(region_url):
    """Získá odkazy na jednotlivé obce z daného územního celku."""
    soup = server_response(region_url)
    town_links = []

    # Procházíme všechny tabulky s daty obcí
    tables = soup.select("table")  # Vybere všechny tabulky na stránce
    for table in tables:
        for row in table.select('tr'):
            code = row.select_one('td:first-child a')
            name = row.select_one('td:nth-child(2)')
            if code and name:
                full_link = urljoin(region_url, code['href'])  # Spojení relativního odkazu s hlavní URL
                town_links.append((code.text.strip(), name.text.strip(), full_link))

    if not town_links:
        print("❌ Chyba: Nebyl nalezen žádný územní celek! Zkontrolujte zadanou URL.")
        sys.exit(1)

    print(f"✅ Načteno {len(town_links)} obcí.")  # Pro kontrolu
    return town_links

def scrape_town_data(town_url):
    """Získá volební data pro konkrétní obec."""
    soup = server_response(town_url)

    def get_value(headers_id):
        """Pomocná funkce pro extrakci hodnoty z buňky podle headers atributu."""
        cell = soup.find("td", {"headers": headers_id})
        return cell.text.strip().replace("\xa0", "") if cell else "0"

    # Počet voličů, vydané obálky a platné hlasy
    voters = get_value("sa2")  # Voliči v seznamu
    envelopes = get_value("sa3")  # Vydané obálky
    valid_votes = get_value("sa6")  # Platné hlasy

    # Seznam názvů stran
    parties = [p.text.strip() for p in soup.select("td.overflow_name")]

    # Hlasy pro jednotlivé strany
    votes_raw = soup.select("td.cislo[headers*=sa2][headers*=sb3]")  
    votes = [int(v.text.strip().replace("\xa0", "").replace(" ", "").replace(",", "")) for v in votes_raw]

    # Ověření, že data sedí
    if len(parties) != len(votes):
        print(f"❌ Chyba: Počet stran ({len(parties)}) a počet hlasů ({len(votes)}) nesedí!")
        sys.exit(1)

    party_votes = dict(zip(parties, votes))
    return voters, envelopes, valid_votes, party_votes

def save_to_csv(filename, data, parties):
    """Uloží data do CSV souboru."""
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Hlavička souboru
        headers = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy'] + parties
        writer.writerow(headers)

        for row in data:
            writer.writerow(row)

    print(f"✅ Výsledky uloženy do {filename}")

def main():
    if len(sys.argv) != 3:
        print("Použití: python main.py <url_územního_celku> <výstupní_soubor.csv>")
        sys.exit(1)

    region_url = sys.argv[1]
    output_file = sys.argv[2]

    try:
        towns = get_town_links(region_url)
        all_data = []
        all_parties = set()
        town_data = {}

        for code, name, link in towns:
            voters, envelopes, valid_votes, party_votes = scrape_town_data(link)
            all_parties.update(party_votes.keys())
            town_data[code] = [code, name, voters, envelopes, valid_votes, party_votes]

        sorted_parties = list(next(iter(town_data.values()))[5].keys())  # Pořadí stran podle první obce
        for code, (code, name, voters, envelopes, valid_votes, party_votes) in town_data.items():
            row = [code, name, voters, envelopes, valid_votes] + [party_votes.get(party, '0') for party in sorted_parties]
            all_data.append(row)

        save_to_csv(output_file, all_data, sorted_parties)

    except Exception as e:
        print(f"❌ Chyba: {e}")

if __name__ == '__main__':
    main()
