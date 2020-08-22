from constantes import *
from utils import copia_populacao
from random import random, randint

def selecao_roleta(populacao, fitness, tamanho):
    selecionados = []

    posicao = []
    soma_fitness = 0
    for individuo in populacao:
        soma_fitness += fitness(individuo)
    aux = 0
    for individuo in populacao:
        aux += fitness(individuo)/soma_fitness
        posicao.append(aux)

    aux = 0
    while aux < tamanho:
        prob = random()
        for i in range(len(populacao)):
            if posicao[i] >= prob:
                selecionados.append(populacao[i][:])
                aux += 1
                break
    
    return selecionados

def selecao_torneio(populacao, fitness, tamanho, k, kp):
    selecionados = []

    t = 0
    while t < tamanho:
        aux = copia_populacao(populacao)
        k_aleatorios = []
        l = len(aux)
        for i in range(k):
            ind = randint(0, l-1)
            k_aleatorios.append(aux[ind])
            aux.pop(ind)
            l -= 1
        if random() <= kp:
            selecionados.append(max(k_aleatorios, key=lambda x : fitness(x)))
        else:
            selecionados.append(min(k_aleatorios, key=lambda x : fitness(x)))
        t += 1
    
    return selecionados

def selecao(populacao, fitness, tamanho, tipo, arg1=0, arg2=0):
    if tipo == ROLETA:
        return selecao_roleta(populacao, fitness, tamanho)
    elif tipo == TORNEIO:
        return selecao_torneio(populacao, fitness, tamanho, arg1, arg2)