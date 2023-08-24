from collections import deque

class Strat:
    def __init__(self, message_queue):
        self.lista_cores = deque(maxlen=16)
        self.saldo_inicial = 50
        self.valor_aposta = self.saldo_inicial
        self.pode_apostar = False
        self.ultima_lista_cores = []
        self.analise_pendente = None
        self.acertos = 0
        self.quantidade_perdas = 0
        self.message_queue = message_queue

    @property
    def lucro(self):
        lucro = self.valor_aposta - self.saldo_inicial
        return max(0, lucro)  # Para garantir que o lucro nunca seja negativo

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

    def fazer_aposta(self, cor, valor_aposta_ui):
        if self.valor_aposta >= valor_aposta_ui:
            # Removemos a diminuição da banca aqui, pois será gerenciada nos métodos ganho e perda.
            return f"Aposta de {valor_aposta_ui} reais feita na cor {cor}. Saldo atual: {self.valor_aposta}", cor, valor_aposta_ui
        else:
            return "Saldo insuficiente para fazer a aposta.", None, None

    def get_last_colors(self):
        return list(self.lista_cores)

    def ganho(self, cor_vencedora, valor_aposta_ui):
        if cor_vencedora in ['red', 'green']:
            ganho = valor_aposta_ui * 2
        elif cor_vencedora == 'white':
            ganho = valor_aposta_ui * 14
        # A banca é aumentada quando o ganho é processado
        self.valor_aposta += ganho
        self.acertos += 1
        self.message_queue.put(f"WIN - Você Ganhou! Saldo: {self.valor_aposta}")

    def perda(self, valor_aposta_ui):
        # A banca é diminuída quando a perda é processada
        self.valor_aposta -= valor_aposta_ui
        if self.valor_aposta < 0:
            self.valor_aposta = 0
        self.quantidade_perdas += 1
        self.message_queue.put("LOSS - Você Perdeu")
        if self.valor_aposta <= 0:
            self.message_queue.put("Saldo 0, iniciando novamente.")
            self.valor_aposta = self.saldo_inicial

    def aposta(self, cor_aposta, resultado, valor_aposta_ui):
        if resultado == cor_aposta:
            self.ganho(resultado, valor_aposta_ui)
        else:
            self.perda(valor_aposta_ui)

    def verificar_meta(self):
        if self.valor_aposta >= 100:
            self.message_queue.put("Meta batida!")
            return True
        return False
    
    def analisar_cores(self):
        if not self.pode_apostar:
            self.message_queue.put("Aguardando mais cores...")
            return

        for i in range(len(self.lista_cores), 1, -1):
            cores = tuple(list(self.lista_cores)[-i:])
            cor_aposta = self.acerto(cores)

            if cor_aposta:
                self.message_queue.put(f"Encontrado um Padrão.. Padrão encontrado: {cores} -> {cor_aposta}")
                self.analise_pendente = cor_aposta
                break
        else:
            self.message_queue.put("Nenhum padrão encontrado..")
            self.pode_apostar = False
       
    def processar_cores(self, fila_dados_impressos, valor_aposta_ui):
        for item in fila_dados_impressos:
            cor = item.split(",")[0].split(":")[1].strip()
            self.lista_cores.append(cor)

        if list(self.lista_cores) != self.ultima_lista_cores:
            self.message_queue.put(f"Cores atuais: {list(self.lista_cores)}")
            self.ultima_lista_cores = list(self.lista_cores)
            self.pode_apostar = True

            if self.analise_pendente:
                resultado_real = self.lista_cores[-1]
                mensagem, cor_apostada, _ = self.fazer_aposta(self.analise_pendente, valor_aposta_ui)
                self.aposta(cor_apostada, resultado_real, valor_aposta_ui)

            self.analisar_cores()
