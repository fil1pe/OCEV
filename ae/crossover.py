from constantes import *
from individuo import Individuo
from utils import copia_populacao
from random import randint, random

def um_ponto(mae, pai):
    mae = mae.cromossomo
    pai = pai.cromossomo

    ponto = randint(0, len(mae))

    return Individuo(mae[:ponto] + pai[ponto:]), Individuo(pai[:ponto] + mae[ponto:])

def pmx(mae, pai):
    mae = mae.cromossomo
    pai = pai.cromossomo

    filho = [0 for _ in range(len(mae))]
    filho_map = [False for _ in range(len(filho))]

    ponto = randint(0, len(mae)-2)
    n = randint(1, len(mae)-ponto)
    for i in range(ponto, ponto + n):
        filho_map[i] = True
        filho[i] = mae[i]

    for i in range(len(pai)):
        filho_contem = False
        for j in range(len(filho)):
            if filho_map[j] and filho[j] == pai[i]:
                filho_contem = True
                break
        if filho_contem:
            continue
        
        v_ind = i
        while True:
            v = mae[v_ind]
            v_ind = pai.index(v)
            if not filho_map[v_ind]:
                break
        filho[v_ind] = pai[i]
        filho_map[v_ind] = True
    
    return Individuo(filho)

def crossover(populacao, tamanho, probabilidade, tipo):
    nova_populacao = []
    populacao = copia_populacao(populacao)
    aux = len(populacao)
    t = 0
    while t < tamanho and aux >= 2:
        ind = randint(0, aux-1)
        mae = populacao[ind]
        populacao.pop(ind)

        ind = randint(0, aux-2)
        pai = populacao[ind]
        populacao.pop(ind)

        aux -= 2

        if random() < probabilidade:
            if tipo == UM_PONTO:
                filho1, filho2 = um_ponto(mae, pai)
            elif tipo == PMX:
                filho1 = pmx(mae, pai)
                filho2 = pmx(pai, mae)
        else:
            filho1 = mae
            filho2 = pai

        nova_populacao.append(filho1)
        nova_populacao.append(filho2)
        t += 2
    return nova_populacao




