# Definice prostředí

Prostředí je definované v .json souboru. Tento soubor obsahuje jeden rootovský objekt se 4 parametry: "stepPenalty", "map", "rewards" a "position". Step penalty označuje pokutu za 1 krok. V atributu "map" je uložena samotná mapa jako pole stringů, kde znak na pozici (i,j) může být "#", pokud je na pozici zeď, " ", pokud je pozice volná a "T" pokud jde o koncový stav. Parametr "rewards" označuje seznam odměn za koncové stavy v pořadí v jakém jsou stavy v mapě uvedeny (řádek má přednost před sloupcem). Poslední attribut "position" označuje startovní pozici robota (kterou však robot nezná).

# Řešení úlohy v jazyce Python

Veškeré řešení pište do třídy Solution.py (případně si můžete vytvořit další pomocné soubory). Ostatní soubory nijak neměňte, jinak vám automatické testy nemusí fungovat. Definici tříd a výčtů, tkeré budeme u úlohy používat naleznete v souboru Environment.py.


## Inicializace

Na začátku programu bude zavolaná metoda init třídy Solution, tedy bude vytvořena její instance, která bude používaná během celého procesu. Tento konstruktor dostane na vstupu popis prostředí, který obsahuje mapu (tedy pozice zdí a koncových stavů spolu s jejich hodnocením) spolu s pokutou (bodovou ztrátou) za každý provedený krok. V tomto konstruktoru si můžete udělat jakékoliv předvýpočty chcete, limit pro běh konstruktoru je 10 sekund.

## Krok

Před provedením každé instrukce se zavolá funkce getInstruction nebo getInstructionGPS (podle toho, kterou variantu úlohy řešíte), které dostanou buďto data ze senzorů nebo přímo pozici robota (x,y souřadnice). Vaším úkolem je určit, která instrukce se má optimálně vykonat a vrátit intrukci, kterou pošleme robotovi k vykonání. Tato funkce se volá stále dokola, dokud robot nedorazí do koncového stavu. 

Pokud chceme, můžeme místo instrukce samotné vrátit Tuple, který jako 1. prvek obsahuje instrukci a jako druhý prvek data pro vizualizaci, pomocí nichž si můžete nastavit barvu pozadí políček a také si do políček něco vepsat. Tato data slouží pro jednodušší debudování a sledování, zda se váš algoritmus chová tak, jak chcete (jak tato data vypadají se můžete podívat v souboru Environment.py).

## Vizualizace

Vizualizace zobrazuje pohyb robota. Tato vizalizace zobrazí mapu, pozici robota po každém kroku instrukci a hodnoty ze senzorů, případně spolu s vašimi daty, která jste zadali.

Ovládání:

- Space: krok vřed
- b: krok zpět
- l/s: zvětšení/zmenšení vykreslené buňky
- a: autorun
- +/-: změna rychlosti autorunu

## Spuštění programu

Program spustíte scriptem main.py, který bere až 3 parametry. První z nich je povinný a jedná se o (relativní/absolutní) cestu k souboru s definicí prostředí. Dále můžete nepovině dát 2 další argumenty a to "novis", který spustí program/simulaci bez vizualizace a pouze vypíše do konzole výsledné skóre a poté argument "gps", který spustí program ve gps formátu (pro řešení jednodušší varianty).


# Řešení v jiném programovacím jazyce

Pokud chcete robota programovat v jiném programovacím jazyce, vytvořte program, který poslouchá na TCP portu 8080. Simulátor se pak k tomuto programu přes port připojí (naváže TCP komunikaci) a začne posílat zprávy, na které bude tvůj program reagovat. Tvůj program musí umět reagovat na 3 zprávy: INIT, STEP a END.

## INIT Message

Tato zpráva je ve formátu 

```
INIT: <env>
```

, kde <env> obsahuje popis prostředí. Proměnná <env> má formát:

```
<stepPenalty>;<mapHeight>;<mapWidth>;<map>
```

kde <stepPenalty> je číslo popisující penalizaci kroku, <mapHeight> a <mapWidth> jsou čísla popisující výšku a šířku mapy a map popisuje mapu ve formátu:

```
a,b,c,e,...,x
```

kde a,b,c,e,x... jsou jednotlivá políčka posaná čísli, přičemž pokud je políčko 0, pak znamená, že je volné, pokud 1, pak je zde zeď a pokud je to číslo začínající na číslici (tedy například 254.32), pak jde o koncový stav s hodnotou za číslící 2 (tedy 54.32).

Tato zráva říká, že začne program na následující mapě a dá vám prostor k předvýpočtům (podobně jako konstruktor v případě řešení v pythonu). Jakmile budete s předvýpočtem hotoví, odpovězte simulátoru zprávou 

```
DONE
```

a simulátor vám začne posílat jendotlivé kroky.

## STEP Message

Jednotlivé kroky (ekvivalent sekce Krok v případě řešení v pythonu) je zpráva ve formátu

```
STEP: u;l;r;d
```

, kde u,l,r,d jsou hodnoty ze senzoru v pořadí UP, LEFT, RIGHT a DOWN, s tím že je číslo rovno 1, pokud je na pozici detekována zeď a 0, pokud není.

Případně

```
STEP: (x,y)
```

kde x a y je pozice robota v případě, že máte zapnutý GPS mód. Odpověď na tuto zprávu je jen jedno číslo od 0 do 3 včetně, které odpovídá instrukci, kterou má robot vykonat, příčemž: 0=UP, 1=LEFT, 2=RIGHT a 3=DOWN.

Pozn. Ukládání vlastní dat do vizualizace není v případě socketové komunikace podporováno.

## END Message

Jakmile robot koncového stavu, nebo donjde v simulátoru k nějaké chybě/timeoutu, dostanete message s textem "END", oznamující, že simulace skončila. Na tuto zprávu nijak nereagujte a ukončete program.


## Spuštění

Z prvé spusťte váš program. Následně spusťte script mainSocket.py, který bere stejný paramtery jako main.py popsaný výše, a který se k vašemu programu automaticky připojí spustí simulaci/vizualizaci.


## Příklad v Javě

Jako příklad jsme, jak takovýto prgram program vytvoři jsme pro vás připravili kostru řešení v Javě, kde je příjmání, parsování a posílání zpráv již vytvořené a jediné, co vám zbývá naimplementovat je třída Solution podobně, jako v případě řešení v pythonu.
