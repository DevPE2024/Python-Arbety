import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configura as opções do Chrome
options = Options()
options.add_argument("--headless")  # Executa o Chrome em modo headless

# Configura o serviço do ChromeDriver
service = Service(ChromeDriverManager().install())

# Cria uma nova instância do Google Chrome
driver = Chrome(service=service, options=options)

driver.implicitly_wait(10)  # espera até 10 segundos antes de lançar uma NoSuchElementException

url = "https://www.arbety.com/games/double"
driver.get(url)

# Armazena o código HTML atual da página
html_antigo = driver.page_source

while True:
    try:
        # Verifica se os elementos estão presentes na página
        elemento_pai = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'items')]"))
        )

        # Executa o código para pegar os elementos filhos
        elementos_filhos = elemento_pai.find_elements(By.XPATH, "./*")
        for elemento in elementos_filhos:
            soup = BeautifulSoup(elemento.get_attribute('innerHTML'), 'html.parser')
            div = soup.find('div')
            if div:
                cor = div.get('class')[1] if len(div.get('class')) > 1 else None
                aria_label = div.get('aria-label')
                numero = div.text
                if aria_label:
                    data, hora = aria_label.split(", ")
                else:
                    data, hora = None, None
                print(f"Cor: {cor}, Data: {data}, Hora: {hora}, Número: {numero}")

        # Armazena o código HTML atual da página
        html_atual = driver.page_source

        # Verifica se houve mudanças na página
        if html_atual != html_antigo:
            html_antigo = html_atual
            driver.refresh()

        # Espera por 30 segundos antes de verificar novamente
        time.sleep(30)

    except Exception as e:
        print(e)
        driver.quit()
        break