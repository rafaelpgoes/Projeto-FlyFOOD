import matplotlib.pyplot as plt

# Custos fornecidos
custos = [
    8026.564396193624, 7795.669632591321, 8009.177392334522, 7903.795328661095, 7681.45365625258,
    7920.886043455698, 7943.1776494347605, 7782.170498044019, 7681.453656252581, 7826.852439296087,
    7760.213479665802, 7704.415742583886, 7681.749965600122, 7823.041929379201, 7681.453656252581,
    7906.0048289763745, 8000.131867218707, 7896.719493874052, 7906.0048289763745, 7791.37563410007,
    7681.453656252581, 7943.1776494347605, 8096.473650700891, 7791.37563410007, 7760.213479665803,
    7753.496331884781, 7681.453656252581, 7791.37563410007, 7681.45365625258, 7681.453656252581
]

# Média
media = 7837.49

# Criar uma lista de desvios em relação à média
desvios = [custo - media for custo in custos]

# Criar o gráfico de dispersão
plt.figure(figsize=(10, 6))
plt.scatter(range(1, len(custos) + 1), desvios, color='blue', marker='o', label='Desvio em relação à média')

# Configurar rótulos e título
plt.xlabel('Execução')
plt.ylabel('Desvio em relação à média')
plt.title('Desvio em relação à média para cada execução')

# Adicionar uma linha horizontal na média
plt.axhline(y=0, color='red', linestyle='--', label='Média')

# Mostrar a legenda
plt.legend()

# Exibir o gráfico
plt.grid()
plt.show()