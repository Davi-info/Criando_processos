import multiprocessing  # Biblioteca que permite criar e gerenciar processos em Python
import os               # Biblioteca que fornece funcionalidades relacionadas ao sistema operacional
import time             # Biblioteca que permite adicionar atrasos temporais
import math             #Biblioteca que realiza operaçoes matematicas.

#Criamos uma função que os processos filhos vão executar.
#Tambem criação das variaveis a serem utilizadas.
def tarefa(numero, operacao, num2=None, a=None, b=None, c=None):
    print(f"Processo {os.getpid()} está execuntando a operação '{operacao}'.")
    
     # Realiza a operação escolhida
    if operacao == "quadrado":
        resultado = numero ** 2
    elif operacao == "soma":
        resultado = numero + num2
    elif operacao == "subtracao":
        resultado = numero - num2
    elif operacao == "multiplicacao":
        resultado = numero * num2
    elif operacao == "divisao":
        resultado = numero / num2 if num2 != 0 else "Divisão por zero indefinida"
    elif operacao == "bhaskara":
        delta = (b ** 2) - (4 * a * c)
        if delta < 0:
            resultado = "Delta negativo, raízes imaginárias"
        else:
            raiz1 = (-b + math.sqrt(delta)) / (2 * a)
            raiz2 = (-b - math.sqrt(delta)) / (2 * a)
            resultado = f"Raízes: {raiz1} e {raiz2}"
    else:
        resultado = "Operação inválida"
        
    
    time.sleep(2)  # Simula o tempo de execução
    if operacao == "quadrado":
        print(f"Processo {os.getpid()} terminou: {numero}^2 = {resultado}")
        
        print("-" * 50)
        
    elif operacao == "soma":
        print(f"Processo {os.getpid()} terminou: {numero} + {num2} = {resultado}")
        
        print("-" * 50)
        
    elif operacao == "subtracao":
        print(f"Processo {os.getpid()} terminou: {numero} - {num2} = {resultado}")
        
        print("-" * 50)
        
    elif operacao == "multiplicacao":
        print(f"Processo {os.getpid()} terminou: {numero} x {num2} = {resultado}")
        
        print("-" * 50)
        
    elif operacao == "divisao":
        print(f"Processo {os.getpid()} terminou: {numero} / {num2} = {resultado}")
        
        print("-" * 50)
        
    elif operacao == "bhaskara":
        print(f"Processo {os.getpid()} terminou: Raízes calculadas = {resultado}")
        
        print("-" * 50)
        
    else:
        print(f"Processo {os.getpid()} terminou com erro: Operação inválida.")
        
        print("-" * 50)
    
    
    # #Cada processo filho vai calcular um quadrado.
    # print(f"Processo {os.getpid()} está calculando o quadrado de {numero}. ")
    # resultado = numero ** 2
    
    
    # time.sleep(3)#Simula o tempo de execução do processo.
    # print(f"Processo {os.getpid()} terminou: {numero}^2 = {resultado}")
      
#Agora função que cria os processos filhos.
def criar_processos(): 
    
    print("-" * 50)
    
    print(f"PID do processo pai: {os.getpid()}")  # Exibe o PID do processo pai
    
    processos = [] #Lista para armazenar os processos filhos
    
    
    #Escolha das operações.
    print("-" * 50)
    
    print("Escolha a operação que deseja realizar:")
    
    print("-" * 50)
    
    print("1. Quadrado")
    print("2. Soma")
    print("3. Subtração")
    print("4. Multiplicação")
    print("5. Divisão")
    print("6. Bhaskara")
    
    print("-" * 50)
    
    opcao = int(input("Digite o número correspondente à operação: "))
    
    #Trazendo as operações em string.
    operacao = {
        1: "quadrado",
        2: "soma",
        3: "subtracao",
        4: "multiplicacao",
        5: "divisao",
        6: "bhaskara"
    }.get(opcao, "inválida")
    
    #Se operações for diferente sera inválida.
    if operacao == "inválida":
        print("Operação inválida. Tente novamente.")
        return
    
    print("-" * 50)
    
    #Você pode definir quantos processos filhos deseja criar.
    num_processos = int(input("Digite número de processos flihos quer criar: "))
    
    print("-" * 50)
    
    # Posição inicial para a criação dos processos
    posicao_inicial = int(input("Escolha a posição inicial numérica para os processos começarem: "))
    
    print("-" * 50)
   
    
    # Solicitar números ou parâmetros conforme a operação escolhida
    if operacao == "bhaskara":
        a = int(input("Digite o valor de a: "))
        b = int(input("Digite o valor de b: "))
        c = int(input("Digite o valor de c: "))
        
        print("-" * 50)
        
        #Utilizamos o for para adicionar os processos filhos na lista.
        for i in range(1, num_processos + 1):
            p = multiprocessing.Process(target=tarefa, args=(0, operacao, None, a, b, c))# Cria um novo processo
            processos.append(p)# Adiciona o processo à lista
            p.start()
    #Solicitando outros números e operações para escolha. 
    elif operacao in ["soma", "subtracao", "multiplicacao", "divisao"]:
        num2 = int(input("Digite o segundo número: "))
        
        print("-" * 50)
        
        for i in range(posicao_inicial, posicao_inicial + num_processos):
            p = multiprocessing.Process(target=tarefa, args=(i, operacao, num2))# Cria um novo processo
            processos.append(p)# Adiciona o processo à lista
            p.start()# Inicia o processo filho
    elif operacao == "quadrado":
        for i in range(posicao_inicial, posicao_inicial + num_processos):
            p = multiprocessing.Process(target=tarefa, args=(i, operacao))  # Passar a operação
            processos.append(p)  # Adiciona o processo à lista
            p.start()  # Inicia o processo filho
    
    # #Utilizamos o for para criar 3 processo filhos.
    # for i in range(1,4):
    #     p = multiprocessing.Process(target=tarefa, args=(i,)) # Cria um novo processo
    #     processos.append(p)  # Adiciona o processo à lista
    #     p.start()  # Inicia o processo filho

    # Aguarda os processos filhos terminarem
    for p in processos:
        p.join()  # Espera cada processo filho terminar
    
    print("Todos os processos filhos terminaram.")  # Exibe quando todos os filhos terminaram

# Inicia o processo pai, que vai criar e gerenciar os filhos
if __name__ == "__main__":
    criar_processos()