from constantes import *
from individuo import Individuo
from utils import copia_populacao
from random import random, randint

def roletaCtes(populacao):
    fmin = min(populacao, key=lambda x: x.fitness)
    fmax = max(populacao, key=lambda x: x.fitness)
    favg = sum([i.fitness for i in populacao])/len(populacao)
    if fmin > (Individuo.roletaC*favg - fmax) / (Individuo.roletaC - 1):
        alfa = (favg * (Individuo.roletaC-1)) / (fmax - favg)
        beta = (favg * (fmax - Individuo.roletaC*favg)) / (fmax - favg)
    else:
        alfa = favg / (favg - fmin)
        beta = (-fmin * favg) / (favg - fmin)
    return alfa, beta

def selecao_roleta(populacao, tamanho):
    selecionados = []

    alfa, beta = roletaCtes(populacao)

    for i in populacao:
        i.roletaFitness = alfa*i.fitness + beta

    posicao = []
    soma_fitness = 0
    for individuo in populacao:
        soma_fitness += individuo.roletaFitness
    aux = 0
    for individuo in populacao:
        aux += individuo.roletaFitness/soma_fitness
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