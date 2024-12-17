

from flask import Blueprint, render_template, request
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

# Criação do Blueprint
pesquisaCcs = Blueprint('pesquisaCcs', __name__)

# Caminho completo para o chromedriver
caminho_do_driver = Variavel_Ambiente_DRIVER

logger = logging.getLogger(__name__)

@pesquisaCcs.route('/Pesquisa_CCS')
def restart_page():
    nomes_clusters = obter_nomes_clusters_producao()  # Obtém os nomes dos clusters
    logger.info(f"Nomes dos clusters obtidos: {nomes_clusters}")  # Log para verificar os nomes dos clusters
    return render_template('index6.html', nomes_clusters=nomes_clusters)  # Passa a lista para o template


def obter_nomes_clusters_producao():
    url = "https://delivery.sicoob.com.br/sicoob-entrega-continua/configuracoes-clusters?count=1000&page=1"
    response = requests.get(url)
    if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        data = response.json()
        nomes_clusters_producao = []
        for cluster in data["resultado"]["dados"]:
            nome_cluster = cluster.get("nomeCluster")
            if any(host.get("ambiente") == "PRODUCAO" for host in cluster.get("hosts", [])):
                nomes_clusters_producao.append(nome_cluster)
        logger.info(f"Nomes de clusters em produção: {nomes_clusters_producao}")  # Log dos clusters em produção
        return nomes_clusters_producao
    else:
        logger.error(f"Erro ao obter clusters: {response.status_code} - {response.text}")
        return []





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

from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import render_template, request

@pesquisaCcs.route('/repostar', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    selected_clusters = list(set(request.form.get('selectedClusters', '').split(',')))

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

    def task(cluster, url):
        try:
            host = obter_host_do_cluster(cluster)
            if host:
                return f"{cluster} em {balanceadores[url]}", acessar_pool_members(host, username, password, url)
            else:
                return f"Nenhum host encontrado para o cluster {cluster}.", None
        except Exception as e:
            return f"Erro ao acessar o cluster {cluster}: {str(e)}", None

    with ThreadPoolExecutor() as executor:
        futures = []
        for cluster in selected_clusters:
            for url in balanceadores.keys():
                futures.append(executor.submit(task, cluster, url))

        for future in as_completed(futures):
            nome_balanceador, resultado = future.result()
            if resultado is not None:
                resultados[nome_balanceador] = resultado
            else:
                mensagem_erro += f"{nome_balanceador}<br>"

    # Ordenar os resultados por nome (chave)
    resultados_ordenados = dict(sorted(resultados.items()))

    return render_template('pesquisa4.html', resultados=resultados_ordenados, mensagem_erro=mensagem_erro)




def acessar_pool_members(host, login, senha, url):
    service = Service(executable_path=caminho_do_driver)
    navegador = webdriver.Chrome(service=service)
    host = host.upper()
    try:
        navegador.get(url)

        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="details-button"]'))).click()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="proceed-link"]'))).click()

        navegador.find_element(By.ID, "username").send_keys(login)
        navegador.find_element(By.ID, "passwd").send_keys(senha)
        navegador.find_element(By.CSS_SELECTOR, "button:nth-child(5)").click()

        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Local Traffic"))).click()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Nodes"))).click()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Node List"))).click()

        navegador.switch_to.frame("contentframe")
        search_input = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "search_input")))
        search_input.clear()
        search_input.send_keys(host)
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.NAME, "search_button"))).click()

        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, host))).click()
        navegador.switch_to.parent_frame()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Pool Membership"))).click()
        navegador.switch_to.frame("contentframe")

        pool_links = WebDriverWait(navegador, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        link_9443 = next((link for link in pool_links if link.text.endswith("9443")), None)
        link_9810 = next((link for link in pool_links if link.text.endswith("9810")), None)
        link_9843 = next((link for link in pool_links if link.text.endswith("9843")), None)  # Novo link adicionado

        if link_9443:
            link_9443.click()
        elif link_9810:
            link_9810.click()
        elif link_9843:  # Verifica se o link 9843 está disponível
            link_9843.click()
        else:
            logger.warning("Nenhum link desejado encontrado.")

        navegador.switch_to.parent_frame()
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Members"))).click()
        navegador.switch_to.frame("contentframe")

        tabela = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='list_body']")))

        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        print(linhas)
        result_message = f"Resultados para {url}:<br>"  # Adiciona o link pesquisado

        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")

            checkbox_value = colunas[0].find_element(By.TAG_NAME, 'input').get_attribute('value')
            result_message += f"Coluna 0: {checkbox_value}<br>"

            img_elements = colunas[1].find_elements(By.TAG_NAME, "img")
            if img_elements:
                status_info = img_elements[0].get_attribute("title")
                
                # Verifica se o status é "Offline (Enabled)" com uma mensagem de "No successful responses"
                if "Offline (Enabled)" in status_info and "No successful responses received before deadline" in status_info:
                    status_img = "<img src='/static/status_diamond_red.png' alt='Offline with errors'>"
                    status_info = f"<span style='color: red; font-weight: bold;'>{status_info}</span>"
                elif "Offline" in status_info:
                    status_img = "<img src='/static/office.png' alt='Offline'>"
                    status_info = f"<span style='color: red; font-weight: bold;'>{status_info}</span>"
                elif "Available (Enabled)" in status_info:
                    status_img = "<img src='/static/Enable.png' alt='Enabled'>"
                    status_info = status_info.replace("Enabled", "<span style='color: green; font-weight: bold;'>Enabled</span>")
                result_message += f"Status: {status_info}<br>{status_img}<br>"

            link_element = colunas[2].find_element(By.TAG_NAME, "a")
            result_message += f"Coluna 2: {link_element.text}<br>"

        return result_message
    finally:
        navegador.quit()
