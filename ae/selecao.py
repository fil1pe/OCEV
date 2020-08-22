from constantes import *
from utils import copia_populacao
from random import random, randint

def selecao_roleta(populacao, tamanho):
    selecionados = []

    posicao = []
    soma_fitness = 0
    for individuo in populacao:
        soma_fitness += individuo.fitness
    aux = 0
    for individuo in populacao:
        aux += individuo.fitness/soma_fitness
        posicao.append(aux)

    aux = 0
    while aux < tamanho:
        prob = random()
        for i in range(len(populacao)):
            if posicao[i] >= prob:
                selecionados.append(populacao[i].copia())
                aux += 1
                break
    
    return selecionados

def selecao_torneio(populacao, tamanho, k, kp):
    selecionados = []

    t = 0
    while t < tamanho:
        aux = copia_populacao(populacao)
        k_aleatorios = []
        l = len(aux)
        for _ in range(k):
            ind = randint(0, l-1)
            k_aleatorios.append(aux[ind])
            aux.pop(ind)
            l -= 1
        if random() <= kp:
            selecionados.append(max(k_aleatorios, key=lambda x : x.fitness))
        else:
            selecionados.append(min(k_aleatorios, key=lambda x : x.fitness))
        t += 1
    
    return selecionados

def selecao(populacao, tamanho, tipo, arg1=0, arg2=0):
    if tipo == ROLETA:
        return selecao_roleta(populacao, tamanho)
    elif tipo == TORNEIO:
        return selecao_torneio(populacao, tamanho, arg1, arg2)