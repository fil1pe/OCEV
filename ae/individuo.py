class Individuo:
    @staticmethod
    def fitness(cromossomo):
        return 0
    
    def __init__(self, cromossomo, calcularFitness=True):
        self.cromossomo = cromossomo
        if calcularFitness:
            self.fitness = Individuo.fitness(cromossomo)
    
    def copia(self):
        novo_individuo = Individuo(self.cromossomo[:], False)
        novo_individuo.fitness = self.fitness
        return novo_individuo