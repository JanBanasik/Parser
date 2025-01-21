from collections import defaultdict
from dataclasses import dataclass
import json


@dataclass
class EarleySituation:
    lewa: str
    prawa: str
    h: int
    i: int
    pozycjaKropki: int

    def __repr__(self):
        temp = list(self.prawa[:])
        temp.insert(self.pozycjaKropki, '·')
        temp = "".join(temp)
        return f"{self.lewa} -> {temp}[{self.h}, {self.i}]"


def wczytanie(earleySituation: EarleySituation, lista, slowo):
    if earleySituation.i < len(slowo) and \
            slowo[earleySituation.i] == earleySituation.prawa[earleySituation.pozycjaKropki]:
        lista[earleySituation.i + 1].append(
            EarleySituation(
                earleySituation.lewa, earleySituation.prawa, earleySituation.h,
                earleySituation.i + 1, earleySituation.pozycjaKropki + 1
            )
        )


def przewidywanie(earleySituation: EarleySituation, lista, wykonanePrzewidywania, P):
    nieterminal = earleySituation.prawa[earleySituation.pozycjaKropki]
    if nieterminal not in wykonanePrzewidywania[earleySituation.i]:
        wykonanePrzewidywania[earleySituation.i].append(nieterminal)
        lista[earleySituation.i].extend(
            EarleySituation(nieterminal, el, earleySituation.i, earleySituation.i, 0)
            for el in P.get(nieterminal, [])
        )


def uzupelnianie(earleySituation, lista):
    for sytuacja in lista[earleySituation.h]:
        if sytuacja.pozycjaKropki < len(sytuacja.prawa) and \
                sytuacja.prawa[sytuacja.pozycjaKropki] == earleySituation.lewa:
            lista[earleySituation.i].append(
                EarleySituation(
                    sytuacja.lewa, sytuacja.prawa, sytuacja.h,
                    earleySituation.i, sytuacja.pozycjaKropki + 1
                )
            )


def executeProcedure(P, terminale, slowo, symbolStartowy):
    lista = defaultdict(list)
    wykonanePrzewidywania = defaultdict(list)
    lista[0].append(EarleySituation("S'", symbolStartowy, 0, 0, 0))

    for index in range(len(slowo) + 1):
        i = 0
        while i < len(lista[index]):
            sytuacja = lista[index][i]
            if sytuacja.pozycjaKropki == len(sytuacja.prawa):  # Uzupelnianie
                uzupelnianie(sytuacja, lista)
            elif sytuacja.prawa[sytuacja.pozycjaKropki] not in terminale:  # Przewidywanie
                przewidywanie(sytuacja, lista, wykonanePrzewidywania, P)

            i += 1

        # Na koniec wczytujemy
        for sytuacja in lista[index]:
            if sytuacja.pozycjaKropki < len(sytuacja.prawa) and \
                    sytuacja.prawa[sytuacja.pozycjaKropki] in terminale:
                wczytanie(sytuacja, lista, slowo)

    printResults(lista, slowo, symbolStartowy)


def printResults(lista, slowo, symbolStartowy):
    for index, sytuacje in lista.items():
        print(f"i: {index}")
        for syt in sytuacje:
            print(syt)
    print()
    expected = EarleySituation("S'", symbolStartowy, 0, len(slowo), 1)
    if expected not in lista[len(slowo)]:
        print(f"Słowo '{slowo}' nie należy do języka.")
    else:
        print(f"Słowo '{slowo}' należy do języka.")
    print()


def loadAndExecuteTests(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)

    for index, case in enumerate(data):
        P = case["P"]
        terminale = case["terminale"]
        slowo = case["slowo"]
        symbolStartowy = case["symbolStartowy"]
        print(f"{P=}\n{terminale=}\n{slowo=}\n{symbolStartowy=}\n")
        executeProcedure(P, terminale, slowo, symbolStartowy)
        print("-" * 50)


# Wywołanie testów
loadAndExecuteTests("testcases.json")
