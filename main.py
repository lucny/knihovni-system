import csv
from tabulate import tabulate
import os

class KnihovniSystem:
    def __init__(self, soubor):
        self.soubor = soubor
        self.knihy = self.nacti_knihy()
        
    def nacti_knihy(self):
        try:
            with open(self.soubor, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            print(f"Soubor {self.soubor} nebyl nalezen.")
            return []

    def uloz_knihy(self):
        if self.knihy:
            fieldnames = self.knihy[0].keys()
            with open(self.soubor, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.knihy)

    def zobraz_knihy(self):
        if not self.knihy:
            print("Žádné knihy k zobrazení.")
            return
        
        headers = {
            'isbn': 'ISBN',
            'nazev_knihy': 'Název knihy',
            'autor': 'Autor',
            'rok_vydani': 'Rok vydání',
            'nakladatelstvi': 'Nakladatelství',
            'zanr': 'Žánr',
            'pocet_stran': 'Počet stran',
            'cena': 'Cena'
        }
        
        table_data = [[kniha[key] for key in headers.keys()] for kniha in self.knihy]
        print(tabulate(table_data, headers=headers.values(), tablefmt='grid'))

    def filtruj_knihy(self):
        print("\n=== FILTRACE KNIH ===")
        print("1. Podle žánru")
        print("2. Podle počtu stran")
        print("3. Podle roku vydání")
        volba = input("Vyberte možnost filtrace (1-3): ")

        if volba == '1':
            zanr = input("Zadejte žánr: ")
            filtrovane = [k for k in self.knihy if k['zanr'].lower() == zanr.lower()]
        elif volba == '2':
            try:
                min_strany = int(input("Zadejte minimální počet stran: "))
                max_strany = int(input("Zadejte maximální počet stran: "))
                filtrovane = [k for k in self.knihy if min_strany <= int(k['pocet_stran']) <= max_strany]
            except ValueError:
                print("Neplatný vstup!")
                return
        elif volba == '3':
            try:
                rok = int(input("Zadejte rok vydání: "))
                filtrovane = [k for k in self.knihy if int(k['rok_vydani']) == rok]
            except ValueError:
                print("Neplatný vstup!")
                return
        else:
            print("Neplatná volba!")
            return

        if filtrovane:
            headers = self.knihy[0].keys()
            print(tabulate(filtrovane, headers='keys', tablefmt='grid'))
        else:
            print("Nebyly nalezeny žádné knihy odpovídající filtru.")

    def pridej_knihu(self):
        print("\n=== PŘIDÁNÍ NOVÉ KNIHY ===")
        nova_kniha = {
            'isbn': input("ISBN: "),
            'nazev_knihy': input("Název knihy: "),
            'autor': input("Autor: "),
            'rok_vydani': input("Rok vydání: "),
            'nakladatelstvi': input("Nakladatelství: "),
            'zanr': input("Žánr: "),
            'pocet_stran': input("Počet stran: "),
            'cena': input("Cena: ")
        }
        self.knihy.append(nova_kniha)
        self.uloz_knihy()
        print("Kniha byla úspěšně přidána.")

    def uprav_knihu(self):
        self.zobraz_knihy()
        isbn = input("\nZadejte ISBN knihy k úpravě: ")
        
        for kniha in self.knihy:
            if kniha['isbn'] == isbn:
                print(f"\nÚprava knihy: {kniha['nazev_knihy']}")
                for klic, hodnota in kniha.items():
                    nova_hodnota = input(f"Zadejte novou hodnotu pro {klic} (nebo Enter pro ponechání současné hodnoty \"{hodnota}\"): ")
                    if nova_hodnota:
                        kniha[klic] = nova_hodnota
                self.uloz_knihy()
                print("Kniha byla úspěšně upravena.")
                return
        print("Kniha s tímto ISBN nebyla nalezena.")

    def smaz_knihu(self):
        self.zobraz_knihy()
        isbn = input("\nZadejte ISBN knihy ke smazání: ")
        
        for i, kniha in enumerate(self.knihy):
            if kniha['isbn'] == isbn:
                del self.knihy[i]
                self.uloz_knihy()
                print("Kniha byla úspěšně smazána.")
                return
        print("Kniha s tímto ISBN nebyla nalezena.")

def hlavni_menu():
    system = KnihovniSystem('knihy.csv')
    
    while True:
        print("\n=== SPRÁVA KNIHOVNY ===")
        print("1. Zobrazit všechny knihy")
        print("2. Filtrovat knihy")
        print("3. Přidat novou knihu")
        print("4. Upravit knihu")
        print("5. Smazat knihu")
        print("6. Konec")
        
        volba = input("\nVyberte možnost (1-6): ")
        
        if volba == '1':
            system.zobraz_knihy()
        elif volba == '2':
            system.filtruj_knihy()
        elif volba == '3':
            system.pridej_knihu()
        elif volba == '4':
            system.uprav_knihu()
        elif volba == '5':
            system.smaz_knihu()
        elif volba == '6':
            print("Program ukončen.")
            break
        else:
            print("Neplatná volba!")

if __name__ == "__main__":
    hlavni_menu()
