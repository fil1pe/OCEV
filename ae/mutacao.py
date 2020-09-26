from constantes import *
from individuo import Individuo
from utils import swap
from random import random, randint

def bit_flip(individuo, probabilidade):
    cromossomo = individuo.cromossomo[:]
    dimensao = len(cromossomo)
    for i in range(dimensao):
        if random() < probabilidade:
            cromossomo[i] = (cromossomo[i] + 1) % 2
    return Individuo(cromossomo)

def swap_mutation(individuo, probabilidade):
    cromossomo = individuo.cromossomo[:]
    dimensao = len(cromossomo)
    for i in range(dimensao):
        if random() < probabilidade:
            swap(cromossomo, randint(0, dimensao-1), i)
    return Individuo(cromossomo)

def mutacao(populacao, probabilidade, tipo):
    if tipo == BIN:
        return [bit_flip(individuo, probabilidade) for individuo in populacao]
    elif tipo == INT_PERM:
        return [swap_mutation(individuo, probabilidade) for individuo in populacao]