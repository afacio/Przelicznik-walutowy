import xml.etree.ElementTree  as  ET
import requests

class Waluta():
    def __init__(self, nazwa_waluty):
        self.nazwa_waluty = nazwa_waluty
        self.przelicznik = None
        self.kod_waluty = None
        self.kurs_sredni = None

    def print_currency_code(self):
        print(self.kod_waluty, end=', ')

    def print_all(self):
        print("\n=================================")
        print("nazwa waluty: ", self.nazwa_waluty, "\nkod_waluty: ", self.kod_waluty, "\nprzelicznik: ", self.przelicznik, "\nkurs_sredni: ", self.kurs_sredni)

class ZbiorWalut():
    def __init__(self):
        self.zbior = list()

    def download_file(self):
        try:
            url = 'https://www.nbp.pl/kursy/xml/lasta.xml'
            r = requests.get(url, allow_redirects=True)
            open('lasta.xml', 'wb').write(r.content)
        except requests.ConnectionError:
            print("brak polaczenia z internetem")
            exit(1)

    def czytajPlik(self, zbior):
        file = r"lasta.xml"

        tree = ET.parse(file)
        root = tree.getroot()

        for linia in root.iterfind("pozycja"):
            nazwa_waluty = linia.findtext("nazwa_waluty")
            waluta = Waluta(nazwa_waluty)
            waluta.kod_waluty = linia.findtext("kod_waluty")
            przelicznik = linia.findtext("przelicznik")
            kurs_sredni = linia.findtext("kurs_sredni")
            waluta.przelicznik = string_to_float(przelicznik)
            waluta.kurs_sredni = string_to_float(kurs_sredni)
            zbior.append(waluta)

    def wybor(self):
        while (True):
            var1 = input("\nWpisz kod waluty jakiej chcesz użyć: ")
            var2 = 0

            for waluta in self.zbior:
                if var1 == waluta.kod_waluty:
                    print("Wybrales walute: ", waluta.nazwa_waluty)
                    return waluta
                else:
                    var2 += 1
                if var2 == len(self.zbior):
                    print("brak podanego kodu waluty, sprobuj ponownie", end='')
                    continue
    def wyswietl_kod_waluty(self, zbior):
        for waluta in zbior:
            waluta.print_currency_code()
    def wyswietl_wszystko(self, zbior):
        for waluta in zbior:
            waluta.print_all()

def przelicznik(var1, var2):
    proba = True
    while(proba):
        suma_string = input("\nPodaj sumę pieniędzy ktora chcesz przeliczyć z waluty {0} na {1}: ".format(var1.kod_waluty, var2.kod_waluty))
        try:
            suma_float = float(suma_string)
            print(suma_float)
            PLN = suma_float * var1.przelicznik * var1.kurs_sredni
            suma_koncowa = PLN * var2.przelicznik / var2.kurs_sredni
            print(round(suma_koncowa, 4))
            proba = False
        except ValueError:
            print("Wprowadz wartosc typu float")

def string_to_float(string):
    return round(float(zmiana_przecinka(string)),4)

def list_to_string(list):
    str = ""
    for element in list:
        str += element
    return str

def zmiana_przecinka(str):
    str_list = list(str)
    for i in range(len(str_list)):
        if str_list[i] == ',':
            str_list[i] = '.'
    string = list_to_string(str_list)
    return string

def main():
    zbior = ZbiorWalut()
    zbior.download_file()
    zbior.czytajPlik(zbior.zbior)

    program = True
    MENU = "\nWybierz akcje:\n1: Podglad kursu walut\n2: Wymiana walutowa\n3: Koniec programu\n"
    while (program):
        wybor = input(MENU)
        if wybor == '1':
            zbior.wyswietl_wszystko(zbior.zbior)
        elif wybor == '2':
            zbior.wyswietl_kod_waluty(zbior.zbior)
            waluta1 = zbior.wybor()
            waluta2 = zbior.wybor()
            przelicznik(waluta1, waluta2)
        elif wybor == '3':
            program = False
        else:
            print("Wprowadziles zly znak")

main()
