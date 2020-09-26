import sys
sys.path.insert(1, 'ae')
from constantes import *
from principal import inicializa

from tkinter import Canvas

DIM = 200

RUN = 1
GEN = 5000
COD = BIN
POP = 200
PC = 0.8
PM = 0.05#1/DIM
K = 6
KP = 0.7

class Mapa:
    def __init__(self, posicoes):
        self.posicoes = posicoes
        for i in range(len(posicoes)):
            for j in range(len(posicoes[i])):
                if posicoes[i][j] == 2:
                    self.inicio = [i, j]
                elif posicoes[i][j] == 3:
                    self.fim = [i, j]

    def caminha(self, inicio, direcao, proibidos):
        possiveis_direcoes = []
        if inicio[0]+1 < len(self.posicoes) and self.posicoes[inicio[0]+1][inicio[1]] != 0:
            if [inicio[0]+1, inicio[1]] not in proibidos:
                possiveis_direcoes.append([inicio[0]+1, inicio[1]])
        if inicio[0]-1 >= 0 and self.posicoes[inicio[0]-1][inicio[1]] != 0:
            if [inicio[0]-1, inicio[1]] not in proibidos:
                possiveis_direcoes.append([inicio[0]-1, inicio[1]])
        if inicio[1]+1 < len(self.posicoes[0]) and self.posicoes[inicio[0]][inicio[1]+1] != 0:
            if [inicio[0], inicio[1]+1] not in proibidos:
                possiveis_direcoes.append([inicio[0], inicio[1]+1])
        if inicio[1]-1 >= 0 and self.posicoes[inicio[0]][inicio[1]-1] != 0:
            if [inicio[0], inicio[1]-1] not in proibidos:
                possiveis_direcoes.append([inicio[0], inicio[1]-1])
        if len(possiveis_direcoes) == 0:
            return inicio, 0
        direcao %= len(possiveis_direcoes)
        inicio = possiveis_direcoes[direcao]
        return inicio, self.posicoes[inicio[0]][inicio[1]]
        

def le_labirinto(arquivo):
    posicoes = []
    with open(arquivo, "r") as f:
        linhas = f.readlines()
    linhas = [x.strip() for x in linhas]
    for linha in linhas:
        linha = linha[linha.find("{")+1:linha.find("}")].split(',')
        posicoes.append(list(map(int, linha)))
    return Mapa(posicoes)

MAPA_LABIRINTO = le_labirinto('labirinto.txt')

def desenha_mapa(frame, individuo):
    cromossomo = individuo.cromossomo
    linhas, colunas = len(MAPA_LABIRINTO.posicoes), len(MAPA_LABIRINTO.posicoes[0])
    size = frame['width']//max([linhas, colunas])
    canvas = Canvas(frame, width=size*colunas, height=size*linhas)
    for i in range(linhas):
        for j in range(colunas):
            posicao = MAPA_LABIRINTO.posicoes[i][j]
            if posicao == 0:
                cor = '#000'
            elif posicao == 2:
                cor = '#45ff86'
            elif posicao == 3:
                cor = '#ff303e'
            else:
                cor = '#fff'
            canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=cor, outline='')
    cor = '#ffa200'
    aux = size//4
    celula_atual, posicao = MAPA_LABIRINTO.inicio[:], 2
    visitados = []
    for i in range(0, DIM, 2):
        x, y = celula_atual
        canvas.create_rectangle(y*size+aux, x*size+aux, (y+1)*size-aux, (x+1)*size-aux, fill=cor, outline='')
        visitados.append(celula_atual)
        direcao = cromossomo[i] + 2*cromossomo[i+1]
        celula_atual, posicao = MAPA_LABIRINTO.caminha(celula_atual, direcao, visitados)
        if posicao == 0 or posicao == 3:
            break
    x, y = celula_atual
    canvas.create_rectangle(y*size+aux, x*size+aux, (y+1)*size-aux, (x+1)*size-aux, fill=cor, outline='')
    canvas.pack()

maior_distancia = abs(0 - 24) + abs(0 - 29)

def objetivo(cromossomo):
    dimensao = len(cromossomo)
    celula_atual, posicao = MAPA_LABIRINTO.inicio[:], 2
    visitados = []
    melhor_distancia = maior_distancia
    for i in range(0, dimensao, 2):
        visitados.append(celula_atual)
        direcao = cromossomo[i] + 2*cromossomo[i+1]
        celula_atual, posicao = MAPA_LABIRINTO.caminha(celula_atual, direcao, visitados)
        aux = abs(celula_atual[0] - 24) + abs(celula_atual[1] - 29)
        if aux < melhor_distancia:
            melhor_distancia = aux
        if posicao == 0 or posicao == 3:
            break
    return 1.0 - aux/maior_distancia

def colisoes(cromossomo):
    return 0

def fitness(cromossomo):
    return objetivo(cromossomo)

if __name__ == "__main__":
    inicializa(fitness, objetivo, colisoes, COD, RUN, GEN, POP, DIM, PC, PM, ROLETA, K, KP, True, desenha_mapa, True)