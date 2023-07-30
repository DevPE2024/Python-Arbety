import time
from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException


# Configura as opções do Edge
options = Options()
options.add_argument("--headless")  # Executa o Edge em modo headless

# Configura o serviço do EdgeDriver
service = Service(EdgeChromiumDriverManager().install())

# Cria uma nova instância do Microsoft Edge
driver = Edge(service=service, options=options)

driver.implicitly_wait(
    10
)  # espera até 10 segundos antes de lançar uma NoSuchElementException

url = "https://www.arbety.com/games/double"
driver.get(url)

# Armazena o código HTML atual da página
html_antigo = driver.page_source

# Armazena as linhas de dados já impressas
dados_impressos = set()

try:
    while True:
        try:
            # Verifica se os elementos estão presentes na página
            elemento_pai = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'items')]")
                )
            )

            # Executa o código para pegar os elementos filhos
            elementos_filhos = elemento_pai.find_elements(By.XPATH, "./*")
            for elemento in elementos_filhos:
                soup = BeautifulSoup(elemento.get_attribute("innerHTML"), "html.parser")
                div = soup.find("div")
                if div:
                    cor = div.get("class")[1] if len(div.get("class")) > 1 else None
                    aria_label = div.get("aria-label")
                    numero = div.text
                    if aria_label:
                        data, hora = aria_label.split(", ")
                    else:
                        data, hora = None, None

                    # Monta a linha de dados
                    linha_dados = f"Cor: {cor}, Data: {data}, Hora: {hora}, Número: {numero}"

                    # Verifica se a linha de dados já foi impressa
                    if linha_dados not in dados_impressos:
                        # Se não, imprime a linha de dados, e a adiciona ao conjunto de dados impressos
                        print(linha_dados)
                        dados_impressos.add(linha_dados)

            # Armazena o código HTML atual da página
            html_atual = driver.page_source

            # Verifica se houve mudanças na página
            if html_atual != html_antigo:
                html_antigo = html_atual
                driver.refresh()

            # Espera por 30 segundos antes de verificar novamente
            time.sleep(15)

        except NoSuchElementException as e:
            print(e)
            driver.quit()
            break

except KeyboardInterrupt:
    print("Programa interrompido pelo usuário")
    driver.quit()
