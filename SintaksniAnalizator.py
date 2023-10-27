import pandas as pd
import numpy as np
import sys
from typing import List

rez_lex = sys.stdin.read().split("\n")

if rez_lex[-1] == "":
    rez_lex[-1] = "%"
else:
    rez_lex.append("%")

colnames = ['IDN', 'BROJ', 'OP_PRIDRUZI', 'OP_PLUS', 'OP_MINUS', 'OP_PUTA', 'OP_DIJELI', 'L_ZAGRADA', 'D_ZAGRADA',
            'KR_ZA', 'KR_OD', 'KR_DO', 'KR_AZ', '%']
rownames = ['<program>', '<lista_naredbi>', '<naredba>', '<naredba_pridruzivanja>', '<za_petlja>', '<E>', '<E_lista>',
            '<T>', '<T_lista>', '<P>', 'IDN', 'OP_PRIDRUZI', 'KR_OD', 'KR_DO', 'KR_AZ', 'D_ZAGRADA', '#']
data = np.array([[["<lista_naredbi>", False], None, None, None, None, None, None, None, None, ["<lista_naredbi>", False],
                  None, None, None, ["<lista_naredbi", False]],
                 [["<lista_naredbi> <naredba>", False], None, None, None, None, None, None, None, None,
                  ["<lista_naredbi> <naredba>", False], None, None, ["", False], ["", False]],
                 [["<naredba_pridruzivanja>", False], None, None, None, None, None, None, None, None,
                  ["<za_petlja>", False], None, None, None, None],
                 [["<E> OP_PRIDRUZI", True], None, None, None, None, None, None, None, None, None, None, None, None,
                  None],
                 [None, None, None, None, None, None, None, None, None,
                  ["KR_AZ <lista_naredbi> <E> KR_DO <E> KR_OD IDN", True], None, None, None, None],
                 [["<E_lista> <T>", False], ["<E_lista> <T>", False], None, ["<E_lista> <T>", False],
                  ["<E_lista> <T>", False], None, None, ["<E_lista> <T>", False], None, None, None, None, None, None],
                 [["", False], None, None, ["<E>", True], ["<E>", True], None, None, None, ["", False], ["", False],
                  None, ["", False], ["", False], ["", False]],
                 [["<T_lista> <P>", False], ["<T_lista> <P>", False], None, ["<T_lista> <P>", False],
                  ["<T_lista> <P>", False], None, None, ["<T_lista> <P>", False], None, None, None, None, None, None],
                 [["", False], None, None, ["", False], ["", False], ["<T>", True], ["<T>", True], None, ["", False],
                  ["", False], None, ["", False], ["", False], ["", False]],
                 [["", True], ["", True], None, ["<P>", True], ["<P>", True], None, None, ["D_ZAGRADA <E>", True], None,
                  None, None, None, None, None],
                 [["", True], None, None, None, None, None, None, None, None, None, None, None, None, None],
                 [None, None, ["", True], None, None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None, ["", True], None, None, None],
                 [None, None, None, None, None, None, None, None, None, None, None, ["", True], None, None],
                 [None, None, None, None, None, None, None, None, None, None, None, None, ["", True], None],
                 [None, None, None, None, None, None, None, None, ["", True], None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None, None, None, None, "Prihvati"]],
                dtype=object)

parser = pd.DataFrame(data, columns=colnames)
parser.index = rownames

stog: List[list] = [["#", "<program>"], [-1, 0]]

stablo = ""

i = 0
while i < len(rez_lex):
    if rownames.count(stog[0][-1]) == 0 or colnames.count(rez_lex[i].split(" ")[0]) == 0:
        print("err " + (rez_lex[i] if rez_lex[i] != "%" else "kraj"))
        exit(0)
    element = parser.at[stog[0][-1], rez_lex[i].split(" ")[0]]
    if element:
        if len(element) == 2:
            dubina = stog[1][-1]
            if colnames.count(stog[0][-1]) == 0:
                stablo += " " * dubina + stog[0][-1] + "\n"
            maknuto = stog[0].pop()
            stog[1].pop()
            for el in element[0].split(" "):
                if el != "":
                    stog[0].append(el)
                    stog[1].append(dubina + 1)
            if element[1]:
                if maknuto == rez_lex[i].split(" ")[0]:
                    stablo += " " * dubina + rez_lex[i] + "\n"
                else:
                    stablo += " " * (dubina + 1) + rez_lex[i] + "\n"
            if element[0] == "" and not element[1]:
                stablo += " " * (dubina + 1) + "$\n"
            if element[1]:
                i += 1
        else:
            print(stablo)
            exit(0)
    else:
        print("err " + (rez_lex[i] if rez_lex[i] != "%" else "kraj"))
        exit(0)

