
# from Balanceadores_ENABLE_NOR.Balanceador_2006_ENABLE import executar_processo_2006_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_2007_ENABLE import executar_processo_2007_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_4006_ENABLE import executar_processo_4006_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_4007_ENABLE import executar_processo_4007_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_CYOI_ENABLE import executar_processo_CYOI_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_CSS_ENABLE import executar_processo_CSS_ENABLE
# from Balanceadores_Isolar_NOR.Balanceador_2006 import executar_processo_2006
# from Balanceadores_Isolar_NOR.Balanceador_2007 import executar_processo_2007
# from Balanceadores_Isolar_NOR.Balanceador_4006 import executar_processo_4006
# from Balanceadores_Isolar_NOR.Balanceador_4007 import executar_processo_4007
# from Balanceadores_Isolar_NOR.Balanceador_CSS import executar_processo_CSS
# from Balanceadores_Isolar_NOR.Balanceador_CYOI import executar_processo_CYOI
# from Pesquisar_Cluster import Pesquisar
# from Restart_Funcoes.Restart_Liberty import restart_liberty
# from Restart_Funcoes.Restart_SRTB import restart_SRTB
# from Restart_Funcoes.Restart_Websphere import restart_Websphere
# from flask import Flask, render_template, request, jsonify
# from routes.jenkins_Pesquisa_Whebsphere import jenkins_Whebsphere  # Importa as rotas do Jenkins
# from routes.jenkins_Pesquisa_Liberty import jenkins_Liberty
# from routes.jenkins_Pesquisa_SRTB import jenkins_SRTB
# from routes.restart_routes import restart_bp
# from routes.Isolar_Nor import Isolar_Nor
# from routes.Pesquisa_CCS import pesquisaCcs
# from routes.Isolar_ENABLE import Habilitar
# from routes.SSH_Outofmemory import move_bp
# from routes.SSH_Disco_opt import ssh_bp
# import concurrent.futures
# import logging
# import time
# from flask import Flask, request
# from flask import Blueprint, render_template, request


# # Configuração básica do logging
# class DevToolsFilter(logging.Filter):
#     def filter(self, record):
#         return 'DevTools listening on' not in record.getMessage() and \
#                'Invalid first_paint' not in record.getMessage()

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# # Manipulador de console
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# console_handler.addFilter(DevToolsFilter())

# # Manipulador de arquivo
# file_handler = logging.FileHandler('app.log')
# file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# file_handler.addFilter(DevToolsFilter())

# logger.addHandler(console_handler)
# logger.addHandler(file_handler)

# from dotenv import load_dotenv
# import os

# # Carrega as variáveis do arquivo .env
# load_dotenv()

# RestartCompleto_SEGUENCIAL = Blueprint('RestartCompleto_SEGUENCIAL', __name__)


# Variavel_Ambiente_DRIVER = os.getenv('Variavel_Ambiente_DRIVER')

# caminho_do_driver = Variavel_Ambiente_DRIVER

# @RestartCompleto_SEGUENCIAL.route('/IsolarERestartEnable')
# def index5():
#     return render_template('index9.html')

# @RestartCompleto_SEGUENCIAL.route('/submitIsolarRestartEnable', methods=['POST'])
# def submitIsolarRestartEnables():
#     numeros = request.form.get('Numero')
#     login = request.form.get('Name')
#     senha = request.form.get('PassWord')
#     Modo = request.form.get('Modo', '').upper()
#     logger.info(f"Modo: {Modo}")

#     result_message = ""

#     if numeros:
#         numeros_lista = [numero.strip() for numero in numeros.split(',')]
#         processos = [
#             ("CSS", executar_processo_CSS),
#             ("CYOI", executar_processo_CYOI),
#             ("4007", executar_processo_4007),
#             ("4006", executar_processo_4006),
#             ("2007", executar_processo_2007),
#             ("2006", executar_processo_2006)
#         ]

#         max_threads = 2  # Define o número máximo de threads
#         for nome_processo, processo in processos:
#             logger.info(f"Iniciando processos para {nome_processo} Operador: {login}")
#             with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
#                 futures = {executor.submit(processo, caminho_do_driver, login, senha, numero): numero for numero in numeros_lista}

#                 for future in concurrent.futures.as_completed(futures):
#                     numero = futures[future]
#                     try:
#                         message = future.result()
#                         result_message += f"{message}<br>"
#                         logger.info(message)

#                         if "Falha no login" in message:
#                             result_message += "Erro de autenticação detectado. Processo interrompido."
#                             return result_message

#                     except Exception as e:
#                         result_message += f"Erro ao processar {nome_processo} para o número {numero}: {e}"
#                         logger.error(f"Erro ao processar {nome_processo} para o número {numero}: {e}")

#         result_message += "Processo concluído com sucesso!"

#         # Aguarda 3 minutos antes de executar o segundo processo
#         time.sleep(180)

#         # Chama a função submitNew com os mesmos dados do formulário
#         submit_new_result = submitNew(request.form)
#         if submit_new_result:
#             result_message += submit_new_result

#     else:
#         result_message = "Número da máquina não informado."

#     return result_message

# def submitNew(form_data):
#     Numeros = form_data.get('Numero')
#     Modo = form_data.get('Modo', '').upper()
#     logger.info(f"Modo: {Modo}")
#     Login = form_data.get('NameJenkins')
#     Senha = form_data.get('PassWordJenkins')

#     result_message = ""

#     if Numeros:
#         numeros_lista = [numero.strip() for numero in Numeros.split(',')]
        

#         for numero in numeros_lista:
#             logger.info(f"Número recebido: {numero}")
#             try:
#                 valor_codigo, valor_cluster = Pesquisar.pesquisar(numero)
#                 if valor_codigo and valor_cluster:
#                     if valor_codigo.startswith("WASP") or valor_codigo.startswith("TRNP"):
#                         mensagem_retorno = restart_Websphere(Modo, valor_cluster, valor_codigo, Login, Senha)
#                         result_message += mensagem_retorno
#                         logger.info(f"Executando o processo para Websphere: {valor_codigo} Operador: {Login}")

#                     elif valor_codigo.startswith("CTRP"):
#                         mensagem_retorno = restart_Websphere(Modo, valor_cluster, valor_codigo, Login, Senha)
#                         result_message += mensagem_retorno
#                         logger.info(f"Executado o Processo Websphere: {valor_codigo} Operador: {Login}")

#                         mensagem_retorno = restart_liberty(Modo, valor_cluster, valor_codigo, Login, Senha)
#                         result_message += mensagem_retorno
#                         logger.info(f"Executado o Processo Liberty: {valor_codigo} Operador: {Login}")

#                         mensagem_retorno = restart_SRTB(Modo, valor_cluster, valor_codigo, Login, Senha)
#                         result_message += mensagem_retorno
#                         logger.info(f"Executado o Processo SRTB: {valor_codigo} Operador: {Login}")
#                 else:
#                     result_message += f"Erro ao localizar o código ou cluster para o número: {numero} "
#                     logger.error(f"Erro ao localizar o código ou cluster para o número: {numero}")

#             except Exception as e:
#                 result_message += f"Erro ao processar o número {numero}: {e}"
#                 logger.error(f"Erro ao processar o número {numero}: {e}")

#         # Aguarda 4 minutos antes de executar o segundo processo
#         time.sleep(240)

#         # Chama a função submitIsolarRestartEnablesNew com os mesmos dados do formulário
#         submit_new_result = submitIsolarRestartEnablesNew(form_data)
#         if submit_new_result:
#             result_message += submit_new_result

#     else:
#         result_message = "Número da máquina não informado."

#     return result_message or ""  # Garante que a função sempre retorne uma string

# def submitIsolarRestartEnablesNew(form_data):
#     numeros = form_data.get('Numero')
#     login = form_data.get('Name')
#     senha = form_data.get('PassWord')

#     result_message = ""

#     if numeros:
#         numeros_lista = [numero.strip() for numero in numeros.split(',')]
#         processos = [
#             ("CSS", executar_processo_CSS_ENABLE),
#             ("CYOI", executar_processo_CYOI_ENABLE),
#             ("4007", executar_processo_4007_ENABLE),
#             ("4006", executar_processo_4006_ENABLE),
#             ("2007", executar_processo_2007_ENABLE),
#             ("2006", executar_processo_2006_ENABLE)
#         ]

#         max_threads = 2  # Define o número máximo de threads
#         for nome_processo, processo in processos:
#             logger.info(f"Iniciando processos para {nome_processo} Operador: {login}")
#             with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
#                 futures = {executor.submit(processo, caminho_do_driver, login, senha, numero): numero for numero in numeros_lista}

#                 for future in concurrent.futures.as_completed(futures):
#                     numero = futures[future]
#                     try:
#                         message = future.result()
#                         result_message += f"{message}<br>"
#                         logger.info(message)
#                     except Exception as e:
#                         result_message += f"Erro ao processar {nome_processo} para o número {numero}: {e}"
#                         logger.error(f"Erro ao processar {nome_processo} para o número {numero}: {e}")

#         result_message += "Processo concluído com sucesso!"

#     else:
#         result_message = "Número da máquina não informado."

#     return result_message or ""  # Garante que a função sempre retorne uma string




#FUNCIONANDO *****
# from Balanceadores_ENABLE_NOR.Balanceador_2006_ENABLE import executar_processo_2006_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_2007_ENABLE import executar_processo_2007_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_4006_ENABLE import executar_processo_4006_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_4007_ENABLE import executar_processo_4007_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_CYOI_ENABLE import executar_processo_CYOI_ENABLE
# from Balanceadores_ENABLE_NOR.Balanceador_CSS_ENABLE import executar_processo_CSS_ENABLE
# from Balanceadores_Isolar_NOR.Balanceador_2006 import executar_processo_2006
# from Balanceadores_Isolar_NOR.Balanceador_2007 import executar_processo_2007
# from Balanceadores_Isolar_NOR.Balanceador_4006 import executar_processo_4006
# from Balanceadores_Isolar_NOR.Balanceador_4007 import executar_processo_4007
# from Balanceadores_Isolar_NOR.Balanceador_CSS import executar_processo_CSS
# from Balanceadores_Isolar_NOR.Balanceador_CYOI import executar_processo_CYOI
# from Pesquisar_Cluster import Pesquisar
# from Restart_Funcoes.Restart_Liberty import restart_liberty
# from Restart_Funcoes.Restart_SRTB import restart_SRTB
# from Restart_Funcoes.Restart_Websphere import restart_Websphere
# from flask import Flask, render_template, request, jsonify, Blueprint
# import concurrent.futures
# import logging
# import time
# import os
# from dotenv import load_dotenv

# # Configuração básica do logging
# class DevToolsFilter(logging.Filter):
#     def filter(self, record):
#         return 'DevTools listening on' not in record.getMessage() and \
#                'Invalid first_paint' not in record.getMessage()

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# console_handler = logging.StreamHandler()
# console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# console_handler.addFilter(DevToolsFilter())

# file_handler = logging.FileHandler('app.log')
# file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# file_handler.addFilter(DevToolsFilter())

# logger.addHandler(console_handler)
# logger.addHandler(file_handler)

# # Carrega as variáveis do arquivo .env
# load_dotenv()
# caminho_do_driver = os.getenv('Variavel_Ambiente_DRIVER')

# RestartCompleto_SEGUENCIAL = Blueprint('RestartCompleto_SEGUENCIAL', __name__)

# @RestartCompleto_SEGUENCIAL.route('/IsolarERestartEnable_SEGUENCIAL')
# def index5():
#     return render_template('index9.html')

# @RestartCompleto_SEGUENCIAL.route('/submitIsolarRestartEnable_SEGUENCIAL', methods=['POST'])
# def submitIsolarRestartEnables():
#     numeros = request.form.get('Numero')
#     login = request.form.get('Name')
#     senha = request.form.get('PassWord')
#     Modo = request.form.get('Modo', '').upper()
#     logger.info(f"Modo: {Modo}")

#     result_message = ""

#     if numeros:
#         numeros_lista = [numero.strip() for numero in numeros.split(',')]
        
#         for numero in numeros_lista:
#             logger.info(f"Iniciando processos de isolamento para o número {numero} Operador: {login}")
#             result_message += processar_isolamento(numero, login, senha)
            
#             # Reinicialização após isolamento
#             result_message += processar_reinicializacao(numero, Modo, login, senha)
            
#             # Habilitação após reinicialização
#             result_message += processar_habilitacao(numero, login, senha)

#     else:
#         result_message = "Número da máquina não informado."

#     return result_message

# def processar_isolamento(numero, login, senha):
#     result_message = ""
#     processos_isolar = [
#         ("CSS", executar_processo_CSS),
#         ("CYOI", executar_processo_CYOI),
#         ("4007", executar_processo_4007),
#         ("4006", executar_processo_4006),
#         ("2007", executar_processo_2007),
#         ("2006", executar_processo_2006)
#     ]

#     for nome_processo, processo in processos_isolar:
#         try:
#             message = processo(caminho_do_driver, login, senha, numero)
#             result_message += f"{message}<br>"
#             logger.info(message)
#             if "Falha no login" in message:
#                 return "Erro de autenticação detectado. Processo interrompido."
#         except Exception as e:
#             result_message += f"Erro ao processar {nome_processo} para o número {numero}: {e}"
#             logger.error(f"Erro ao processar {nome_processo} para o número {numero}: {e}")

#     result_message += "Processo de isolamento concluído para este número.<br>"
#     time.sleep(180)
#     return result_message

# def processar_reinicializacao(numero, Modo, login, senha):
#     result_message = ""
#     try:
#         valor_codigo, valor_cluster = Pesquisar.pesquisar(numero)
#         if valor_codigo and valor_cluster:
#             if valor_codigo.startswith("WASP") or valor_codigo.startswith("TRNP"):
#                 result_message += restart_Websphere(Modo, valor_cluster, valor_codigo, login, senha)
#             elif valor_codigo.startswith("CTRP"):
#                 result_message += restart_Websphere(Modo, valor_cluster, valor_codigo, login, senha)
#                 result_message += restart_liberty(Modo, valor_cluster, valor_codigo, login, senha)
#                 result_message += restart_SRTB(Modo, valor_cluster, valor_codigo, login, senha)
#         else:
#             result_message += f"Erro ao localizar o código ou cluster para o número: {numero}"
#     except Exception as e:
#         result_message += f"Erro ao processar a reinicialização para o número {numero}: {e}"

#     time.sleep(240)
#     return result_message

# def processar_habilitacao(numero, login, senha):
#     result_message = ""
#     processos_enable = [
#         ("CSS", executar_processo_CSS_ENABLE),
#         ("CYOI", executar_processo_CYOI_ENABLE),
#         ("4007", executar_processo_4007_ENABLE),
#         ("4006", executar_processo_4006_ENABLE),
#         ("2007", executar_processo_2007_ENABLE),
#         ("2006", executar_processo_2006_ENABLE)
#     ]

#     for nome_processo, processo in processos_enable:
#         try:
#             message = processo(caminho_do_driver, login, senha, numero)
#             result_message += f"{message}<br>"
#             logger.info(message)
#         except Exception as e:
#             result_message += f"Erro ao processar {nome_processo} para o número {numero}: {e}"
#             logger.error(f"Erro ao processar {nome_processo} para o número {numero}: {e}")

#     result_message += "Processo de habilitação concluído para este número.<br>"
#     return result_message





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
    logger.info(f"Modo: {Modo}")

    result_message = ""

    if numeros:
        numeros_lista = [numero.strip() for numero in numeros.split(',')]
        
        for numero in numeros_lista:
            logger.info(f"Iniciando processos de isolamento para o número {numero} Operador: {login}")
            result_message += processar_isolamento(numero, login, senha)
            
            # Reinicialização após isolamento
            result_message += processar_reinicializacao(numero, Modo, login, senha)
            
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

def processar_reinicializacao(numero, Modo, login, senha):
    result_message = ""
    try:
        valor_codigo, valor_cluster = Pesquisar.pesquisar(numero)
        if valor_codigo and valor_cluster:
            if valor_codigo.startswith("WASP") or valor_codigo.startswith("TRNP"):
                result_message += restart_Websphere(Modo, valor_cluster, valor_codigo, login, senha)
            elif valor_codigo.startswith("CTRP"):
                result_message += restart_Websphere(Modo, valor_cluster, valor_codigo, login, senha)
                result_message += restart_liberty(Modo, valor_cluster, valor_codigo, login, senha)
                result_message += restart_SRTB(Modo, valor_cluster, valor_codigo, login, senha)
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
