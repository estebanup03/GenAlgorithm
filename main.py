import random
import matplotlib.pyplot as plt

class EightPuzzle:
    def __init__(self,populationSize,generationsNumber):
        #Crear una clase algoritmo genetico con parametros Tamaño de poblacion, numero de generaciones y tamaño del chromosome
        self.populationSize = populationSize #Define la cantidad de cromosomas por generacion
        self.generationsNumber = generationsNumber #Define la cantidad de generaciones
        self.chromosomeSize = 9 #el tamaño del cromosoma (Los numeros del 1 al 9)
        self.chromosomeGoal = list(range(1,10)) #Define cual seria el valor ideal

    def generateChromosomes(self): #Funcion para generar la cantidad de cromosomas segun el tamaño de la poblacion
        chromosomes = []
        for i in range(populationSize):
            chromosomes.append(tuple(random.sample(range(1, 10), self.chromosomeSize))) #Una lista de tuplas con numeros aleatorios del 1 al 9
        return chromosomes

    def performance(self,initialPopulation): #Funcion para encontrar el performance de un cromosoma
        scoreList = []
        for chromosome in initialPopulation:
            score = 0
            if chromosome == self.chromosomeGoal: #Si el cromosoma es igual al cromosoma objetivo se asigna un puntaje de 1000 y retorna el puntaje
                score.append(1000)
                continue
            if chromosome.index(min(chromosome)) == 0: #Si el primer numero del cromosoma es el menor numero se suma un puntaje de 300 y sigue averiguando
                score += 300
            difference = []
            zip_object = zip(chromosome, self.chromosomeGoal) #Funcion para juntar las dos listas y restarlas
            for i, j in zip_object:
                difference.append(abs(i - j)) #Resta cada valor de las dos listas el cromosoma a evaluar y el objetivo
            score += 700 - sum(difference)*10 # funcion para multiplicar la suma de las diferencias por 10 y a 700 restarle el valor, mientras mayor sea la diferencia menor sera el score este seria nuestro f(x)
            scoreList.append(score)
        return scoreList

    def workOndata(self,chromosomes,fx):
        suma = sum(fx) #fx sera una lista de tantos valores como sea el tamaño de la poblacion con esto se encuentra la suma
        percentages = [float(x/suma) for x in fx] #Siguiente operacion matematica para encontrar el %/tamaño de poblacion
        weights = [float(x/populationSize) for x in percentages]
        dictPopulation = dict(zip(chromosomes, weights)) #Hacer un diccionario para guardar cromosoma:peso
        return dictPopulation

    def intermediatePopulation(self,dictPopulation):
        """Funcion para rellenar la nueva poblacion a partir de una poblacion intermedia"""
        newPopulation = []
        while len(newPopulation) < 100: #Mientras que no se llene la nueva poblacion que se quede en el loop
            maxKey = max(dictPopulation, key=dictPopulation.get) #Se obtiene el cromosoma que tiene el valor mayor
            newPopulation.append(maxKey) #Se crea la nueva población con el cromosoma encontrado
            dictPopulation[maxKey] -= 1 #Se le resta 1 al valor del score del cromosoma
        return newPopulation

    def mutation(self,newPopulation,mutationProbability):
        if mutationProbability < 0 and mutationProbability > 1: #Validacion para que la probabilidad de mutacion este entre 0 y 1
            print("Probabilidad de mutacion erronea")
            return False
        mutatedPopulation = []
        for element in newPopulation: #recorrer cada elemento de la nueva poblacion para mutarlo
            newList = list(element)
            movements = round(mutationProbability*10) # Definir la cantidad de movimientos
            elementsTomove = random.sample(range(0,9),movements) #Definir los elementos que se van a mover
            for index in elementsTomove:
                x = element[index]
                while True:
                    indexToswap = random.sample(range(0,9),1)[0]
                    if indexToswap != index:
                        newList[index] = newList[indexToswap]
                        newList[indexToswap] = x
                        break
            mutatedPopulation.append(tuple(newList))
        return mutatedPopulation

#Comienza el codigo

populationSize = int(input("Ingrese el tamaño de la población(Cantidad de chromosomes/combinaciones): "))
probabilidadMutacion = float(input("Ingrese la probabilidad de mutacion: "))
generationsNumber = int(input("Ingrese la cantidad de generaciones: "))

experimento = EightPuzzle(populationSize,generationsNumber) #Creacion del objeto a partir de la clase 8-Puzzle
poblacionInicial = EightPuzzle.generateChromosomes(experimento) #Generar la poblacion de manera aleatoria, se genera una lista de Tuplas
#print(poblacionInicial)
mejoresPorgeneracion = []
for generacion in range(generationsNumber):
    score = experimento.performance(poblacionInicial)# Retornar el score de la poblacion inicial
    #print(score)
    poblacionIntermedia = experimento.workOndata(poblacionInicial,score) #Procesamiento de los datos segun la poblacion inicial y el score obtenido
    #print(poblacionIntermedia)
    nuevaPoblacion = experimento.intermediatePopulation(poblacionIntermedia) #Seleccion de los mejores
    #print(nuevaPoblacion)
    poblacionMutada = experimento.mutation(nuevaPoblacion,probabilidadMutacion)#Mutacion de la poblacion seleccionada
    #print(poblacionMutada)
    scoreMutado = experimento.performance(poblacionMutada)
    mejoresPorgeneracion.append(max(scoreMutado))
    poblacionInicial = poblacionMutada
print(mejoresPorgeneracion)

plt.plot(mejoresPorgeneracion)
plt.ylabel("F(x)")
plt.show()





















