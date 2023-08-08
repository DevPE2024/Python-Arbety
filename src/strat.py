from collections import deque

class Strat:
    def __init__(self):
        self.lista_cores = deque(maxlen=10)
        self.valor_aposta = 50
        self.gale_nivel = 0
        self.lista_atualizada = False
        self.valor_aposta_usuario = 0  # Valor da aposta definido pelo usuário
        self.robo_ligado = False  # Status do robô

    def definir_valor_aposta_usuario(self, valor):
        self.valor_aposta_usuario = valor

    def ligar_robo(self):
        self.robo_ligado = True

    def desligar_robo(self):
        self.robo_ligado = False

    def processar_cores(self, fila_dados_impressos):
        # Verificar as condições
        if not self.robo_ligado:
            print("Robô desligado. Ligue o robô para iniciar as apostas.")
            return
        if self.valor_aposta <= 0:
            print("Saldo insuficiente. Adicione saldo para iniciar as apostas.")
            return
        if self.valor_aposta_usuario <= 0:
            print("Defina o valor da aposta para iniciar as apostas.")
            return
        
    def acerto(self, cores):
        padroes = {
            ('red', 'green', 'red'): 'green',
            ('green', 'red', 'green'): 'red',
            ('green', 'red', 'red', 'green'): 'red',
            ('red', 'green', 'green', 'red'): 'green',
            ('red', 'red'): 'red',
            ('green', 'green',): 'green',
            ('green', 'white', 'green'): 'green',
        }
        return padroes.get(cores, None)

    def fazer_aposta(self, cor):
        valor_aposta = 10
        if self.valor_aposta >= valor_aposta:
            self.valor_aposta -= valor_aposta
            print(f"Aposta de {valor_aposta} reais feita na cor {cor}. Saldo atual: {self.valor_aposta}")
            return cor
        else:
            print("Saldo insuficiente para fazer a aposta.")
            return None

    def ganho(self, cor_aposta):
        ganho = 10
        if cor_aposta == 'green':
            ganho *= 2
        elif cor_aposta == 'red':
            ganho *= 2
        elif cor_aposta == 'white':
            ganho *= 14
        self.valor_aposta += ganho
        print(f"WIN - Você Ganhou! Saldo: {self.valor_aposta}")
        self.verificar_meta()


    def perda(self):
        print("LOSS - Você Perdeu")
        perda = 10
        self.gale_nivel += 1

        if self.gale_nivel == 1:
            print("Entrando em GALE 1")
            perda *= 2
        elif self.gale_nivel == 2:
            print("Entrando em GALE 2")
            perda *= 4

        self.valor_aposta -= perda

        if self.gale_nivel > 2:
            print("Guardando o dinheiro e aguardando a próxima avaliação")
            self.gale_nivel = 0

        if self.valor_aposta <= 0:
            print("Saldo 0, iniciando nova aposta")
            self.valor_aposta = 50

        self.verificar_meta()


    def aposta(self, cor_aposta, resultado):
        ganhou = resultado == cor_aposta
        if ganhou:
            self.ganho(cor_aposta)
        else:
            self.perda()

    def verificar_meta(self):
        meta = 150
        if self.valor_aposta >= meta:
            print("Meta alcançada!")

    def analisar_cores(self):
        print("Iniciando análise das cores para iniciar as apostas")
        
        for i in range(4, 1, -1):
            cores = tuple(list(self.lista_cores)[-i:])
            cor_aposta = self.acerto(cores)
        
            if cor_aposta:
                print("Encontrado um Padrão..", f"Padrão encontrado: {cores} -> {cor_aposta}", "Vamos iniciar as apostas..")
                resultado = self.fazer_aposta(cor_aposta)
                self.aposta(cor_aposta, resultado)
                break
        else:
            print("Analisando...")


    def processar_cores(self, fila_dados_impressos):
        if not self.lista_atualizada and len(self.lista_cores) >= 10:
            self.lista_atualizada = True
            print("A lista foi atualizada, aguardando próxima atualização para começar a apostar.")
            return

        for item in fila_dados_impressos:
            cor = item.split(",")[0].split(":")[1].strip()
            self.lista_cores.append(cor)

        if len(self.lista_cores) > 10:
            self.lista_cores = deque(list(self.lista_cores)[-10:], maxlen=10)

        if len(self.lista_cores) < 10:
            print("Aguardando mais cores...")
            return

        self.analisar_cores()
        print("Cores atuais:", list(self.lista_cores))
        print("Saldo:", self.valor_aposta)

    
