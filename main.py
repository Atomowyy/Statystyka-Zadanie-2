from decimal import Decimal
from random import randint
import matplotlib.pyplot as plt
from math import sqrt
from scipy.stats import t


def read_files():
    global populacja_1, populacja_2
    populacja_1 = []
    populacja_2 = []
    file = open("3.csv", "r")
    lines = file.readlines()
    for i in lines:
        i = i.replace("\n", "")
        a = i.split(",")
        populacja_1.append(change_notation(a[0]))
        populacja_2.append(change_notation(a[1]))
    file.close()


def change_notation(string):
        string=string.split("e")
        string = Decimal(string[0])*pow(10,Decimal(string[1]))
        return string


#zastosowałem wybór losowy, jeśli program wylosuje 1 to liczba jest brana do próby, jeśli 0 to pomijana
def probe_selection(populacja):
    tab=[]
    for i in populacja:
        selection = randint(0,1)
        if selection==1:
            tab.append(i)
    return tab


def histogram(proba, tytul):
    plt.hist(proba, bins=26, color='blue', edgecolor='black')
    plt.xlabel('Wartości')
    plt.ylabel('Częstość')
    plt.title(tytul)
    plt.show()


def wskazniki_polozenia_rozproszenia(dane, nr_proby, nr_populacji):
    srednia = srednia_arytmetyczna(dane)
    print(f"Średnia arytmetyczna próby {nr_proby} populacji {nr_populacji}:", srednia)
    me = mediana(dane)
    print(f"Mediana próby {nr_proby} populacji {nr_populacji}:",me)
    mo = moda(dane)
    print(f"Moda próby {nr_proby} populacji {nr_populacji}:",mo)
    rozstep = rozstep_proby(dane)
    print(f"Rozstęp próby {nr_proby} populacji {nr_populacji}:", rozstep)
    s2 = wariancja(dane, srednia)
    print(f"Wariancja próby {nr_proby} populacji {nr_populacji}:", s2)
    s = odchylenie_standardowe(s2)
    print(f"Odchylenie standardowe próby {nr_proby} populacji {nr_populacji}:", s)
    q1 = kwantyl_dolny(dane, me)
    print(f"Kwantyl dolny próby {nr_proby} populacji {nr_populacji}:", q1)
    q3 = kwantyl_gorny(dane, me)
    print(f"Kwantyl górny próby {nr_proby} populacji {nr_populacji}:", q3)
    IQR = rozstep_miedzykwartylowy(q1, q3)
    print(f"Rozstęp międzykwartylowy próby {nr_proby} populacji {nr_populacji}:", IQR)


def srednia_arytmetyczna(dane):
    N = len(dane)
    suma = Decimal(0)
    for i in dane:
        suma+=Decimal(i)
    srednia = Decimal(suma/N)
    return srednia


def mediana(dane):
    dane.sort(key=Decimal)
    n=len(dane)
    if len(dane)%2==0:
        me=Decimal((dane[int(n/2)]+dane[int((n/2)+1)])/2)
    else:
        me=Decimal(dane[int((n+1)/2)])
    return me


def moda(dane):
    dane.sort(key=Decimal)
    N = len(dane)
    mo = max(set(dane), key=dane.count)
    if(mo==dane[0] or (mo==dane[N-1])):
        return "brak mody"
    else:
        return mo


def rozstep_proby(dane):
    dane.sort(key=Decimal)
    N = len(dane)
    rozstep = Decimal(dane[N-1] - dane[0])
    return rozstep


def wariancja(dane, srednia):
    s2 = Decimal(0)
    N = len(dane)
    for i in dane:
        roznica = Decimal(dane[int(i)]-srednia)
        kwadrat = Decimal(pow(roznica, 2))
        s2+=kwadrat
    wynik = Decimal(s2/N)
    return wynik


def odchylenie_standardowe(s2):
    s = Decimal(sqrt(s2))
    return s


def kwantyl_gorny(dane, me):
    dane.sort(key=Decimal)
    tab = []
    for i in dane:
        if i > me:
            tab.append(i)
    q3 = mediana(tab)
    return q3


def kwantyl_dolny(dane, me):
    dane.sort(key=Decimal)
    tab = []
    for i in dane:
        if i < me:
            tab.append(i)
    q1 = mediana(tab)
    return q1


def rozstep_miedzykwartylowy(q1, q3):
    IQR = Decimal(q3-q1)
    return IQR


def wartosci_krytyczne(stopnie_swobody, alfa, test_obustronny):
    if test_obustronny == True:
        alfa = alfa/2
    wartosc = t.ppf(1-alfa,stopnie_swobody)
    return wartosc

#Do testowania hipotez używam testu t-studenta
def hipoteza_ab(x, proba, alfa):
    srednia = srednia_arytmetyczna(proba)
    n = len(proba)
    s = odchylenie_standardowe(wariancja(proba, srednia))
    test = Decimal(((srednia-Decimal(x))/s)*Decimal(sqrt(n)))
    wartosc_bezwzgledna_testu = Decimal(abs(test))
    stopnie_swobody=n-1
    wartosc_kryt = wartosci_krytyczne(stopnie_swobody, alfa, True)
    print(f"Wartość bezwzględna testu: {wartosc_bezwzgledna_testu}")
    print(f"Wartość krytyczna: {Decimal(wartosc_kryt)}")
    if Decimal(wartosc_bezwzgledna_testu)>Decimal(wartosc_kryt):
        print("Odrzucamy H0")
    elif Decimal(wartosc_bezwzgledna_testu)<Decimal(wartosc_kryt):
        print("Przyjmujemy H0")

#wzory na test i stopnie_swobody znalezione na wikipedii
def hipoteza_c(x, proba1, proba2, alfa):
    srednia1 = srednia_arytmetyczna(proba1)
    srednia2 = srednia_arytmetyczna(proba2)
    w1 = wariancja(proba1, srednia1)
    w2 = wariancja(proba2, srednia2)
    n1 = len(proba1)
    n2 = len(proba2)
    test = Decimal(((srednia1-srednia2)/Decimal(sqrt((n1*w1)+(n2*w2))))*Decimal(sqrt(((n1*n2)/(n1+n2))*(n1+n2-2))))
    stopnie_swobody = (n1+n2-2)
    wartosc_kryt = wartosci_krytyczne(stopnie_swobody, alfa, True)
    wartosc_bezwzgledna_testu = Decimal(abs(test))
    print(f"Wartość bezwzględna testu: {wartosc_bezwzgledna_testu}")
    print(f"Wartość krytyczna: {Decimal(wartosc_kryt)}")
    if Decimal(wartosc_bezwzgledna_testu)>Decimal(wartosc_kryt):
        print("Odrzucamy H0")
    elif Decimal(wartosc_bezwzgledna_testu)<Decimal(wartosc_kryt):
        print("Przyjmujemy H0")

read_files()

#próba 2_1 oznacza że jest to próba pierwsza z drugiej populacji
proba_1_1=probe_selection(populacja_1)
proba_1_2=probe_selection(populacja_1)
proba_2_1=probe_selection(populacja_2)
proba_2_2=probe_selection(populacja_2)


print("Testy statystyczne dla próby 1 populacji 1:")
histogram(proba_1_1, "Histogram próby 1 populacji 1")
wskazniki_polozenia_rozproszenia(proba_1_1, "1", "1")
u1 = int(input("Podaj x dla populacji 1"))
print(f"Hipoteza A: H0:u1={u1}, H1:u1=/={u1}")
hipoteza_ab(u1,proba_1_1,0.05)

print("Testy statystyczne dla próby 1 populacji 2:")
histogram(proba_2_1, "Histogram próby 1 populacji 2")
wskazniki_polozenia_rozproszenia(proba_2_1, "1", "2")
u2 = int(input("Podaj x dla populacji 2"))
print(f"Hipoteza B: H0:u1={u2}, H1:u1=/={u2}")
hipoteza_ab(u2,proba_2_1,0.05)

print("Hipoteza C: H0:u1-u2=/=0, H1: u1-u2=/=x")
wartosc = int(input("Podaj wartosc x"))
hipoteza_c(wartosc, proba_1_2, proba_2_1,0.05)

print("Testy statystyczne dla próby 2 populacji 1:")
histogram(proba_1_2, "Histogram próby 2 populacji 1")
wskazniki_polozenia_rozproszenia(proba_1_2, "2", "1")
u1 = int(input("Podaj x dla populacji 1"))
print(f"Hipoteza A: H0:u1={u1}, H1:u1=/={u1}")
hipoteza_ab(u1,proba_1_2,0.05)

print("Testy statystyczne dla próby 2 populacji 2:")
histogram(proba_2_2, "Histogram próby 2 populacji 2")
wskazniki_polozenia_rozproszenia(proba_2_2, "2", "2")
u2 = int(input("Podaj x dla populacji 2"))
print(f"Hipoteza B: H0:u1={u2}, H1:u1=/={u2}")
hipoteza_ab(u2,proba_2_2,0.05)

print("Hipoteza C: H0:u1-u2=/=0, H1: u1-u2=/=x")
wartosc = int(input("Podaj wartosc x"))
hipoteza_c(wartosc, proba_1_2, proba_2_2,0.05)