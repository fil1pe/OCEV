import sys
sys.path.insert(1, 'ae')

from constantes import *
from principal import ae
from math import sqrt, log10

from pprint import pprint

DIM = 128

RUN = 10
GEN = 800#1000#2000#10000
COD = INT_PERM
POP = 50
PC = 0.85
PM = 1/DIM
K = 6
KP = 1

def colisoes(individuo):
    dimensao = len(individuo)
    c = 0
    for i in range(dimensao):
        for j in range(i+1, dimensao):
            if(j-i == abs(individuo[i]-individuo[j])):
                c += 1
                break
    return c

max_colisoes = DIM

def lucro_elemento(linha, coluna, dimensao):
    valor = linha * dimensao + coluna + 1
    if linha % 2 == 0:
        return sqrt(valor)
    return log10(valor)

def lucro(individuo):
    dimensao = len(individuo)
    return sum([lucro_elemento(i, individuo[i], dimensao) for i in individuo])

max_lucro = sum([max([lucro_elemento(DIM-1, i, DIM), lucro_elemento(DIM-2, i, DIM)]) for i in range(DIM)])

def fitness(individuo):
    FO = lucro(individuo)/max_lucro
    H = colisoes(individuo)/max_colisoes
    r = -1
    return FO + r*H

if __name__ == "__main__":
    ae(fitness, lucro, colisoes, COD, RUN, GEN, POP, DIM, PC, PM, TORNEIO, K, KP)