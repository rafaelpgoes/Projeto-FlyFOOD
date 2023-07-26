import time

# Função que calcula a distância entre dois pontos no plano cartesiano usando a métrica de "taxicab"
def distancia(p1, p2):
    dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return dist

# Função que calcula a distância total de um percurso, considerando a volta ao ponto inicial (restaurante)
def dist_percurso(percurso):
    d = 0
    for i in range(1, len(percurso)):
        d += distancia(percurso[i - 1], percurso[i])
    # Considerar a volta ao restaurante R
    d += distancia(percurso[-1], percurso[0])
    return d

# Função que gera todas as permutações possíveis dos pontos de entrega fornecidos como parâmetro
def permutar(pontos_de_entrega):
    if len(pontos_de_entrega) <= 1:
        return [pontos_de_entrega]
    permutacoes = []
    for i, ponto_atual in enumerate(pontos_de_entrega):
        pontos_restantes = pontos_de_entrega[:i] + pontos_de_entrega[i+1:]
        for permutacao in permutar(pontos_restantes):
            permutacoes.append([ponto_atual] + permutacao)
    return permutacoes

# Função que lê a matriz de entrada do usuário
def ler_matriz():
    linhas, colunas = map(int, input().split())
    matriz = []
    for _ in range(linhas):
        linha = input().split()
        matriz.append(linha)
    return matriz

# Função que encontra os pontos de entrega na matriz de entrada
def encontrar_pontos_de_entrega(matriz):
    pontos_de_entrega = []
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] != '0' and matriz[i][j] != 'R':
                pontos_de_entrega.append((i, j))
    return [(0, 0)] + pontos_de_entrega + [(0, 0)]

# Início da medição do tempo de execução
inicio_execucao = time.time()

# Leitura da matriz de entrada e identificação dos pontos de entrega
entrada_matriz = ler_matriz()
pontos_de_entrega = encontrar_pontos_de_entrega(entrada_matriz)

# Usamos diretamente a matriz de entrada como rótulos
rotulos = entrada_matriz

# Inicialização das variáveis para encontrar o menor percurso
menor = float("inf")
menor_percurso = None

# Geração de todas as permutações dos pontos de entrega e busca do menor percurso
for i in permutar(pontos_de_entrega):
    dist = dist_percurso(i)
    if dist < menor:
        menor = dist
        menor_percurso = i

# Remoção do ponto "restaurante" do resultado final para exibição
menor_percurso = [ponto for ponto in menor_percurso if ponto != (0, 0)]

# Inclusão do restaurante no início e no final do percurso
menor_percurso = [(0, 0)] + menor_percurso + [(0, 0)]

# Obtendo os rótulos dos pontos de entrega no percurso e substituindo "0" por "R"
percurso_com_rotulos = [rotulos[ponto[0]][ponto[1]] if rotulos[ponto[0]][ponto[1]] != '0' else 'R' for ponto in menor_percurso]

# Exibição do resultado final
print(f"Menor percurso foi {percurso_com_rotulos} com a distância de {menor} dronômetros")

# Fim da medição do tempo de execução
fim_execucao = time.time()

# Cálculo do tempo total de execução
tempo_total = fim_execucao - inicio_execucao
print(f"Tempo total de execução: {tempo_total:.5f} segundos")