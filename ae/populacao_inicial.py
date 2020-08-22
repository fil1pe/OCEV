from constantes import *
from random import randint

def individuo_aleatorio(tipo, dimensao):
    individuo = []
    if tipo == INT_PERM:
        aux = [i for i in range(dimensao)]
        l = len(aux)
        while l > 0:
            ind = randint(0, l-1)
            individuo.append(aux[ind])
            aux.pop(ind)
            l -= 1
    return individuo

def populacao_inicial(tipo, tamanho, dimensao):
    return [individuo_aleatorio(tipo, dimensao) for _ in range(tamanho)]