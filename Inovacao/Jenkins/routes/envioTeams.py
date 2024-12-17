# import os
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from dotenv import load_dotenv
# import os


# # Carrega as variáveis do arquivo .env
# load_dotenv()

# Variavel_Ambiente_DRIVER = os.getenv('Variavel_Ambiente_DRIVER')

# # Caminho completo para o chromedriver
# caminho_do_driver = Variavel_Ambiente_DRIVER
# # Função para configurar o driver do Selenium
# def configurar_driver():
#     service = Service(executable_path=caminho_do_driver)
#     driver = webdriver.Chrome(service=service)
#     return driver

# # Função para fazer login no Microsoft Teams Web
# def login_teams(driver, email, senha):
#     # Acesse o Teams Web
#     driver.get("https://teams.microsoft.com")

#     # Espera o campo de login carregar
#     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "i0116")))

#     # Inserir o e-mail
#     campo_email = driver.find_element(By.ID, "i0116")
#     campo_email.send_keys(email)
#     campo_email.send_keys(Keys.RETURN)

#     # Aguardar o campo de senha
#     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "i0118")))
#     campo_senha = driver.find_element(By.ID, "i0118")
#     campo_senha.send_keys(senha)
#     campo_senha.send_keys(Keys.RETURN)

#     # Aguardar o login completar
#     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "app-launcher")))

# # Função para buscar o CSV mais recente na raiz do projeto
# def encontrar_csv_mais_recente():
#     arquivos = [f for f in os.listdir() if f.endswith('.csv')]  # Listar todos os arquivos CSV na raiz
#     if not arquivos:
#         print("Nenhum arquivo CSV encontrado.")
#         return None

#     # Encontrar o arquivo mais recente com base na data de modificação
#     arquivo_mais_recente = max(arquivos, key=lambda f: os.path.getmtime(f))
#     return arquivo_mais_recente

# # Função para ler os dados do CSV
# def ler_dados_csv(nome_arquivo):
#     dados = []
#     with open(nome_arquivo, mode="r", encoding="utf-8") as arquivo_csv:
#         leitor = csv.reader(arquivo_csv)
#         next(leitor)  # Pular cabeçalho
#         for linha in leitor:
#             dados.append(" | ".join(linha))  # Formato da linha do CSV
#     return dados

# # Função para enviar as informações do CSV para o Teams
# def enviar_para_teams(driver, grupo_nome, dados_csv):
#     # Navega até o grupo ou canal
#     grupo = driver.find_element(By.XPATH, f"//span[text()='{grupo_nome}']")
#     grupo.click()

#     # Espera a caixa de mensagem carregar
#     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "msgInput")))

#     # Localiza a caixa de mensagem no Teams
#     caixa_mensagem = driver.find_element(By.CLASS_NAME, "msgInput")

#     # Insere a mensagem na caixa de entrada
#     mensagem = "\n".join(dados_csv)  # Junta os dados com uma quebra de linha
#     caixa_mensagem.send_keys(mensagem)

#     # Envia a mensagem
#     caixa_mensagem.send_keys(Keys.RETURN)

# # Função principal para executar o processo
# def main():
#     # Configurar o driver
#     driver = configurar_driver()

#     # Definir suas credenciais do Teams
#     email = "Diogo.Soares@fornecedores.sicoob.com.br"
#     senha = "Francielle!123"
    
#     # Login no Teams Web
#     login_teams(driver, email, senha)

#     # Encontrar o arquivo CSV mais recente
#     nome_arquivo_csv = encontrar_csv_mais_recente()
#     if nome_arquivo_csv is None:
#         driver.quit()
#         return  # Se não encontrar um CSV, sai da função

#     # Ler os dados do CSV gerado
#     dados_csv = ler_dados_csv(nome_arquivo_csv)

#     # Definir o nome do grupo/canal no Teams onde as mensagens serão enviadas
#     grupo_nome = "Thiago Goncalves Deodato"

#     # Enviar os dados para o grupo do Teams
#     enviar_para_teams(driver, grupo_nome, dados_csv)

#     # Fechar o driver após o envio
#     driver.quit()





import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

Variavel_Ambiente_DRIVER = os.getenv('Variavel_Ambiente_DRIVER')

# Caminho completo para o chromedriver
caminho_do_driver = Variavel_Ambiente_DRIVER

# Função para configurar o driver do Selenium
def configurar_driver():
    chrome_options = Options()
    # Altera o User-Agent para um agente de usuário comum
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
    # Desabilita a detecção de automação
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # Oculta o modo de automação
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(executable_path=caminho_do_driver)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Executa comandos para remover detecção de automação após inicializar o driver
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        },
    )
    return driver

# Função para fazer login no Microsoft Teams Web
def login_teams(driver, email, senha):
    # Acesse o Teams Web
    driver.get("https://teams.microsoft.com")

    # Espera o campo de login carregar
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "i0116")))

    # Inserir o e-mail
    campo_email = driver.find_element(By.ID, "i0116")
    campo_email.send_keys(email)
    campo_email.send_keys(Keys.RETURN)

    # Aguardar o campo de senha
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "i0118")))
    campo_senha = driver.find_element(By.ID, "i0118")
    campo_senha.send_keys(senha)
    campo_senha.send_keys(Keys.RETURN)

    # Aguardar o login completar
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "app-launcher")))

# Função para buscar o CSV mais recente na raiz do projeto
def encontrar_csv_mais_recente():
    arquivos = [f for f in os.listdir() if f.endswith('.csv')]  # Listar todos os arquivos CSV na raiz
    if not arquivos:
        print("Nenhum arquivo CSV encontrado.")
        return None

    # Encontrar o arquivo mais recente com base na data de modificação
    arquivo_mais_recente = max(arquivos, key=lambda f: os.path.getmtime(f))
    return arquivo_mais_recente

# Função para ler os dados do CSV
def ler_dados_csv(nome_arquivo):
    dados = []
    with open(nome_arquivo, mode="r", encoding="utf-8") as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor)  # Pular cabeçalho
        for linha in leitor:
            dados.append(" | ".join(linha))  # Formato da linha do CSV
    return dados

# Função para enviar as informações do CSV para o Teams
def enviar_para_teams(driver, grupo_nome, dados_csv):
    # Navega até o grupo ou canal
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//span[text()='{grupo_nome}']")))
    grupo = driver.find_element(By.XPATH, f"//span[text()='{grupo_nome}']")
    grupo.click()

    # Espera a caixa de mensagem carregar
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "msgInput")))

    # Localiza a caixa de mensagem no Teams
    caixa_mensagem = driver.find_element(By.CLASS_NAME, "msgInput")

    # Insere a mensagem na caixa de entrada
    mensagem = "\n".join(dados_csv)  # Junta os dados com uma quebra de linha
    caixa_mensagem.send_keys(mensagem)

    # Envia a mensagem
    caixa_mensagem.send_keys(Keys.RETURN)

# Função principal para executar o processo
def main():
    # Configurar o driver
    driver = configurar_driver()

    # Definir suas credenciais do Teams
    email = "Diogo.Soares@fornecedores.sicoob.com.br"
    senha = "Francielle!123"
    
    # Login no Teams Web
    login_teams(driver, email, senha)

    # Encontrar o arquivo CSV mais recente
    nome_arquivo_csv = encontrar_csv_mais_recente()
    if nome_arquivo_csv is None:
        driver.quit()
        return  # Se não encontrar um CSV, sai da função

    # Ler os dados do CSV gerado
    dados_csv = ler_dados_csv(nome_arquivo_csv)

    # Definir o nome do grupo/canal no Teams onde as mensagens serão enviadas
    grupo_nome = "Thiago Goncalves Deodato"

    # Enviar os dados para o grupo do Teams
    enviar_para_teams(driver, grupo_nome, dados_csv)

    # Fechar o driver após o envio
    driver.quit()

if __name__ == "__main__":
    main()
