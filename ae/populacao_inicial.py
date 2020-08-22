from constantes import *
from individuo import Individuo
from random import randint

def individuo_aleatorio(tipo, dimensao):
    cromossomo = []
    if tipo == INT_PERM:
        aux = [i for i in range(dimensao)]
        l = len(aux)
        while l > 0:
            ind = randint(0, l-1)
            cromossomo.append(aux[ind])
            aux.pop(ind)
            l -= 1
    return Individuo(cromossomo)

def populacao_inicial(tipo, tamanho, dimensao):
    return [individuo_aleatorio(tipo, dimensao) for _ in range(tamanho)]