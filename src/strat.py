from collections import deque, Counter
from calc import Calc
from cores import Cores
import logging
import time

class Strat:
    def __init__(self, message_queue):
        self.calc = Calc()
        self.lista_cores = deque(maxlen=16)  # Regra 1
        self.saldo_inicial = 50
        self.valor_aposta = self.saldo_inicial
        self.pode_apostar = False
        self.ultima_lista_cores = []
        self.analise_pendente = None
        self.acertos = 0
        self.quantidade_perdas = 0
        self.message_queue = message_queue
        self.cores_instance = Cores()

    @property
    def lucro(self):
        lucro = self.valor_aposta - self.saldo_inicial
        return max(0, lucro)

    def acerto(self, cores):
        padroes = self.cores_instance.get_padrao(self.lista_cores)  # Regra 2
        return padroes.get(cores, None)

    def fazer_aposta(self, cor, valor_aposta_ui):
        # Regra 7 (parte do saldo)
        self.valor_aposta -= valor_aposta_ui  # Deduz o valor da aposta do saldo atual
        if self.valor_aposta >= 0:
            return f"Aposta de {valor_aposta_ui} reais feita na cor {cor}. Saldo atual: {self.valor_aposta}", cor, valor_aposta_ui
        else:
            self.valor_aposta += valor_aposta_ui  # Reverte a dedução
            return "Saldo insuficiente para fazer a aposta.", None, None  # Regra 3


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
        self.print_efficiency()

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
       
    
    def fazer_aposta_decidida(self, valor_aposta_ui):
        if not self.pode_apostar:
            self.message_queue.put("Aguardando mais informações para fazer uma previsão confiável.")
            return "Aguardando mais informações.", None, None

        # Verificação adicional aqui
        predictions_ml = self.calc.predict_color() if self.calc.predict_color() is not None else {}
        final_color_ml = predictions_ml.get('final_color', None)

        # Pega a previsão do modelo baseado em regras
        prediction_rules = self.acerto(tuple(self.get_last_colors()[-3:]))

        # Faz uma votação majoritária para encontrar a previsão mais comum entre todos os modelos
        all_predictions = list(filter(None, [final_color_ml, prediction_rules]))  # remove None

        if all_predictions:
            most_common_prediction, _ = Counter(all_predictions).most_common(1)[0]
            return self.fazer_aposta(most_common_prediction, valor_aposta_ui)
        else:
            self.message_queue.put("Não foi possível fazer uma previsão.")
            return "Não foi possível fazer uma previsão.", None, None


    def print_efficiency(self):
        # Calcula o total de previsões feitas pelo modelo
        total = self.acertos + self.quantidade_perdas
        
        # Calcula a precisão do modelo baseado em regras
        if total > 0:
            precisao = (self.acertos / total) * 100
            self.message_queue.put(f"Precisão do modelo baseado em regras: {precisao:.2f}%")
            print(f"Precisão do modelo baseado em regras: {precisao:.2f}%")
        
        # Calcula a precisão dos modelos de aprendizado de máquina
        for name, score in self.calc.mean_cv_scores.items():
            self.message_queue.put(f"Precisão do modelo {name}: {score * 100:.2f}%")
            print(f"Precisão do modelo {name}: {score * 100:.2f}%")

    def processar_cores(self, fila_dados_impressos, valor_aposta_ui):
        if not fila_dados_impressos:  # Verifica se há dados para processar
            print("Nenhum dado para processar. Aguardando...")
            return

        self.adicionar_dados_e_treinar_modelos(fila_dados_impressos)
        self.atualizar_lista_cores(fila_dados_impressos)

        if self.lista_cores_changed():
            logging.info(f"Cores atuais: {self.lista_cores}")
            self.pode_apostar = True

            if any(self.calc.is_trained.values()):
                prediction = self.calc.predict_color()
                if prediction:
                    logging.info(f"Previsão feita: {prediction['final_color']}, Votos: {prediction['votes']}")
                else:
                    logging.warning("A previsão retornou None.")
            else:
                logging.warning("Nenhum modelo treinado disponível para previsão.")

            self.analisar_e_realizar_aposta(valor_aposta_ui)  # Regras 5 e 6 são tratadas aqui


    def adicionar_dados_e_treinar_modelos(self, fila_dados_impressos):
        for item in fila_dados_impressos:
            self.calc.add_data(item)
        if len(self.calc.data) >= 20:
            self.calc.train_models()

    def atualizar_lista_cores(self, fila_dados_impressos):
        for item in fila_dados_impressos:
            cor = item.split(",")[0].split(":")[1].strip()
            self.lista_cores.append(cor)

    def lista_cores_changed(self):
        current_list = list(self.lista_cores)
        if current_list != self.ultima_lista_cores:
            self.message_queue.put(f"Cores atuais: {current_list}")
            self.ultima_lista_cores = current_list
            return True
        return False

    def analisar_e_realizar_aposta(self, valor_aposta_ui):
        result = self.fazer_aposta_decidida(valor_aposta_ui)
        if len(result) == 3:  # Verifica se o resultado tem três elementos
            _, cor_apostada, _ = result
        else:
            _, cor_apostada, _ = None, None, None

        if self.pode_apostar and cor_apostada:
            resultado_real = self.lista_cores[-1]
            self.aposta(cor_apostada, resultado_real, valor_aposta_ui)

    def realizar_aposta_pendente(self, valor_aposta_ui):
        # Realiza a aposta pendente com a cor analisada anteriormente e o resultado real
        resultado_real = self.lista_cores[-1]
        cor_apostada, _ = self.fazer_aposta(self.analise_pendente, valor_aposta_ui)
        self.aposta(cor_apostada, resultado_real, valor_aposta_ui)

   


