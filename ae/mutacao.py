from constantes import *
from utils import swap
from random import random, randint

def swap_mutation(individuo, probabilidade):
    dimensao = len(individuo)
    individuo = individuo[:]
    for i in range(dimensao):
        if random() < probabilidade:
            swap(individuo, randint(0, dimensao-1), i)
    return individuo

def mutacao(populacao, probabilidade, tipo):
    if tipo == INT_PERM:
        return [swap_mutation(individuo, probabilidade) for individuo in populacao]