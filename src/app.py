from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configura as opções do Chrome
options = Options()
options.add_argument("--headless")  # Executa o Chrome em modo headless

# Configura o serviço do ChromeDriver
service = Service(ChromeDriverManager().install())

# Cria uma nova instância do Google Chrome
driver = webdriver.Chrome(service=service, options=options)

driver.implicitly_wait(10)  # espera até 10 segundos antes de lançar uma NoSuchElementException

driver.get("https://www.arbety.com/games/double")  # substitua pelo URL correto

elemento_pai = driver.find_element(By.XPATH, "//div[contains(@class, 'items')]")

# Encontrar todos os elementos filhos DIRETOS do elemento pai
elementos_filhos = elemento_pai.find_elements(By.XPATH, "./*")

for elemento in elementos_filhos:
    print(f"Tag: {elemento.tag_name}, Conteúdo: {elemento.text}")

driver.quit()
