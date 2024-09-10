import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
import time
from threading import Thread

# Configurações fixas
TAMANHO_LOTE = 3
TEMPO_ESPERA = 60  # Tempo de espera entre lotes em segundos

# Funções de consulta e leitura de arquivos
def consultar_cnpj(cnpj):
    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao consultar CNPJ {cnpj}: {e}")
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

# Função de preenchimento e progresso
def preencher_informacoes_cnpjs(cnpjs, campos, progress_callback):
    resultados = []
    total_cnpjs = len(cnpjs)
    for i, cnpj in enumerate(cnpjs):
        resultado = ['C'] * len(campos)
        dados = consultar_cnpj(cnpj)
        if dados:
            for j, campo in enumerate(campos):
                if campo in dados:
                    resultado[j] = dados[campo]
        resultados.append(resultado)
        time.sleep(1)
        progress_callback(i + 1, total_cnpjs)
    return resultados

# Funções de seleção de arquivos
def selecionar_arquivo_cnpjs():
    arquivo_cnpjs = filedialog.askopenfilename(title="Selecione o arquivo de CNPJs (apenas números)", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    entrada_cnpjs.delete(0, tk.END)
    entrada_cnpjs.insert(0, arquivo_cnpjs)

def selecionar_arquivo_resultado():
    arquivo_resultado = filedialog.asksaveasfilename(title="Selecione onde salvar os resultados", defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    entrada_resultados.delete(0, tk.END)
    entrada_resultados.insert(0, arquivo_resultado)

# Função de execução da consulta em um novo thread
def executar_consulta():
    nome_arquivo_cnpjs = entrada_cnpjs.get()
    nome_arquivo_resultados = entrada_resultados.get()
    
    if not nome_arquivo_cnpjs or not nome_arquivo_resultados:
        messagebox.showwarning("Aviso", "Selecione os arquivos necessários!")
        return
    
    cnpjs = ler_cnpj(nome_arquivo_cnpjs)
    campos = ['C', 'nome', 'cnpj', 'IE', 'IM', 'uf', 'municipio', 'bairro', 'logradouro', 'numero', 'complemento', 'cep', 'telefone']
    
    total_cnpjs = len(cnpjs)
    total_passos = (total_cnpjs // TAMANHO_LOTE) + (total_cnpjs % TAMANHO_LOTE > 0)
    
    # Tempo total em segundos
    tempo_total = (total_passos - 1) * TEMPO_ESPERA + ((total_cnpjs % TAMANHO_LOTE) or TAMANHO_LOTE)
    
    start_time = time.time()

    def atualizar_progresso():
        elapsed_time = time.time() - start_time
        time_remaining = max(0, tempo_total - elapsed_time)
        progresso_percentual = (1 - (time_remaining / tempo_total)) * 100
        progresso_bar['value'] = progresso_percentual
        minutos, segundos = divmod(time_remaining, 60)
        progresso_bar_text['text'] = f"Tempo restante: {int(minutos):02}:{int(segundos):02}"
        root.update_idletasks()
        if time_remaining > 0:
            root.after(1000, atualizar_progresso)
        else:
            progresso_bar_text['text'] = "100% Concluído"
    
    def atualizar_progresso_lote(atual, total):
        # Atualiza a barra de progresso de acordo com o avanço dos lotes
        progresso_percentual = (atual / total) * 100
        progresso_bar['value'] = progresso_percentual
        root.update_idletasks()
    
    resultados_totais = []  # Inicializa a lista para armazenar todos os resultados
    
    progresso_bar['value'] = 0
    progresso_bar_text['text'] = "Tempo restante: 00:00"
    root.update_idletasks()
    
    atualizar_progresso()

    for i in range(0, total_cnpjs, TAMANHO_LOTE):
        lote_cnpjs = cnpjs[i:i+TAMANHO_LOTE]
        resultados_lote = preencher_informacoes_cnpjs(lote_cnpjs, campos, lambda x, y: atualizar_progresso_lote(x, total_cnpjs))
        resultados_totais.extend(resultados_lote)
        
        # Pausa de espera entre os lotes
        if i + TAMANHO_LOTE < total_cnpjs:
            time.sleep(TEMPO_ESPERA)

    escrever_resultados_em_arquivo(nome_arquivo_resultados, resultados_totais)
    messagebox.showinfo("Sucesso", "Consultas concluídas e resultados salvos!")
    progresso_bar['value'] = 100
    progresso_bar_text['text'] = "100% Concluído"

def executar_consulta_async():
    Thread(target=executar_consulta).start()

# Criação da janela principal
root = ttk.Window(themename="superhero")
root.title("Consulta CNPJs")
root.geometry("1050x350")
root.resizable(False, False)

# Entrada do arquivo de CNPJs
label_cnpjs = ttk.Label(root, text="Arquivo txt com CNPJs por linha (apenas números):", font=("Helvetica", 12))
label_cnpjs.grid(row=0, column=0, padx=15, pady=10, sticky=W)

entrada_cnpjs = ttk.Entry(root, width=50, font=("Helvetica", 12))
entrada_cnpjs.grid(row=0, column=1, padx=15, pady=10)

botao_cnpjs = ttk.Button(root, text="Selecionar", command=selecionar_arquivo_cnpjs)
botao_cnpjs.grid(row=0, column=2, padx=15, pady=10)

# Entrada do arquivo de resultados
label_resultados = ttk.Label(root, text="Salvar resultados em:", font=("Helvetica", 12))
label_resultados.grid(row=1, column=0, padx=15, pady=10, sticky=W)

entrada_resultados = ttk.Entry(root, width=50, font=("Helvetica", 12))
entrada_resultados.grid(row=1, column=1, padx=15, pady=10)

botao_resultados = ttk.Button(root, text="Selecionar", command=selecionar_arquivo_resultado)
botao_resultados.grid(row=1, column=2, padx=15, pady=10)

# Barra de progresso
progresso_bar = ttk.Progressbar(root, orient="horizontal", length=550, mode="determinate")
progresso_bar.grid(row=2, column=0, columnspan=3, pady=20)

# Texto para mostrar o tempo restante
progresso_bar_text = ttk.Label(root, text="Tempo restante: 00:00", font=("Helvetica", 12))
progresso_bar_text.grid(row=3, column=0, columnspan=3)

# Botão de executar
botao_executar = ttk.Button(root, text="Executar Consulta", command=executar_consulta_async)
botao_executar.grid(row=4, column=0, columnspan=3, pady=15)

root.mainloop()
