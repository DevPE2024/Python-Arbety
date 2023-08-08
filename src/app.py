import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from collections import deque
from strat import Strat
from face import FaceGUI
import tkinter as tk
import threading

def start_robot(strategia):
    # Configura as opções do Edge
    options = Options()
    options.add_argument("--headless")
    service = Service(EdgeChromiumDriverManager().install())
    driver = Edge(service=service, options=options)
    
    driver.implicitly_wait(10)
    url = "https://www.arbety.com/games/double"
    driver.get(url)
    html_antigo = driver.page_source
    TAMANHO_MAXIMO = 20
    fila_dados_impressos = deque(maxlen=TAMANHO_MAXIMO)
    
    try:
        while True:
            try:
                # Verifica se os elementos estão presentes na página
                elemento_pai = WebDriverWait(driver, 10).until(
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

                # Adiciona os novos dados à fila
                fila_dados_impressos.extend(dados_atuais[-TAMANHO_MAXIMO:])

                # Chama o método processar_cores para processar as cores e tomar decisões de apostas
                strategia.processar_cores(fila_dados_impressos)

                # Armazena o código HTML atual da página
                html_atual = driver.page_source

                # Verifica se houve mudanças na página
                if html_atual != html_antigo:
                    html_antigo = html_atual
                    driver.refresh()

                # Espera por 15 segundos antes de verificar novamente
                time.sleep(15)

            except NoSuchElementException as e:
                print(e)
                driver.quit()
                break

    except KeyboardInterrupt:
        print("Programa interrompido pelo usuário")
        driver.quit()

def start_gui(strategia):
    root = tk.Tk()
    face_gui = FaceGUI(root, strategia)
    root.mainloop()

if __name__ == "__main__":
    strategia = Strat()
    robot_thread = threading.Thread(target=start_robot, args=(strategia,))
    robot_thread.start()
    start_gui(strategia)
