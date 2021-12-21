# Engeto_Scrapper
Tento projekt extrahuje ze zvoleného odkazu voleb v okresu vysledky za jednotlivé obce v daném okresu a uloží do CSV souboru.
Jdi na tento odkaz: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ a klikni na křížek v poli "výběr obce".
Odkaz v horní liště prohlížeče pak použiješ jako argument pro spuštění projektu

### Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru **requirements.txt**. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

$ pip3 --version #overim verzi manažeru

$ pip3 install -r requirements.txt #nainstalujeme knihovny

### Spuštění projektu
Spustím soubor **volby_2017.py** v příkazovém řádku a zadám 2 povinné argumenty
1. odkaz na zvolenou obec
2. název CSV souboru, který chceme vytvořit včetně koncovky .csv

### Ukázka projektu
Pro Prostějov bude text příkazovém řádku vypadat takto:

python vysledky_voleb_obce_2017.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv

Projekt oznámí z jakého okresu stahuje data, v našem příkladu:

"Prohlížím jednotlivé obce pro okres - Prostějov"


Po stáhnutí dat za jednotlivé obce oznámí:

"Data obcí zapsána"

Nakonec informuje o vytvoří .csv souboru, včetně názvu souboru:

"soubor vysledky_prostejov.csv vytvořen a uložen"

Zde je ukázka částečného výstupu z .csv souboru:

kód obce,název obce,voliči v seznamu,vydané obálky,platné hlasy,Občanská demokratická strana, .......
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,29,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,51,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,Bílovice-Lutotín,431,279,275,13,0,0,32,0,8,40,1,0,4,0,13,30,0,3,83,0,0,22,0,0,0,1,38,0



