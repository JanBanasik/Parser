from collections import defaultdict
import json


class EarleySituation:
    def __init__(self, lewa, prawa, h, i, pozycjaKropki):
        self.lewa = lewa
        self.prawa = prawa
        self.h = h
        self.i = i
        self.pozycjaKropki = pozycjaKropki

    def __repr__(self):
        temp = list(self.prawa[:])
        temp.insert(self.pozycjaKropki, '·')
        temp = "".join(temp)
        return f"{self.lewa} -> {temp}[{self.h}, {self.i}]"

    def __eq__(self, other):
        return self.lewa == other.lewa and self.prawa == other.prawa and self.h == other.h and self.i == other.i and self.pozycjaKropki == other.pozycjaKropki


def wczytanie(earleySituation: EarleySituation, lista, slowo):
    if earleySituation.i == len(slowo):
        return
    if slowo[earleySituation.i] == earleySituation.prawa[earleySituation.pozycjaKropki]:
        lista[earleySituation.i + 1].append(
            EarleySituation(earleySituation.lewa, earleySituation.prawa, earleySituation.h, earleySituation.i + 1,
                            earleySituation.pozycjaKropki + 1))


def przewidywanie(earleySituation: EarleySituation, lista, wykonanePrzewidywania, P):
    nieterminal = earleySituation.prawa[earleySituation.pozycjaKropki]
    if nieterminal in wykonanePrzewidywania[earleySituation.i]:
        return
    wykonanePrzewidywania[earleySituation.i].append(nieterminal)
    for el in P.get(nieterminal, []):
        lista[earleySituation.i].append(EarleySituation(nieterminal, el, earleySituation.i, earleySituation.i, 0))


def uzupelnianie(earleySituation, lista):
    for sytuacja in lista[earleySituation.h]:
        try:
            if sytuacja.prawa[sytuacja.pozycjaKropki] == earleySituation.lewa:
                lista[earleySituation.i].append(EarleySituation(sytuacja.lewa, sytuacja.prawa,
                                                                sytuacja.h, earleySituation.i,
                                                                sytuacja.pozycjaKropki + 1))
        except IndexError:
            continue


def executeProcedure(P, terminale, slowo, symbolStartowy):
    lista = defaultdict(list)
    wykonanePrzewidywania = defaultdict(list)
    lista[0].append(EarleySituation("S'", symbolStartowy, 0, 0, 0))
    for index in range(len(slowo) + 1):
        i = 0
        while i < len(lista[index]):
            sytuacja = lista[index][i]
            if len(sytuacja.prawa) == sytuacja.pozycjaKropki:
                # print("Uzupelnianie")
                uzupelnianie(sytuacja, lista)
            elif sytuacja.prawa[sytuacja.pozycjaKropki] in terminale:
                # print("Wczytanie")
                wczytanie(sytuacja, lista, slowo)
            else:
                # print("Przewidywanie")
                przewidywanie(sytuacja, lista, wykonanePrzewidywania, P)
            i += 1

    for index in range(len(slowo) + 1):
        print(f"i: {index}")
        for syt in lista[index]:
            print(syt)
    print()
    if EarleySituation("S'", symbolStartowy, 0, len(slowo), 1) not in lista[len(slowo)]:
        print(f"Slowo {slowo} nie nalezy do jezyka")
    else:
        print(f"Slowo {slowo} nalezy do jezyka")
    print()

with open("testcases.json", "r") as file:
    data = json.load(file)

for index, case in enumerate(data):
    P = case["P"]
    terminale = case["terminale"]
    slowo = case["slowo"]
    symbolStartowy = case["symbolStartowy"]
    print(f"{P=}\n{terminale=}\n{slowo=}\n{symbolStartowy=}\n")
    executeProcedure(P, terminale, slowo, symbolStartowy)
    print(f"-----------------------------------------------------")
