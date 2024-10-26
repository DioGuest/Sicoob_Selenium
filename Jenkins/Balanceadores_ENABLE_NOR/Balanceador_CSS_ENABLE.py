

import ctypes
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def executar_processo_CSS_ENABLE(caminho_do_driver, usuario, senha, Numeros):
    result_message = ""  # Inicializa a mensagem de resultado
    
    # Configuração do Service com o caminho do chromedriver
    service = Service(executable_path=caminho_do_driver)
    
    # Configuração do webdriver (sem headless)
    chrome_options = Options()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # # Configuração do webdriver
    # chrome_options = Options()
    # chrome_options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navegar para a página de login
        driver.get("https://10.210.231.242/tmui/login.jsp?msgcode=2&")
      

        # Aguardar e clicar no botão "details-button"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="details-button"]'))
        ).click()

        # Aguardar e clicar no link "proceed-link"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="proceed-link"]'))
        ).click()

        # Inserir senha
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "passwd"))
        ).send_keys(senha)

        # Inserir nome de usuário
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        ).send_keys(usuario)

        # Clicar no botão de login
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        ).click()


        # Verifica se há uma mensagem de erro de autenticação
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="message" and contains(text(), "Login failed")]'))
            )
            result_message = "Falha no login. Verifique suas credenciais."
            return result_message
        except TimeoutException:
            # Continuar se não houver mensagem de erro
            pass


        # Navegar para "Local Traffic"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Local Traffic"))
        ).click()

        # Navegar para "Nodes"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Nodes"))
        ).click()

        # Navegar para "Node List"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Node List"))
        ).click()

        # Selecionar o frame com ID "contentframe"
        driver.switch_to.frame("contentframe")  # Ou use o índice 3 se preferir

        # Encontrar o campo de busca, limpar o campo e inserir o texto em caixa alta
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "search_input"))
        )
        search_input.clear()  # Limpar o campo
        search_input.send_keys(Numeros.upper())  # Inserir texto em caixa alta

        # Clicar no botão de busca
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "search_button"))
        ).click()

        try:
            # Tentar clicar no checkbox
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "checkbox0"))
            ).click()

            # Tentar clicar no botão "forced_offline"
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "enable"))
            ).click()

            result_message = f"(Proces.*HABILITAR*) Maquina: {Numeros} Foi habilitada *ENABLE* no balanceador CSS."  # Mensagem de sucesso

        except TimeoutException:
            result_message = f"(Proces.*HABILITAR*) A Maquina {Numeros} NAO foi encontrada na lista do Balanceador CSS."
    
    finally:
        driver.quit()
        return result_message
