import multiprocessing  # Biblioteca que permite criar e gerenciar processos em Python
import os               # Biblioteca que fornece funcionalidades relacionadas ao sistema operacional
import time             # Biblioteca que permite adicionar atrasos temporais
import math             # Biblioteca que realiza operaçoes matematicas.
import flet as ft       # Bibloteca para criação de interface grafica.

# Define uma função chamada 'tarefa', que realiza operações específicas.
# Parâmetros:
# - numero: Valor numérico usado na operação.
# - operacao: String que define a operação a ser executada.
# - num2, a, b, c: Parâmetros opcionais para complementar as operações.
# - queue: Objeto de fila usado para comunicação entre processos.

def tarefa(numero, operacao, num2=None, a=None, b=None, c=None, queue=None):
   
    # Obtém o identificador único (PID) do processo atual.
    pid = os.getpid()
    
    # Verifica se o objeto 'queue' foi fornecido.
    if queue:
        # Adiciona uma mensagem à fila indicando o PID e a operação em execução.
        queue.put(f"Processo {pid} está executando a operação '{operacao}'.")
    
    # Simula o tempo de execução da tarefa, esperando 2 segundos.
    time.sleep(2)
    
    # Realiza a operação escolhida.
    if operacao == "quadrado":
        resultado = numero ** 2
        # Mensagem para exibir o fim do processo
        # e tambem o resultado da operação.
        mensagem = f"Processo {pid} terminou: {numero}^2 = {resultado}"
    
    elif operacao == "soma":
        resultado = numero + num2
        mensagem = f"Processo {pid} terminou: {numero} + {num2} = {resultado}"
    
    elif operacao == "subtracao":
        resultado = numero - num2
        mensagem = f"Processo {pid} terminou: {numero} - {num2} = {resultado}"
    
    elif operacao == "multiplicacao":
        resultado = numero * num2
        mensagem = f"Processo {pid} terminou: {numero} x {num2} = {resultado}"
    
    elif operacao == "divisao":
        if num2 == 0:
            mensagem = f"Processo {pid} terminou com erro: Divisão por zero indefinida."
        else:
            resultado = numero / num2
            mensagem = f"Processo {pid} terminou: {numero} / {num2} = {resultado}"
    
    elif operacao == "bhaskara":
        delta = (b ** 2) - (4 * a * c)
        if delta < 0:
            mensagem = f"Processo {pid} terminou: Delta negativo, raízes imaginárias."
        else:
            raiz1 = (-b + math.sqrt(delta)) / (2 * a)
            raiz2 = (-b - math.sqrt(delta)) / (2 * a)
            mensagem = f"Processo {pid} terminou: Raízes calculadas = {raiz1}, {raiz2}"
    
    else:
        mensagem = f"Processo {pid} terminou com erro: Operação inválida."

    if queue:
        queue.put(mensagem)
    
#Função para da interface.
def main(page: ft.Page):
    
    #Titulo da janela.
    page.title = "Gerenciador de Processos"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Mensagem que você deseja exibir
    men_bug = """Encontramos alguns bugs relacionados à rolagem da interface. Para garantir uma melhor experiência, recomendamos evitar a criação excessiva de processos, pois isso pode afetar a visibilidade na rolagem, fazendo com que nem todos os processos apareçam corretamente. Estamos trabalhando para corrigir o problema. Agradecemos a compreensão!"""

    # Exibe a mensagem de alerta na interface
    page.add(ft.Text(men_bug, size=14, color=ft.colors.RED))


    def on_column_scroll(e: ft.OnScrollEvent):
        print(
            f"Type: {e.event_type}, pixels: {e.pixels}, min_scroll_extent: {e.min_scroll_extent}, max_scroll_extent: {e.max_scroll_extent}"
        )

    # Criando a coluna para armazenar os resultados
    resultados = ft.Column(
        spacing=10,
        height=500,
        width=500,
        scroll=ft.ScrollMode.ALWAYS,
        on_scroll=on_column_scroll,
    )    


    #Criando quadro de seleção para as operações.
    operacao_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("quadrado"),
            ft.dropdown.Option("soma"),
            ft.dropdown.Option("subtracao"),
            ft.dropdown.Option("multiplicacao"),
            ft.dropdown.Option("divisao"),
            ft.dropdown.Option("bhaskara")
        ],
        label="Escolha a operação",
        on_change=lambda e: atualizar_campos()
    )    
    
    # Cria um campo de entrada de texto para o número de processos.
    # Este campo permite que o usuário insira a quantidade de processos a serem criados.
    num_processos_input = ft.TextField(label="Número de processos", width=200)
    
    

    # Cria um campo de entrada de texto para a posição inicial.
    # Permite ao usuário definir a posição inicial para alguma operação ou cálculo.
    posicao_inicial_input = ft.TextField(label="Posição inicial", width=200)

    # Cria um campo de entrada de texto para o segundo número.
    # Este campo está inicialmente invisível, mas pode ser exibido dependendo do contexto.
    num2_input = ft.TextField(label="Número 2", visible=False, width=200)

    # Cria um campo de entrada de texto para o valor de 'a'.
    # Está configurado como invisível por padrão e pode ser usado em operações específicas.
    a_input = ft.TextField(label="Valor de a", visible=False, width=200)

    # Cria um campo de entrada de texto para o valor de 'b'.
    # Também está invisível inicialmente e será exibido conforme necessário.
    b_input = ft.TextField(label="Valor de b", visible=False, width=200)

    # Cria um campo de entrada de texto para o valor de 'c'.
    # Este campo está invisível e é utilizado em operações avançadas ou específicas.
    c_input = ft.TextField(label="Valor de c", visible=False, width=200)
    
    

    # Função para atualizar os campos visíveis com base na operação selecionada.
    def atualizar_campos():
        # Obtém o valor selecionado no dropdown de operações.
        operacao = operacao_dropdown.value

        # Torna o campo 'num2_input' visível se a operação for soma, subtração, multiplicação ou divisão.
        num2_input.visible = operacao in ["soma", "subtracao", "multiplicacao", "divisao"]

        # Torna os campos 'a_input', 'b_input' e 'c_input' visíveis apenas se a operação for 'bhaskara'.
        a_input.visible = operacao == "bhaskara"
        b_input.visible = operacao == "bhaskara"
        c_input.visible = operacao == "bhaskara"

        # Atualiza a página para refletir as mudanças nos campos visíveis.
        page.update()

    # Função para iniciar os processos com base nos valores fornecidos pelos campos de entrada
    def iniciar_processos(e):
        
        # Limpa os controles que exibem os resultados para preparar uma nova execução
        resultados.controls.clear()
    
        # Lista para armazenar os processos criados
        processos = []
    
        # Cria uma fila para comunicação entre os processos e o processo principal
        queue = multiprocessing.Queue()  # Usada para enviar mensagens entre processos
    
        # Obtém a operação selecionada no dropdown de operações
        operacao = operacao_dropdown.value
    
        # Converte o valor do campo 'Número de processos' para inteiro
        num_processos = int(num_processos_input.value)
    
        # Converte o valor do campo 'Posição inicial' para inteiro
        posicao_inicial = int(posicao_inicial_input.value)
    
        # Obtém o valor de 'Número 2' se o campo estiver visível; caso contrário, define como None
        num2 = int(num2_input.value) if num2_input.visible else None
    
        # Obtém o valor de 'a' se o campo estiver visível; caso contrário, define como None
        a = int(a_input.value) if a_input.visible else None
    
        # Obtém o valor de 'b' se o campo estiver visível; caso contrário, define como None
        b = int(b_input.value) if b_input.visible else None
    
        # Obtém o valor de 'c' se o campo estiver visível; caso contrário, define como None
        c = int(c_input.value) if c_input.visible else None
        
        # Adiciona uma linha divisória para indicar o inicio da execução.
        resultados.controls.append(ft.Text("--------------------------------------------------"))
        
        # Exibe o PID do processo pai
        resultados.controls.append(ft.Text(f"PID do processo pai: {os.getpid()}"))
        
        resultados.controls.append(ft.Text("--------------------------------------------------"))
        
        page.update()

        # Cria e inicia os processos com base no intervalo especificado
        for i in range(posicao_inicial, posicao_inicial + num_processos):
            # Cria um novo processo, atribuindo a função 'tarefa' como alvo.
            # Passa os argumentos necessários para a função: 
            # 'i' como identificador do processo, a operação selecionada, e os parâmetros opcionais.
            p = multiprocessing.Process(target=tarefa, args=(i, operacao, num2, a, b, c, queue))
    
            # Adiciona o processo criado à lista de processos
            processos.append(p)
    
            # Inicia a execução do processo em paralelo
            p.start()
    
            # Envia uma mensagem para a fila indicando que o processo foi iniciado.
        
            # Adiciona uma linha divisória para indicar o inicio da execução.
            queue.put(f"--------------------------------------------------")
        
            # Inclui o PID (identificador do processo) para fins de monitoramento.
            queue.put(f"Iniciando o processo {p.pid}...")
            
            # Adiciona uma linha divisória para indicar o inicio da execução.
            queue.put(f"--------------------------------------------------")
            
        
        # Função para monitorar a fila de mensagens enquanto os processos estão em execução
        def monitorar_fila():
            
            # Continua monitorando enquanto:
            # - Algum processo da lista 'processos' ainda estiver ativo (is_alive retorna True)
            # - Ou ainda existirem mensagens na fila ('queue' não está vazia)
            while any(p.is_alive() for p in processos) or not queue.empty():
        
                # Processa todas as mensagens que estão na fila no momento
                while not queue.empty():
                    # Obtém a próxima mensagem da fila
                    mensagem = queue.get()
            
                    # Adiciona a mensagem ao controle de resultados (exibição na interface)
                    resultados.controls.append(ft.Text(mensagem))
        
                # Aguarda brevemente antes de repetir o loop, reduzindo uso excessivo de CPU
                time.sleep(0.1)
                
        # Chama a função para monitorar a fila de mensagens enquanto os processos estão em execução.
        monitorar_fila()

        # Aguarda a finalização de todos os processos criados.
        # O método 'join()' bloqueia a execução do programa até que o processo correspondente termine.
        for p in processos:
            p.join()

        # Adiciona uma linha divisória para indicar o fim da execução.
        resultados.controls.append(ft.Text("--------------------------------------------------"))

        # Adiciona uma mensagem informando que todos os processos foram concluídos.
        resultados.controls.append(ft.Text("Todos os processos filhos terminaram."))
        
        # Atualiza a interface da página para refletir as mensagens adicionadas.
        page.update()

    # Configuração do layout da interface gráfica do aplicativo
    page.add(
        
        # Adiciona uma coluna que organiza os elementos verticalmente
        ft.Column([
            # Dropdown para seleção de operações
            operacao_dropdown,
        
            # Campo de entrada para o número de processos
            num_processos_input,
        
            # Campo de entrada para a posição inicial
            posicao_inicial_input,
        
            # Campo de entrada para o segundo número (inicialmente invisível)
            num2_input,
        
            # Campos de entrada para os valores 'a', 'b' e 'c' (invisíveis até a operação Bhaskara)
            a_input,
            b_input,
            c_input,
        
            # Botão para iniciar os processos. O método 'on_click' chama a função 'iniciar_processos'.
            ft.ElevatedButton("Iniciar Processos", on_click=iniciar_processos),
            
            # Contêiner para exibir os resultados dos processos
            resultados
        ])
    )

# Protege a execução do código principal, garantindo que ele seja executado apenas se o script
# for chamado diretamente (não importado como um módulo).
if __name__ == "__main__":
    # Inicia o aplicativo Flutter no desktop, chamando a função 'main' como ponto de entrada.
    ft.app(target=main)

