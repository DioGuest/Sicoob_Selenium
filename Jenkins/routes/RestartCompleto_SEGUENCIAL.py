
from Balanceadores_ENABLE_NOR.Balanceador_2006_ENABLE import executar_processo_2006_ENABLE
from Balanceadores_ENABLE_NOR.Balanceador_2007_ENABLE import executar_processo_2007_ENABLE
from Balanceadores_ENABLE_NOR.Balanceador_4006_ENABLE import executar_processo_4006_ENABLE
from Balanceadores_ENABLE_NOR.Balanceador_4007_ENABLE import executar_processo_4007_ENABLE
from Balanceadores_ENABLE_NOR.Balanceador_CYOI_ENABLE import executar_processo_CYOI_ENABLE
from Balanceadores_ENABLE_NOR.Balanceador_CSS_ENABLE import executar_processo_CSS_ENABLE
from Balanceadores_Isolar_NOR.Balanceador_2006 import executar_processo_2006
from Balanceadores_Isolar_NOR.Balanceador_2007 import executar_processo_2007
from Balanceadores_Isolar_NOR.Balanceador_4006 import executar_processo_4006
from Balanceadores_Isolar_NOR.Balanceador_4007 import executar_processo_4007
from Balanceadores_Isolar_NOR.Balanceador_CSS import executar_processo_CSS
from Balanceadores_Isolar_NOR.Balanceador_CYOI import executar_processo_CYOI
from Pesquisar_Cluster import Pesquisar
from Restart_Funcoes.Restart_Liberty import restart_liberty
from Restart_Funcoes.Restart_SRTB import restart_SRTB
from Restart_Funcoes.Restart_Websphere import restart_Websphere
from flask import Flask, render_template, request, jsonify, Blueprint
import concurrent.futures
import logging
import time
import os
from dotenv import load_dotenv

# Configuração básica do logging
class DevToolsFilter(logging.Filter):
    def filter(self, record):
        return 'DevTools listening on' not in record.getMessage() and \
               'Invalid first_paint' not in record.getMessage()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
console_handler.addFilter(DevToolsFilter())

file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
file_handler.addFilter(DevToolsFilter())

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Carrega as variáveis do arquivo .env
load_dotenv()
caminho_do_driver = os.getenv('Variavel_Ambiente_DRIVER')

RestartCompleto_SEGUENCIAL = Blueprint('RestartCompleto_SEGUENCIAL', __name__)

@RestartCompleto_SEGUENCIAL.route('/IsolarERestartEnable_SEGUENCIAL')
def index5():
    return render_template('index9.html')

@RestartCompleto_SEGUENCIAL.route('/submitIsolarRestartEnable_SEGUENCIAL', methods=['POST'])
def submitIsolarRestartEnables():
    numeros = request.form.get('Numero')
    login = request.form.get('Name')
    senha = request.form.get('PassWord')
    Modo = request.form.get('Modo', '').upper()
    NameJenkins = request.form.get('NameJenkins')
    PassWordJenkins = request.form.get('PassWordJenkins')
    logger.info(f"Modo: {Modo}")

    result_message = ""

    if numeros:
        numeros_lista = [numero.strip() for numero in numeros.split(',')]
        
        for numero in numeros_lista:
            logger.info(f"Iniciando processos de isolamento para o número {numero} Operador: {login}")
            result_message += processar_isolamento(numero, login, senha)
            
            # Reinicialização após isolamento
            result_message += processar_reinicializacao(numero, Modo, NameJenkins, PassWordJenkins)
            
            # Habilitação após reinicialização
            result_message += processar_habilitacao(numero, login, senha)

    else:
        result_message = "Número da máquina não informado."

    return result_message

def processar_isolamento(numero, login, senha):
    result_message = ""

    processos_isolar = [
        ("CSS", executar_processo_CSS),
        ("CYOI", executar_processo_CYOI),
        ("4007", executar_processo_4007),
        ("4006", executar_processo_4006),
        ("2007", executar_processo_2007),
        ("2006", executar_processo_2006)
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(processo, caminho_do_driver, login, senha, numero): nome_processo 
            for nome_processo, processo in processos_isolar
        }
        
        for future in concurrent.futures.as_completed(futures):
            nome_processo = futures[future]
            try:
                message = future.result()
                result_message += f"{message}<br>"
                logger.info(message)
            except Exception as e:
                result_message += f"Erro ao processar {nome_processo} para o número {numero}: {e}<br>"
                logger.error(f"Erro ao processar {nome_processo} para o número {numero}: {e}")

    result_message += "Processo de isolamento concluído para este número.<br>"
    time.sleep(180)  # Mantém o delay após todos os processos de isolamento
    return result_message

def processar_reinicializacao(numero, Modo, NameJenkins, PassWordJenkins):
    result_message = ""
    try:
        valor_codigo, valor_cluster = Pesquisar.pesquisar(numero)
        if valor_codigo and valor_cluster:
            if valor_codigo.startswith("WASP") or valor_codigo.startswith("TRNP"):
                logger.info(f"Executando o processo para Websphere: {valor_codigo} Operador: {NameJenkins}")
                result_message += restart_Websphere(Modo, valor_cluster, valor_codigo, NameJenkins, PassWordJenkins)
            elif valor_codigo.startswith("CTRP"):
                result_message += restart_Websphere(Modo, valor_cluster, valor_codigo, NameJenkins, PassWordJenkins)
                logger.info(f"Executado o Processo Websphere: {valor_codigo} Operador: {NameJenkins}")

                result_message += restart_liberty(Modo, valor_cluster, valor_codigo, NameJenkins, PassWordJenkins)
                logger.info(f"Executado o Processo Liberty: {valor_codigo} Operador: {NameJenkins}")

                result_message += restart_SRTB(Modo, valor_cluster, valor_codigo, NameJenkins, PassWordJenkins)
                logger.info(f"Executado o Processo SRTB: {valor_codigo} Operador: {NameJenkins}")
        else:
            result_message += f"Erro ao localizar o código ou cluster para o número: {numero}<br>"
    except Exception as e:
        result_message += f"Erro ao processar a reinicialização para o número {numero}: {e}<br>"

    time.sleep(240)  # Delay após reinicialização
    return result_message

def processar_habilitacao(numero, login, senha):
    result_message = ""
    processos_enable = [
        ("CSS", executar_processo_CSS_ENABLE),
        ("CYOI", executar_processo_CYOI_ENABLE),
        ("4007", executar_processo_4007_ENABLE),
        ("4006", executar_processo_4006_ENABLE),
        ("2007", executar_processo_2007_ENABLE),
        ("2006", executar_processo_2006_ENABLE)
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(processo, caminho_do_driver, login, senha, numero): nome_processo 
            for nome_processo, processo in processos_enable
        }
        
        for future in concurrent.futures.as_completed(futures):
            nome_processo = futures[future]
            try:
                message = future.result()
                result_message += f"{message}<br>"
                logger.info(message)
            except Exception as e:
                result_message += f"Erro ao processar {nome_processo} para o número {numero}: {e}<br>"
                logger.error(f"Erro ao processar {nome_processo} para o número {numero}: {e}")

    result_message += "Processo de habilitação concluído para este número.<br>"
    return result_message
