import sys
sys.path.insert(1, 'ae')

from constantes import *
from principal import ae
from math import sqrt, log10

from pprint import pprint

DIM = 128

RUN = 10
GEN = 1000
COD = INT_PERM
POP = 50
PC = 0.85
PM = 1/DIM
K = 6
KP = 1

def colisoes(cromossomo):
    dimensao = len(cromossomo)
    c = 0
    for i in range(dimensao):
        for j in range(i+1, dimensao):
            if(j-i == abs(cromossomo[i]-cromossomo[j])):
                c += 1
                break
    return c

max_colisoes = DIM

def lucro_elemento(linha, coluna, dimensao):
    valor = linha * dimensao + coluna + 1
    if linha % 2 == 0:
        return sqrt(valor)
    return log10(valor)

def lucro(cromossomo):
    dimensao = len(cromossomo)
    return sum([lucro_elemento(i, cromossomo[i], dimensao) for i in cromossomo])

max_lucro = sum([max([lucro_elemento(DIM-1, i, DIM), lucro_elemento(DIM-2, i, DIM)]) for i in range(DIM)])

def fitness(cromossomo):
    FO = lucro(cromossomo)/max_lucro
    H = colisoes(cromossomo)/max_colisoes
    r = -1
    return FO + r*H

if __name__ == "__main__":
    ae(fitness, lucro, colisoes, COD, RUN, GEN, POP, DIM, PC, PM, TORNEIO, K, KP)