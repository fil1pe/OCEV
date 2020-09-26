class Individuo:
    @staticmethod
    def fitness(cromossomo):
        return 0
    
    def __init__(self, cromossomo, calcularFitness=True):
        self.cromossomo = cromossomo
        if calcularFitness:
            self.fitness = Individuo.fitness(cromossomo)
        self.roletaFitness = self.fitness
    
    def copia(self):
        novo_individuo = Individuo(self.cromossomo[:], False)
        novo_individuo.fitness = self.fitness
        novo_individuo.roletaFitness = self.fitness
        return novo_individuo