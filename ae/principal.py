from constantes import *
from individuo import Individuo
from populacao_inicial import populacao_inicial
from selecao import selecao
from crossover import crossover
from mutacao import mutacao
from utils import media, desvio_padrao

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Janela:
    def __init__(self, root, fitness, objetivo, penalidade, codificacao, execucoes, geracoes, tam_populacao, dimensao, prob_crossover, prob_mutacao, selecao, sel_arg0, sel_arg1, elitismo, desenho):
        Individuo.fitness = fitness
        self.objetivo = objetivo
        self.penalidade = penalidade
        self.codificacao = codificacao
        self.execucoes = execucoes
        self.geracoes = geracoes
        self.tam_populacao = tam_populacao
        self.dimensao = dimensao
        self.prob_crossover = prob_crossover
        self.prob_mutacao = prob_mutacao
        self.selecao = selecao
        self.sel_arg0 = sel_arg0
        self.sel_arg1 = sel_arg1
        self.elitismo = elitismo
        self.desenho = desenho

        self.root = root
        tk.Tk.wm_title(root, 'Algoritmo evolucionário')
        root.resizable(False, False)

        container_pai = tk.Frame(root)
        container_pai.pack(side='left')

        container = tk.Frame(container_pai)
        container.pack(side='top')

        f = Figure(figsize=(6, 4), constrained_layout=True)#figsize=(6,3), dpi=100)
        self.subplot = f.add_subplot(111)

        self.subplot.set_xlim((0, self.geracoes))
        self.subplot.set_xlabel('geração')
        self.subplot.set_ylabel('fitness média')

        self.plt_canvas = FigureCanvasTkAgg(f, container)
        self.plt_canvas.draw()
        self.plt_canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)

        toolbar = NavigationToolbar2Tk(self.plt_canvas, container)
        toolbar.update()
        self.plt_canvas._tkcanvas.pack(side='top', fill='both', expand=True)

        container = tk.Frame(container_pai)
        container.pack(side='top', fill='both')

        botao = tk.Button(container)
        botao['text'] = 'Executar'
        botao['command'] = self.evolucao
        botao.pack()

        self.progress_bar = [ttk.Progressbar(container, orient=tk.HORIZONTAL, length=100, mode='determinate'),
            ttk.Progressbar(container, orient=tk.HORIZONTAL, length=100, mode='determinate')]
        self.progress_bar[0].pack(fill='both')
        self.progress_bar[1].pack(fill='both')

        self.media_desvio_label = tk.Label(container, text='Média: -\nDesvio padrão: -')
        self.media_desvio_label.pack()

        container_pai = tk.Frame(root)
        container_pai.pack(side='right')

        self.desenho_container = tk.Frame(container_pai, width=300, height=300)
        self.desenho_container.pack(side='top')

        container = tk.Frame(container_pai)
        container.pack(side='top')

        self.solucao_label = tk.Label(container, text='Valor: -\nPenalidades: -')
        self.solucao_label.pack()
    
    def desenha(self, individuo):
        if self.desenho == False:
            return
        for widget in self.desenho_container.winfo_children():
            widget.destroy()
        self.desenho(self.desenho_container, individuo)

    def evolucao(self):
        if self.codificacao == INT_PERM:
            tipo_crossover = PMX

        plot_data = [[0 for _ in range(self.geracoes)] for _ in range(3)]

        self.progress_bar[1]['value'] = 0
        self.root.update_idletasks()

        melhores = []

        for i in range(self.execucoes):
            populacao = populacao_inicial(self.codificacao, self.tam_populacao, self.dimensao)

            for j in range(self.geracoes):
                self.progress_bar[0]['value'] = j/self.geracoes * 100
                self.root.update_idletasks()

                if self.elitismo:
                    melhor_populacao = max(populacao, key=lambda x : x.fitness)
                    populacao.remove(melhor_populacao)
                    self.tam_populacao -= 1
                
                populacao = selecao(populacao, self.tam_populacao, self.selecao, self.sel_arg0, self.sel_arg1)
                populacao += crossover(populacao, self.tam_populacao, self.prob_crossover, tipo_crossover)
                populacao = mutacao(populacao, self.prob_mutacao, self.codificacao)

                if self.elitismo:
                    populacao.append(melhor_populacao)
                    self.tam_populacao += 1
                
                melhor_populacao = max(populacao, key=lambda x : x.fitness)
                if len(melhores) == i:
                    melhores.append(melhor_populacao)
                else:
                    melhores[i] = max([melhores[i], melhor_populacao], key=lambda x : x.fitness)
                plot_data[0][j] = (i*plot_data[0][j] + melhor_populacao.fitness) / (i+1)
                plot_data[1][j] = (i*plot_data[1][j] + sum([individuo.fitness for individuo in populacao])/len(populacao)) / (i+1)
                plot_data[2][j] = (i*plot_data[2][j] + min(populacao, key=lambda x : x.fitness).fitness) / (i+1)

            melhor = max(melhores, key=lambda x : x.fitness)
            self.progress_bar[1]['value'] = (i+1)/(self.execucoes) * 100
            self.solucao_label['text'] = 'Valor: {}\nPenalidades: {}'.format(self.objetivo(melhor.cromossomo), self.penalidade(melhor.cromossomo))
            self.desenha(melhor)
            self.root.update_idletasks()

            self.subplot.clear()
            self.subplot.plot(plot_data[0], label='Melhor indivíduo', color='green')
            self.subplot.plot(plot_data[1], label='Média da população', color='purple')
            self.subplot.plot(plot_data[2], label='Pior indivíduo', color='red')
            self.subplot.set_xlim((0, self.geracoes))
            self.subplot.set_xlabel("geração")
            self.subplot.set_ylabel("fitness média")
            self.subplot.legend()
            self.plt_canvas.draw()
        
        objetivos = [self.objetivo(individuo.cromossomo) for individuo in melhores]
        self.media_desvio_label['text'] = 'Média: {}\nDesvio padrão: {}'.format(media(objetivos), desvio_padrao(objetivos))
        self.root.update_idletasks()

def inicializa(*args):
    root = tk.Tk()
    Janela(root, *args)
    root.mainloop()