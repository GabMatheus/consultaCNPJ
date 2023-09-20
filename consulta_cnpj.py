import requests
import time

def consultar_cnpj(cnpj):
    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def ler_cnpj(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        cnpjs = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    return cnpjs

def escrever_resultados_em_arquivo(nome_arquivo, resultados):
    with open(nome_arquivo, 'w') as arquivo:
        for resultado in resultados:
            linha = ';'.join(resultado)
            arquivo.write(f'{linha}\n')

def preencher_informacoes_cnpjs(cnpjs, campos):
    resultados = []
    for cnpj in cnpjs:
        resultado = ['C'] * len(campos)
        dados = consultar_cnpj(cnpj)
        if dados:
            for i, campo in enumerate(campos):
                if campo in dados:
                    resultado[i] = dados[campo]
        resultados.append(resultado)
        time.sleep(1)  # Adiciona um intervalo de 1 segundo entre as consultas
    return resultados

# Nome do arquivo contendo a lista de CNPJs
nome_arquivo_cnpjs = 'cnpjs.txt'

# Nome do arquivo para salvar os resultados
nome_arquivo_resultados = 'resultados.txt'

# Ler os CNPJs do arquivo
cnpjs = ler_cnpj(nome_arquivo_cnpjs)
campos = ['Dados', 'nome', 'cnpj', 'IE', 'IM', 'uf', 'municipio', 'bairro', 'logradouro', 'numero', 'complemento', 'cep', 'telefone']

# Definir o tamanho do lote
tamanho_lote = 3

# Definir o tempo de espera entre lotes (1 minuto = 60 segundos)
tempo_espera = 60

# Preencher as informações dos CNPJs em lotes
resultados_totais = []
for i in range(0, len(cnpjs), tamanho_lote):
    lote_cnpjs = cnpjs[i:i+tamanho_lote]
    resultados_lote = preencher_informacoes_cnpjs(lote_cnpjs, campos)
    resultados_totais.extend(resultados_lote)
    if i + tamanho_lote < len(cnpjs):
        time.sleep(tempo_espera)

# Exibir os resultados
for resultado in resultados_totais:
    print(resultado)

# Salvar os resultados em arquivo
escrever_resultados_em_arquivo(nome_arquivo_resultados, resultados_totais)

