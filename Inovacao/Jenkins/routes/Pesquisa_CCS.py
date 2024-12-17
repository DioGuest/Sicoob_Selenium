

import csv
from datetime import datetime
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import jsonify  # Adicione jsonify aqui


from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

Variavel_Ambiente_DRIVER = os.getenv('Variavel_Ambiente_DRIVER')

# Caminho completo para o chromedriver
caminho_do_driver = Variavel_Ambiente_DRIVER

logger = logging.getLogger(__name__)


import requests
import logging

# Configuração do logger
logger = logging.getLogger(__name__)






def obter_host_do_cluster(nome_cluster):
    url = "https://delivery.sicoob.com.br/sicoob-entrega-continua/configuracoes-clusters?count=1000&page=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for cluster in data["resultado"]["dados"]:
            if cluster.get("nomeCluster") == nome_cluster:
                # Verifica se há hosts disponíveis
                hosts = cluster.get("hosts", [])
                if hosts:  # Se houver hosts
                    # Retorna o hostname do primeiro host que estiver no ambiente "PRODUCAO"
                    for host in hosts:
                        if host.get("ambiente") == "PRODUCAO":
                            hostname = host.get("hostname")  # Extrai o hostname
                            logger.info(f"Host encontrado: {hostname}")
                            return hostname  # Retorna apenas o hostname
                else:
                    logger.warning(f"Nenhum host encontrado para o cluster: {nome_cluster}")
                    return None  # Retorna None se não houver hosts

        logger.warning(f"Nenhum host encontrado para o cluster: {nome_cluster}")
    else:
        logger.error(f"Erro ao obter hosts: {response.status_code} - {response.text}")
    
    return None  # Retorna None se não encontrar o cluster ou o ambiente "PRODUCAO"
 

from concurrent.futures import ThreadPoolExecutor, as_completed



def submit():
    username = "adm-diogo.soares"
    password = "+@FtKmUNJIEeAn2u"
    selected_clusters = ["BackofficeCOBCluster", "BackofficeCOBADMCluster", "BackofficeCobAPICluster", "BackofficeCCOCluster", "BackofficeRiscoLimiteCluster", "BackofficeEmpresarialCluster", "BackofficeSegurosCluster", "BackofficeCapesCluster", "BackofficeCreditoCluster", "BackofficeCreditoCoreCluster", "BackofficeInstitucionalCluster"]  # Lista de clusters selecionados
    limpar_dados_csv()
    resultados = {}
    mensagem_erro = ""

    # Dicionário de URLs e nomes dos balanceadores
    balanceadores = {
        "https://10.210.231.242/tmui/login.jsp": "Balanceador: CCS",
        "https://10.100.125.241/tmui/login.jsp": "Balanceador: CYOI",
        "https://bigp2006.sicoob.com.br/tmui/login.jsp": "Balanceador: 2006",
        "https://bigp4006.sicoob.com.br/tmui/login.jsp": "Balanceador: 4006",
        "https://bigp2007.sicoob.com.br/tmui/login.jsp": "Balanceador: 2007",
        "https://bigp4007.sicoob.com.br/tmui/login.jsp": "Balanceador: 4007",
    }

    def task(cluster, url, nome_link):
        try:
            host = obter_host_do_cluster(cluster)
            if host:
                # Passa o cluster para acessar_pool_members
                return f"{cluster} em {nome_link}", acessar_pool_members(host, username, password, url, nome_link, cluster)
            else:
                return f"Nenhum host encontrado para o cluster {cluster}.", None
        except Exception as e:
            return f"Erro ao acessar o cluster {cluster}: {str(e)}", None

    with ThreadPoolExecutor() as executor:
        futures = []
        for cluster in selected_clusters:
            for url in balanceadores.keys():
                nome_link = balanceadores[url]
                futures.append(executor.submit(task, cluster, url, nome_link))



# Função para limpar o arquivo CSV
def limpar_dados_csv(nome_arquivo="pool_members.csv"):
    try:
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(["Cluster", "Nome do Link", "Servidor/Porta", "Status", "Coluna 2"])  # Cabeçalho padrão
        print(f"Arquivo '{nome_arquivo}' limpo com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao limpar o arquivo CSV: {e}")
        print(f"Erro ao limpar o arquivo CSV: {e}")


# def acessar_pool_members(host, login, senha, url, nome_link, cluster):
#     # Configuração do driver
#     service = Service(executable_path=caminho_do_driver)
#     navegador = webdriver.Chrome(service=service)
    
#     host = host.upper()  # Garantir que o host esteja em maiúsculas
#     dados_csv = []  # Armazenar dados para o CSV
#     try:
#         # Acessando a página de login
#         navegador.get(url)
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="details-button"]'))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="proceed-link"]'))).click()

#         # Fazendo login
#         navegador.find_element(By.ID, "username").send_keys(login)
#         navegador.find_element(By.ID, "passwd").send_keys(senha)
#         navegador.find_element(By.CSS_SELECTOR, "button:nth-child(5)").click()

#         # Navegando até a lista de nodes
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Local Traffic"))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Nodes"))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Node List"))).click()

#         navegador.switch_to.frame("contentframe")

#         # Pesquisar o host
#         search_input = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "search_input")))
#         search_input.clear()
#         search_input.send_keys(host)
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.NAME, "search_button"))).click()

#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, host))).click()
#         navegador.switch_to.parent_frame()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Pool Membership"))).click()
#         navegador.switch_to.frame("contentframe")

#         # Coletando os links para os membros do pool
#         pool_links = WebDriverWait(navegador, 10).until(
#             EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
#         )

#         link_9443 = next((link for link in pool_links if link.text.endswith("9443")), None)
#         link_9810 = next((link for link in pool_links if link.text.endswith("9810")), None)
#         link_9843 = next((link for link in pool_links if link.text.endswith("9843")), None)

#         if link_9443:
#             link_9443.click()
#         elif link_9810:
#             link_9810.click()
#         elif link_9843:
#             link_9843.click()
#         else:
#             print("Nenhum link desejado encontrado.")

#         navegador.switch_to.parent_frame()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Members"))).click()
#         navegador.switch_to.frame("contentframe")

#         # Coletando a tabela de membros
#         tabela = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='list_body']")))

#         linhas = tabela.find_elements(By.TAG_NAME, "tr")

#         for linha in linhas:
#             colunas = linha.find_elements(By.TAG_NAME, "td")
#             if len(colunas) < 3:
#                 continue  # Ignorar linhas com dados insuficientes

#             checkbox_value = colunas[0].find_element(By.TAG_NAME, 'input').get_attribute('value')
#             status_info = colunas[1].find_elements(By.TAG_NAME, "img")[0].get_attribute("title") if colunas[1].find_elements(By.TAG_NAME, "img") else "N/A"
#             link_text = colunas[2].find_element(By.TAG_NAME, "a").text

#             # Adiciona os dados ao CSV (incluindo o cluster e nome do balanceador)
#             dados_csv.append([cluster, nome_link, checkbox_value, status_info, link_text])

#         # # Escrever os dados em um arquivo CSV
#         # nome_arquivo = "pool_members.csv"
#         # with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as arquivo_csv:
#         #     escritor = csv.writer(arquivo_csv)
#         #     if arquivo_csv.tell() == 0:  # Escrever cabeçalho se o arquivo estiver vazio
#         #         escritor.writerow(["Cluster", "Nome do Link", "Coluna 0", "Status", "Coluna 2"])
#         #     escritor.writerows(dados_csv)
#         # Obter a data e hora atuais no formato desejado
#         # Obter a data e hora atuais no formato desejado
#         # Obter a data e hora atual sem os segundos
#         # Obter a data e hora da execução no formato: YYYY-MM-DD_HH-MM


#         # data_hora_execucao = datetime.now().strftime("%Y-%m-%d_%H-%M")
#         # nome_arquivo = f"pool_members_{data_hora_execucao}.csv"
#         # Escrever os dados em um arquivo CSV
#         nome_arquivo = "pool_members.csv"  # Nome fixo para o arquivo

#         # Escrever os dados em um arquivo CSV
#         with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as arquivo_csv:
#             escritor = csv.writer(arquivo_csv)
#             if arquivo_csv.tell() == 0:  # Escrever cabeçalho se o arquivo estiver vazio
#                 escritor.writerow(["Cluster", "Nome do Link", "Coluna 0", "Status", "Coluna 2"])
#             escritor.writerows(dados_csv)

#         print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso.")


#         # # Escrever os dados em um arquivo CSV
#         # nome_arquivo = "pool_members.csv"  # Nome fixo para o arquivo

#         # # Escrever os dados no arquivo CSV, sobrescrevendo-o a cada execução
#         # with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
#         #     escritor = csv.writer(arquivo_csv)
#         #     escritor.writerow(["Cluster", "Nome do Link", "Coluna 0", "Status", "Coluna 2"])  # Escrever cabeçalho
#         #     escritor.writerows(dados_csv)

#         # print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso.")

#         return "Processo concluído. CSV gerado com sucesso."
    
#     except Exception as e:
#         print(f"Erro ao acessar a página: {str(e)}")
#         return f"Erro ao acessar a página: {str(e)}"
    
#     finally:
#         navegador.quit()








# #offline arrumado
# def acessar_pool_members(host, login, senha, url, nome_link, cluster):
#     # Configuração do driver
#     service = Service(executable_path=caminho_do_driver)
#     navegador = webdriver.Chrome(service=service)
    
#     host = host.upper()  # Garantir que o host esteja em maiúsculas
#     dados_csv = []  # Armazenar dados para o CSV
#     try:
#         # Acessando a página de login
#         navegador.get(url)
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="details-button"]'))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="proceed-link"]'))).click()

#         # Fazendo login
#         navegador.find_element(By.ID, "username").send_keys(login)
#         navegador.find_element(By.ID, "passwd").send_keys(senha)
#         navegador.find_element(By.CSS_SELECTOR, "button:nth-child(5)").click()

#         # Navegando até a lista de nodes
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Local Traffic"))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Nodes"))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Node List"))).click()

#         navegador.switch_to.frame("contentframe")

#         # Pesquisar o host
#         search_input = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "search_input")))
#         search_input.clear()
#         search_input.send_keys(host)
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.NAME, "search_button"))).click()

#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, host))).click()
#         navegador.switch_to.parent_frame()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Pool Membership"))).click()
#         navegador.switch_to.frame("contentframe")

#         # Coletando os links para os membros do pool
#         pool_links = WebDriverWait(navegador, 10).until(
#             EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
#         )

#         link_9443 = next((link for link in pool_links if link.text.endswith("9443")), None)
#         link_9810 = next((link for link in pool_links if link.text.endswith("9810")), None)
#         link_9843 = next((link for link in pool_links if link.text.endswith("9843")), None)

#         if link_9443:
#             link_9443.click()
#         elif link_9810:
#             link_9810.click()
#         elif link_9843:
#             link_9843.click()
#         else:
#             print("Nenhum link desejado encontrado.")

#         navegador.switch_to.parent_frame()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Members"))).click()
#         navegador.switch_to.frame("contentframe")

#         # Coletando a tabela de membros
#         tabela = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='list_body']")))

#         linhas = tabela.find_elements(By.TAG_NAME, "tr")

#         for linha in linhas:
#             colunas = linha.find_elements(By.TAG_NAME, "td")
#             if len(colunas) < 3:
#                 continue  # Ignorar linhas com dados insuficientes

#             checkbox_value = colunas[0].find_element(By.TAG_NAME, 'input').get_attribute('value')
            
#             # Alterar o status para 'Offline' se o texto contiver 'Offline (Disabled Parent)'
#             status_info = colunas[1].find_elements(By.TAG_NAME, "img")[0].get_attribute("title") if colunas[1].find_elements(By.TAG_NAME, "img") else "N/A"
#             if "Offline (Disabled Parent)" in status_info:
#                 status_info = "Offline"
            
#             link_text = colunas[2].find_element(By.TAG_NAME, "a").text

#             # Adiciona os dados ao CSV (incluindo o cluster e nome do balanceador)
#             dados_csv.append([cluster, nome_link, checkbox_value, status_info, link_text])

#         # Escrever os dados em um arquivo CSV
#         nome_arquivo = "pool_members.csv"  # Nome fixo para o arquivo

#         # Escrever os dados em um arquivo CSV
#         with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as arquivo_csv:
#             escritor = csv.writer(arquivo_csv)
#             if arquivo_csv.tell() == 0:  # Escrever cabeçalho se o arquivo estiver vazio
#                 escritor.writerow(["Cluster", "Nome do Link", "Coluna 0", "Status", "Coluna 2"])
#             escritor.writerows(dados_csv)

#         print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso.")

#         return "Processo concluído. CSV gerado com sucesso."
    
#     except Exception as e:
#         print(f"Erro ao acessar a página: {str(e)}")
#         return f"Erro ao acessar a página: {str(e)}"
    
#     finally:
#         navegador.quit()





# def acessar_pool_members(host, login, senha, url, nome_link, cluster):
#     # Configuração do driver
#     service = Service(executable_path=caminho_do_driver)
#     navegador = webdriver.Chrome(service=service)
    
#     host = host.upper()  # Garantir que o host esteja em maiúsculas
#     dados_csv = []  # Armazenar dados para o CSV
#     try:
#         # Acessando a página de login
#         navegador.get(url)
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="details-button"]'))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="proceed-link"]'))).click()

#         # Fazendo login
#         navegador.find_element(By.ID, "username").send_keys(login)
#         navegador.find_element(By.ID, "passwd").send_keys(senha)
#         navegador.find_element(By.CSS_SELECTOR, "button:nth-child(5)").click()

#         # Navegando até a lista de nodes
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Local Traffic"))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Nodes"))).click()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Node List"))).click()

#         navegador.switch_to.frame("contentframe")

#         # Pesquisar o host
#         search_input = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "search_input")))
#         search_input.clear()
#         search_input.send_keys(host)
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.NAME, "search_button"))).click()

#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, host))).click()
#         navegador.switch_to.parent_frame()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Pool Membership"))).click()
#         navegador.switch_to.frame("contentframe")

#         # Coletando os links para os membros do pool
#         pool_links = WebDriverWait(navegador, 10).until(
#             EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
#         )

#         link_9443 = next((link for link in pool_links if link.text.endswith("9443")), None)
#         link_9810 = next((link for link in pool_links if link.text.endswith("9810")), None)
#         link_9843 = next((link for link in pool_links if link.text.endswith("9843")), None)

#         if link_9443:
#             link_9443.click()
#         elif link_9810:
#             link_9810.click()
#         elif link_9843:
#             link_9843.click()
#         else:
#             print("Nenhum link desejado encontrado.")

#         navegador.switch_to.parent_frame()
#         WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Members"))).click()
#         navegador.switch_to.frame("contentframe")

#         # Coletando a tabela de membros
#         tabela = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='list_body']")))

#         linhas = tabela.find_elements(By.TAG_NAME, "tr")

#         for linha in linhas:
#             colunas = linha.find_elements(By.TAG_NAME, "td")
#             if len(colunas) < 3:
#                 continue  # Ignorar linhas com dados insuficientes

#             checkbox_value = colunas[0].find_element(By.TAG_NAME, 'input').get_attribute('value')
            
#             # Alterar o status para 'Offline' se o texto contiver 'Offline (Disabled Parent)'
#             status_info = colunas[1].find_elements(By.TAG_NAME, "img")[0].get_attribute("title") if colunas[1].find_elements(By.TAG_NAME, "img") else "N/A"
            
#             # Verificação para ajustar o status para "Enabled" ou "Offline"
#             if "Offline (Disabled Parent)" in status_info:
#                 status_info = "Offline"
#             elif "Available (Enabled) - Pool member is available" in status_info:
#                 status_info = "Enabled"
            
#             link_text = colunas[2].find_element(By.TAG_NAME, "a").text

#             # Adiciona os dados ao CSV (incluindo o cluster e nome do balanceador)
#             dados_csv.append([cluster, nome_link, checkbox_value, status_info, link_text])

#         # Escrever os dados em um arquivo CSV
#         nome_arquivo = "pool_members.csv"  # Nome fixo para o arquivo

#         # Escrever os dados em um arquivo CSV
#         with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as arquivo_csv:
#             escritor = csv.writer(arquivo_csv)
#             if arquivo_csv.tell() == 0:  # Escrever cabeçalho se o arquivo estiver vazio
#                 escritor.writerow(["Cluster", "Nome do Link", "Coluna 0", "Status", "Coluna 2"])
#             escritor.writerows(dados_csv)

#         print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso.")

#         return "Processo concluído. CSV gerado com sucesso."
    
#     except Exception as e:
#         print(f"Erro ao acessar a página: {str(e)}")
#         return f"Erro ao acessar a página: {str(e)}"
    
#     finally:
#         navegador.quit()





def acessar_pool_members(host, login, senha, url, nome_link, cluster):
    # Configuração do driver
    service = Service(executable_path=caminho_do_driver)
    navegador = webdriver.Chrome(service=service)
    
    host = host.upper()  # Garantir que o host esteja em maiúsculas
    dados_csv = []  # Armazenar dados para o CSV
    try:
        # Acessando a página de login
        navegador.get(url)
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="details-button"]'))).click()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="proceed-link"]'))).click()

        # Fazendo login
        navegador.find_element(By.ID, "username").send_keys(login)
        navegador.find_element(By.ID, "passwd").send_keys(senha)
        navegador.find_element(By.CSS_SELECTOR, "button:nth-child(5)").click()

        # Navegando até a lista de nodes
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Local Traffic"))).click()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Nodes"))).click()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Node List"))).click()

        navegador.switch_to.frame("contentframe")

        # Pesquisar o host
        search_input = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "search_input")))
        search_input.clear()
        search_input.send_keys(host)
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.NAME, "search_button"))).click()

        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, host))).click()
        navegador.switch_to.parent_frame()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Pool Membership"))).click()
        navegador.switch_to.frame("contentframe")

        # Coletando os links para os membros do pool
        pool_links = WebDriverWait(navegador, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        link_9443 = next((link for link in pool_links if link.text.endswith("9443")), None)
        link_9810 = next((link for link in pool_links if link.text.endswith("9810")), None)
        link_9843 = next((link for link in pool_links if link.text.endswith("9843")), None)

        if link_9443:
            link_9443.click()
        elif link_9810:
            link_9810.click()
        elif link_9843:
            link_9843.click()
        else:
            print("Nenhum link desejado encontrado.")

        navegador.switch_to.parent_frame()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Members"))).click()
        navegador.switch_to.frame("contentframe")

        # Coletando a tabela de membros
        tabela = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='list_body']")))

        linhas = tabela.find_elements(By.TAG_NAME, "tr")

        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) < 3:
                continue  # Ignorar linhas com dados insuficientes

            checkbox_value = colunas[0].find_element(By.TAG_NAME, 'input').get_attribute('value')
            
            # Alterar o status para 'Offline' se o texto contiver 'Offline (Disabled Parent)'
            status_info = colunas[1].find_elements(By.TAG_NAME, "img")[0].get_attribute("title") if colunas[1].find_elements(By.TAG_NAME, "img") else "N/A"
            
            # Verificação para ajustar o status para "Enabled" ou "Offline"
            if "Offline (Disabled Parent)" in status_info:
                status_info = "Offline"
            elif "Available (Enabled) - Pool member is available" in status_info:
                status_info = "Enabled"
            
            link_text = colunas[2].find_element(By.TAG_NAME, "a").text

            # Ignorar "/Common/" na coluna 0 e manter o restante
            if "/Common/" in checkbox_value:
                checkbox_value = checkbox_value.replace("/Common/", "")  # Remover "/Common/"

            # Adiciona os dados ao CSV (incluindo o cluster e nome do balanceador)
            dados_csv.append([cluster, nome_link, checkbox_value, status_info, link_text])

        # Escrever os dados em um arquivo CSV
        nome_arquivo = "pool_members.csv"  # Nome fixo para o arquivo

        # Escrever os dados em um arquivo CSV
        with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            if arquivo_csv.tell() == 0:  # Escrever cabeçalho se o arquivo estiver vazio
                escritor.writerow(["Cluster", "Nome do Link", "Coluna 0", "Status", "Coluna 2"])
            escritor.writerows(dados_csv)

        print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso.")

        return "Processo concluído. CSV gerado com sucesso."
    
    except Exception as e:
        print(f"Erro ao acessar a página: {str(e)}")
        return f"Erro ao acessar a página: {str(e)}"
    
    finally:
        navegador.quit()
