from collections import deque
from math import e

class Strat:
    def __init__(self, message_queue):
        self.lista_cores = deque(maxlen=16)
        self.valor_aposta = 50
        self.pode_apostar = False
        self.ultima_lista_cores = []
        self.analise_pendente = None
        self.acertos = 0
        self.perdas = 0
        self.message_queue = message_queue

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
            return f"Aposta de {valor_aposta} reais feita na cor {cor}. Saldo atual: {self.valor_aposta}", cor, valor_aposta
        else:
            return "Saldo insuficiente para fazer a aposta.", None, None
    
    def get_last_colors(self):
        cores = list(self.lista_cores)
        return cores


    def ganho(self, cor_vencedora):
        ganho = self.valor_aposta
        if cor_vencedora in ['red', 'green']:
            ganho *= 2
        elif cor_vencedora == 'white':
            ganho *= 14
        self.valor_aposta += ganho
        self.acertos += 1
        self.message_queue.put(f"WIN - Você Ganhou! Saldo: {self.valor_aposta}")

    def perda(self):
        self.perdas += 1
        self.message_queue.put("LOSS - Você Perdeu")
        self.valor_aposta -= self.valor_aposta
        if self.valor_aposta <= 0:
            self.message_queue.put("Saldo 0, iniciando novamente.")
            self.valor_aposta = 50

    def aposta(self, cor_aposta, resultado):
        if resultado == cor_aposta:
            self.ganho(resultado)
        else:
            self.perda()

    def verificar_meta(self):
        if self.valor_aposta >= 100:
            self.message_queue.put("Meta batida!")
            return True
        return False
    
    def analisar_cores(self):
        if not self.pode_apostar:
            self.message_queue.put("Aguardando mais cores...")
            return

        for i in range(len(self.lista_cores), 1, -1):  # Ajuste aqui
            cores = tuple(list(self.lista_cores)[-i:])  # Pega os �ltimos 'i' elementos da lista
            cor_aposta = self.acerto(cores)

            if cor_aposta:
                self.message_queue.put(f"Encontrado um Padrão.. Padrão encontrado: {cores} -> {cor_aposta}")
                self.analise_pendente = cor_aposta
                break
        else:
            self.message_queue.put("Nenhum padrão encontrado..")
            self.pode_apostar = False
       
    def processar_cores(self, fila_dados_impressos):
        
        for item in fila_dados_impressos:
            cor = item.split(",")[0].split(":")[1].strip()
            self.lista_cores.append(cor)

        novas_cores = [item.split(",")[0].split(":")[1].strip() for item in fila_dados_impressos]
        for cor in novas_cores:
            if cor not in self.lista_cores:
                self.lista_cores.append(cor)

        if list(self.lista_cores) != self.ultima_lista_cores:
            self.message_queue.put(f"Cores atuais: {list(self.lista_cores)}")
            self.ultima_lista_cores = list(self.lista_cores)
            self.pode_apostar = True

            if self.analise_pendente:
                resultado_real = self.lista_cores[-1]
                self.message_queue.put("Vamos iniciar as apostas..")
                mensagem, cor_apostada, valor_aposta = self.fazer_aposta(self.analise_pendente)
                self.aposta(cor_apostada, resultado_real)
                self.analise_pendente = None

            self.analisar_cores()
