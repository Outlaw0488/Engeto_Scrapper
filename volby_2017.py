import csv
import re
import bs4
import requests
import sys

def vysledky_voleb():
    """zadej odkaz okresu a nazev CSV souboru včetně .csv a funkce vygeneruje vysledky v jednotlivych obcich v ramci okresu"""
    # hlavni funkce, ktera spousti dalsi funkce
    link = str(sys.argv[1])
    nazev_souboru = str(sys.argv[2])
    slovnik = vytvor_odkazy_obci(link) #vytvori slovnik s kody a linky na jednotlive obce
    data = data_obci(slovnik) #posbira data jednotlivych obci
    csv_zapis(data, nazev_souboru) #data nasledne zapise do CSV souboru

def vytvor_odkazy_obci(link: str):
    """vytvori slovnik se vsemi kody obci a odkazy na jejich vysledky"""
    # kody obci nejsou totiz na vysledce strance obce a k tomu napoji odkaz na stranku obce
    linky_obci = dict()
    html_okres = requests.get(link)
    soup_okres = bs4.BeautifulSoup(html_okres.text, "html.parser")
    try:
      nazev_okresu = soup_okres.find(string=re.compile("Okres: ")).strip("\n").split(": ")[1]
    except:
      nazev_okresu = soup_okres.find(string=re.compile("Kraj: ")).strip("\n").split(": ")[1]
    obec_odkaz = soup_okres.find_all("td", {"class" : "cislo"})
    linky_obci.update({a_elem.a.get_text():"https://volby.cz/pls/ps2017nss/"+a_elem.a["href"] for a_elem in obec_odkaz})
    print(f"Prohlížím jednotlivé obce pro okres - {nazev_okresu}")
    return linky_obci

def data_obci(slovnik_obci: dict):
    """ prochází stránku s daty o volbach dane obce a rovnou připravuje listy a slovníky pro zapisování dat do CSV"""
    strany = ['Občanská demokratická strana', 'Řád národa - Vlastenecká unie', 'CESTA ODPOVĚDNÉ SPOLEČNOSTI', 'Česká str.sociálně demokrat.','Volte Pr.Blok www.cibulka.net',
          'Radostné Česko', 'STAROSTOVÉ A NEZÁVISLÍ', 'Komunistická str.Čech a Moravy', 'Strana zelených',
          'ROZUMNÍ-stop migraci,diktát.EU','Společ.proti výst.v Prok.údolí', 'Strana svobodných občanů', 'Blok proti islam.-Obran.domova',
          'Občanská demokratická aliance', 'Česká pirátská strana', 'OBČANÉ 2011-SPRAVEDL. PRO LIDI', 'Unie H.A.V.E.L.', 'Referendum o Evropské unii', 'TOP 09', 'ANO 2011',
          'Dobrá volba 2016', 'SPR-Republ.str.Čsl. M.Sládka', 'Křesť.demokr.unie-Čs.str.lid.',
          'Česká strana národně sociální', 'REALISTÉ', 'SPORTOVCI', 'Dělnic.str.sociální spravedl.',
          'Svob.a př.dem.-T.Okamura (SPD)', 'Strana Práv Občanů']
    list_dat = []
    for kod, link in slovnik_obci.items():
        html_obec = requests.get(link)
        soup_obec = bs4.BeautifulSoup(html_obec.text, "html.parser")
        dict_obsahu = dict()
        dict_obsahu["kód obce"] = kod
        # najdu string nazev obce a musim ocistit o prvky okolo a oddelit od dvojtecky
        dict_obsahu["název obce"] = soup_obec.find(string=re.compile("Obec: ")).strip("\n").split(": ")[1]
        # prochazim postupne tabulku a vkladam udaje do slovniku
        dict_obsahu["voliči v seznamu"] = soup_obec.find("td", {"class": "cislo", "headers": "sa2"}).text
        dict_obsahu["vydané obálky"] = soup_obec.find("td", {"class": "cislo", "headers": "sa3"}).text
        dict_obsahu["platné hlasy"] = soup_obec.find("td", {"class": "cislo", "headers": "sa6"}).text
        # najdu jméno strany a pro každou skočím 2 místa dál a získám počet hlasů. asi složitějš, ale aspoň najdu počty přesně ke každé straně
        for strana in strany:
          try:
            dict_obsahu[strana] = soup_obec.find("td", string=re.compile(strana[:20])).next_sibling.next_sibling.text
          except: #pokud nenajde danou stranu na webove strance obce, tak dej prazdnou bunku s pocty hlasu
            dict_obsahu[strana] = " "
        # slovnik s daty kazde obce nahraju postupne do listu, aby to pak zpracovala whiterows funkce
        list_dat.append(dict_obsahu)
    print("Data obcí zapsána")
    return list_dat

def csv_zapis(obsah:list, nazev_souboru):
    """zapisovani dat do CSV"""
    header = ['kód obce', 'název obce', 'voliči v seznamu', 'vydané obálky', 'platné hlasy', 'Občanská demokratická strana',
              'Řád národa - Vlastenecká unie', 'CESTA ODPOVĚDNÉ SPOLEČNOSTI', 'Česká str.sociálně demokrat.',
              'Radostné Česko', 'STAROSTOVÉ A NEZÁVISLÍ', 'Komunistická str.Čech a Moravy', 'Strana zelených',
              'ROZUMNÍ-stop migraci,diktát.EU', 'Strana svobodných občanů', 'Blok proti islam.-Obran.domova',
              'Občanská demokratická aliance', 'Česká pirátská strana', 'Referendum o Evropské unii', 'TOP 09', 'ANO 2011',
              'Dobrá volba 2016', 'SPR-Republ.str.Čsl. M.Sládka', 'Křesť.demokr.unie-Čs.str.lid.',
              'Česká strana národně sociální', 'REALISTÉ', 'SPORTOVCI', 'Dělnic.str.sociální spravedl.',
              'Svob.a př.dem.-T.Okamura (SPD)', 'Strana Práv Občanů']
    with open(nazev_souboru, mode ="w") as f:
      f_writer = csv.DictWriter(f, header)
      f_writer.writeheader()
      f_writer.writerows(obsah)
    f.close()
    print(f"soubor {nazev_souboru} vytvořen a uložen")

if __name__ == "__main__":
    vysledky_voleb()
