from math import sqrt

def swap(lista, a, b):
    temp = lista[a]
    lista[a] = lista[b]
    lista[b] = temp

def copia_populacao(populacao):
    return [individuo[:] for individuo in populacao]

def media(lista):
    return sum(lista)/len(lista)

def desvio_padrao(lista):
    m = media(lista)
    return sqrt(sum([(i - m)**2 for i in lista])/len(lista))