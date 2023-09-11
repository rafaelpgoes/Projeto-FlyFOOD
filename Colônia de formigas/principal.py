import math
import random
from plot import plot 
import time

# Gere uma semente aleatória única para cada execução (Para utilizar alguma, coloque-a aqui)
random_seed = random.randint(0, 10000)

# Configure a semente aleatória
random.seed(random_seed)

class Grafo(object):
    def __init__(self, matriz_custos: list, rank: int):
        """
        :param matriz_custos:
        :param rank: tamanho da matriz de custos
        """
        self.matriz = matriz_custos
        self.rank = rank
        # noinspection PyUnusedLocal
        self.feromonio = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, quantidade_formigas: int, geracoes: int, alpha: float, beta: float, rho: float, q: int,
                 estrategia: int):
        """
        :param quantidade_formigas:
        :param geracoes:
        :param alpha: importância relativa do feromônio
        :param beta: importância relativa da informação heurística
        :param rho: coeficiente residual de feromônio
        :param q: intensidade do feromônio
        :param estrategia: estratégia de atualização do feromônio. 0 - ciclo de formigas, 1 - qualidade da formiga, 2 - densidade de formigas
        """
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.quantidade_formigas = quantidade_formigas
        self.geracoes = geracoes
        self.estrategia_atualizacao = estrategia

    def _atualiza_feromonio(self, grafo: Grafo, formigas: list):
        for i, linha in enumerate(grafo.feromonio):
            for j, coluna in enumerate(linha):
                grafo.feromonio[i][j] *= self.rho
                for formiga in formigas:
                    grafo.feromonio[i][j] += formiga.delta_feromonio[i][j]

    # noinspection PyProtectedMember
    def resolver(self, grafo: Grafo):
        """
        :param grafo:
        """
        melhor_custo = float('inf')
        melhor_solucao = []
        for gen in range(self.geracoes):
            # noinspection PyUnusedLocal
            formigas = [_Formiga(self, grafo) for i in range(self.quantidade_formigas)]
            for formiga in formigas:
                for i in range(grafo.rank - 1):
                    formiga._seleciona_proxima()
                formiga.custo_total += grafo.matriz[formiga.tabu[-1]][formiga.tabu[0]]
                if formiga.custo_total < melhor_custo:
                    melhor_custo = formiga.custo_total
                    melhor_solucao = [] + formiga.tabu
                # atualiza feromônio
                formiga._atualiza_delta_feromonio()
            self._atualiza_feromonio(grafo, formigas)
            # print('geração #{}, melhor custo: {}, caminho: {}'.format(gen, melhor_custo, melhor_solucao))
        return melhor_solucao, melhor_custo


class _Formiga(object):
    def __init__(self, aco: ACO, grafo: Grafo):
        self.colonia = aco
        self.grafo = grafo
        self.custo_total = 0.0
        self.tabu = []  # lista tabu
        self.delta_feromonio = []  # o aumento local de feromônio
        self.permitted = [i for i in range(grafo.rank)]  # nós permitidos para a próxima seleção
        self.eta = [[0 if i == j else 1 / grafo.matriz[i][j] for j in range(grafo.rank)] for i in
                    range(grafo.rank)]  # informação heurística
        inicio = random.randint(0, grafo.rank - 1)  # começa de qualquer nó
        self.tabu.append(inicio)
        self.atual = inicio
        self.permitted.remove(inicio)

    def _seleciona_proxima(self):
        denominador = 0
        for i in self.permitted:
            denominador += self.grafo.feromonio[self.atual][i] ** self.colonia.alpha * self.eta[self.atual][
                                                                                            i] ** self.colonia.beta
        # noinspection PyUnusedLocal
        probabilidades = [0 for i in range(self.grafo.rank)]  # probabilidades para mover-se para um nó no próximo passo
        for i in range(self.grafo.rank):
            try:
                self.permitted.index(i)  # testa se a lista de permitidos contém i
                probabilidades[i] = self.grafo.feromonio[self.atual][i] ** self.colonia.alpha * \
                    self.eta[self.atual][i] ** self.colonia.beta / denominador
            except ValueError:
                pass  # não faz nada
        # seleciona o próximo nó por roleta de probabilidade
        selecionado = 0
        rand = random.random()
        for i, probabilidade in enumerate(probabilidades):
            rand -= probabilidade
            if rand <= 0:
                selecionado = i
                break
        self.permitted.remove(selecionado)
        self.tabu.append(selecionado)
        self.custo_total += self.grafo.matriz[self.atual][selecionado]
        self.atual = selecionado

    # noinspection PyUnusedLocal
    def _atualiza_delta_feromonio(self):
        self.delta_feromonio = [[0 for j in range(self.grafo.rank)] for i in range(self.grafo.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]
            if self.colonia.estrategia_atualizacao == 1:  # sistema de qualidade da formiga
                self.delta_feromonio[i][j] = self.colonia.Q
            elif self.colonia.estrategia_atualizacao == 2:  # sistema de densidade de formigas
                # noinspection PyTypeChecker
                self.delta_feromonio[i][j] = self.colonia.Q / self.grafo.matriz[i][j]
            else:  # sistema de ciclo de formigas
                self.delta_feromonio[i][j] = self.colonia.Q / self.custo_total


# Chamada principal do código
def distancia(cidade1: dict, cidade2: dict):
    return math.sqrt((cidade1['x'] - cidade2['x']) ** 2 + (cidade1['y'] - cidade2['y']) ** 2)


def principal():
    inicio_execucao = time.time()
    cidades = []
    pontos = []
    with open('C:/Users/Rafael Peralta/OneDrive/Documents/CURSOS/PYTHON/marcelo/ant-colony-tsp-master/data/berlin52.txt') as f:
        for linha in f.readlines():
            cidade = linha.split(' ')
            cidades.append(dict(indice=int(cidade[0]), x=int(cidade[1]), y=int(cidade[2])))
            pontos.append((int(cidade[1]), int(cidade[2])))
    matriz_custos = []
    rank = len(cidades)
    for i in range(rank):
        linha = []
        for j in range(rank):
            linha.append(distancia(cidades[i], cidades[j]))
        matriz_custos.append(linha)
    aco = ACO(50, 300, 1.0, 10.0, 0.9, 15, 2)
    grafo = Grafo(matriz_custos, rank)
    caminho, custo = aco.resolver(grafo)
    print('custo: {}, caminho: {}'.format(custo, caminho))
    
    fim_execucao = time.time()  # Captura o tempo de término da execução
    tempo_execucao = fim_execucao - inicio_execucao  # Calcula o tempo de execução em segundos
    
    plot(pontos, caminho)

    print('Tempo de execução: {:.2f} segundos'.format(tempo_execucao))
    print('Semente aleatória usada: {}'.format(random_seed))

if __name__ == '__main__':
    principal()