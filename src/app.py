from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Navegue para o site
    page.goto('https://www.arbety.com/games/double')

    while True:
        # Localize o elemento pelo XPath completo
        element_handle = page.wait_for_selector('//*[@id="root"]/div[7]/div/div[2]/main/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div')

        # Extraia o texto do elemento
        element_text = page.evaluate('(element) => element.textContent', element_handle)

        # Divida o texto em partes usando a função split()
        parts = element_text.split('">')

        # Obtenha os valores desejados das partes extraídas
        hora = parts[1]
        numero = parts[2]
        cor = parts[3].split('"')[0]
        data = parts[3].split('aria-label="')[1].split(',')[0]

        # Imprima os valores extraídos
        print("Hora:", hora)
        print("Número:", numero)
        print("Cor:", cor)
        print("Data:", data)

        # Aguarde 5 segundos antes de procurar novamente
        page.wait_for_timeout(5000)

    browser.close()

with sync_playwright() as p:
    run(p)
