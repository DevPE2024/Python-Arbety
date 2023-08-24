import tkinter as tk
import queue
import time
import threading
from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Importando a classe Strat aqui para evitar importação cíclica
from strat import Strat


class App:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.strat_instance = Strat(self.message_queue)
        self.face_instance = None

        # Configura as opções do Edge
        options = Options()
        options.add_argument("--headless")

        # Configura o serviço do EdgeDriver
        self.driver = Edge(options=options)
        self.driver.implicitly_wait(10)

    def scrape_data(self):
        url = "https://www.arbety.com/games/double"
        self.driver.get(url)

        # Armazena o código HTML atual da página
        html_antigo = self.driver.page_source

        while True:
            try:
                # Verifica se os elementos estão presentes na página
                elemento_pai = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'items')]"))
                )

                # Executa o código para pegar os elementos filhos
                elementos_filhos = elemento_pai.find_elements(By.XPATH, "./*")

                # Lista para armazenar os dados atuais na página
                dados_atuais = []

                for elemento in elementos_filhos:
                    try:
                        soup = BeautifulSoup(elemento.get_attribute("innerHTML"), "html.parser")
                    except StaleElementReferenceException:
                        print("Elemento obsoleto encontrado. Continuando...")
                        continue

                    div = soup.find("div")
                    if div:
                        cor = div.get("class")[1] if len(div.get("class")) > 1 else None
                        aria_label = div.get("aria-label")
                        numero = div.text
                        if aria_label:
                            data, hora = aria_label.split(", ")
                        else:
                            data, hora = None, None
                        linha_dados = f"Cor: {cor}, Data: {data}, Hora: {hora}, Número: {numero}"
                        dados_atuais.append(linha_dados)

                # Processa os dados usando a Strat
                valor_aposta_ui = float(self.face_instance.bet_value_entry.get())
                self.strat_instance.processar_cores(dados_atuais, valor_aposta_ui)

                # Atualiza a interface gráfica
                if self.face_instance:
                    self.face_instance.update_labels()

                # Armazena o código HTML atual da página
                html_atual = self.driver.page_source

                # Verifica se houve mudanças na página
                if html_atual != html_antigo:
                    html_antigo = html_atual
                    self.driver.refresh()

                # Espera por 15 segundos antes de verificar novamente
                time.sleep(15)

            except NoSuchElementException as e:
                print(e)
                self.driver.quit()
                break


    def update_gui(self):
        if self.face_instance:
            self.face_instance.update_labels()

    def run(self):
        root = tk.Tk()
        # Importando FaceGUI localmente para evitar importação cíclica
        from face import FaceGUI
        self.face_instance = FaceGUI(root, self.strat_instance)
        
        # Usando threading para a raspagem
        scrape_thread = threading.Thread(target=self.scrape_data)
        scrape_thread.start()
        
        root.mainloop()
        scrape_thread.join()  # Aguarda até que o thread seja finalizado

        # Adicionando um método de atualização periódica
        def periodic_update():
            self.update_gui()
            root.after(1000, periodic_update)

        root.after(1000, periodic_update)
        root.mainloop()

        # Certificando-se de fechar o driver quando a GUI é fechada
        self.driver.quit()

        while not self.message_queue.empty():
            print(self.message_queue.get())

if __name__ == "__main__":
    app = App()
    app.run()