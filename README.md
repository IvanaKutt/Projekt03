#  Elections Scraper - Výsledky voleb 2017

Tento Python skript **scrapuje výsledky voleb do Poslanecké sněmovny ČR z roku 2017** pro **vybraný územní celek**  a ukládá je do CSV souboru.

## Funkce

✅ Stahuje odkazy na jednotlivé obce ve vybraném územním celku.
✅ Načítá počet voličů, vydané obálky, platné hlasy a výsledky politických stran za jednotlivé obce.
✅ Ukládá výsledky do CSV ve správném pořadí stran.
,

## Instalace

Projekt je napsán v Pythonu 3.13.2

1. Vytvořte si nové virtuální prostředí (doporučeno):
   ```
   python -m venv venv
   ```
2. Aktivujte virtuální prostředí:
   - **Windows:**
     ```
     venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```
     source venv/bin/activate
     ```
3. Nainstalujte potřebné knihovny ze souboru `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```


## Spuštění

Skript vyžaduje dva argumenty:

1. **URL územního celku** — odkaz na stránku se seznamem obcí naleznete zde: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ, pomocí odkazů ve sloupci Výběr okrsku, tedy sloupec se symbolem X.

2. **Název výstupního souboru** — soubor, kam se uloží výsledky ve formátu CSV (př. vysledky_olomouc.csv)

Příklad spuštění:
```
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102" vysledky_olomouc.csv
```

## Výstup

Výstupní CSV soubor obsahuje následující sloupce:

- **Kód obce**
- **Název obce**
- **Voliči v seznamu**
- **Vydané obálky**
- **Platné hlasy**
- **Kandidující strany** (každá strana má svůj vlastní sloupec s počtem hlasů)

Ukázka výstupu:
```
Kód obce;Název obce;Voliči v seznamu;Vydané obálky;Platné hlasy;Občanská demokratická strana;Řád národa - 
552356;Babice;370;256;254;13;0;0;10;
500526;Bělkovice-Lašťany;1 801;1 079;1 069;97;0;0;83;
500623;Bílá Lhota;931;568;565;31;0;0;42;
552062;Bílsko;172;119;119;8;0;1;11;
500801;Blatec;497;320;319;21;0;0;28;
```

## Ukázka výstupu v terminálu

✅ Načteno 97 obcí.
✅ Výsledky uloženy do vysledky_olomouc.csv


## Chyby

Pokud se během běhu skriptu objeví chyba (např. špatná URL nebo neexistující stránka), program vypíše odpovídající chybovou zprávu.

Skript také upozorní uživatele, pokud nejsou zadány oba argumenty, program zobrazí chybovou zprávu.


## Struktura projektu

📂 Projekt03/
 ├── 📄 main.py          # Hlavní skript
 ├── 📄 README.md        # Dokumentace
 ├── 📄 requirements.txt # Seznam knihoven



## Autor

Ivana Kuttlerová