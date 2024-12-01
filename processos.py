import multiprocessing  # Biblioteca que permite criar e gerenciar processos em Python
import os               # Biblioteca que fornece funcionalidades relacionadas ao sistema operacional
import time             # Biblioteca que permite adicionar atrasos temporais

#Criamos uma função que os processos filhos vão executar.
def tarefa(numero):
    #Cada processo filho vai calcular um quadrado.
    print(f"Processo {os.getpid()} está calculando o quadrado de {numero}. ")
    resultado = numero ** 2
    time.sleep(3)#Simula o tempo de execução do processo.
    print(f"Processo {os.getpid()} terminou: {numero}^2 = {resultado}")
      
#Agora função que cria os processos filhos.
def criar_processos():
    processos = [] #Lista para armazenar os processos filhos
    #Utilizamos o for para criar 3 processo filhos.
    for i in range(1,4):
        p = multiprocessing.Process(target=tarefa, args=(i,)) # Cria um novo processo
        processos.append(p)  # Adiciona o processo à lista
        p.start()  # Inicia o processo filho


    print(f"PID do processo pai: {os.getpid()}")  # Exibe o PID do processo pai

    # Aguarda os processos filhos terminarem
    for p in processos:
        p.join()  # Espera cada processo filho terminar

    print("Todos os processos filhos terminaram.")  # Exibe quando todos os filhos terminaram

# Inicia o processo pai, que vai criar e gerenciar os filhos
if __name__ == "__main__":
    criar_processos()