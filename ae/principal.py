from constantes import *
from populacao_inicial import populacao_inicial
from selecao import selecao
from crossover import crossover
from mutacao import mutacao

import matplotlib.pyplot as plt

def print_solucao(populacao, fitness, objetivo, penalidade):
    populacao = sorted(populacao, key=lambda x : fitness(x))
    populacao.reverse()
    melhor = populacao[0]
    pior = populacao[-1]
    print('Melhor fitness: {}\nPior fitness: {}'.format(fitness(melhor), fitness(pior)))

    for individuo in populacao:
        if penalidade(individuo) == 0:
            print('Melhor solução\nFitness: {}\nObjetivo: {}'.format(fitness(individuo), objetivo(individuo)))
            break

def ae(fitness, objetivo, penalidade, COD, RUN, GEN, POP, DIM, PC, PM, SEL, sel_arg0=0, sel_arg1=0, elitismo=True):
    if COD == INT_PERM:
        CO = PMX

    plt.ion()
    plot_data = [[0 for _ in range(GEN)] for _ in range(3)]

    for i in range(RUN):
        populacao = populacao_inicial(COD, POP, DIM)
        print_solucao(populacao, fitness, objetivo, penalidade)

        for j in range(GEN):
            print('\r{:.2f} %'.format(j/GEN * 100), end='')

            if elitismo:
                melhor = max(populacao, key=lambda x : fitness(x))
                populacao.remove(melhor)
                POP -= 1
            
            populacao = selecao(populacao, fitness, POP, SEL, sel_arg0, sel_arg1)
            populacao += crossover(populacao, POP, PC, CO)
            populacao = mutacao(populacao, PM, COD)

            if elitismo:
                populacao.append(melhor)
                POP += 1
            
            plot_data[0][j] = (i*plot_data[0][j] + fitness(max(populacao, key=lambda x : fitness(x))) ) / (i+1)
            plot_data[1][j] = (i*plot_data[1][j] + sum([fitness(individuo) for individuo in populacao])/len(populacao) ) / (i+1)
            plot_data[2][j] = (i*plot_data[2][j] + fitness(min(populacao, key=lambda x : fitness(x))) ) / (i+1)
        print('\r========================\n', end='')
        print_solucao(populacao, fitness, objetivo, penalidade)
        print()

        plt.clf()
        plt.xlim((0,GEN))
        plt.xlabel("geração")
        plt.ylabel("fitness")
        plt.plot(plot_data[0], label = 'Melhor indivíduo', color = 'green')
        plt.plot(plot_data[1], label = 'Média da população', color = 'purple')
        plt.plot(plot_data[2], label = 'Pior indivíduo', color = 'red')
        plt.legend()
        plt.pause(1)

    plt.ioff()
    plt.show()