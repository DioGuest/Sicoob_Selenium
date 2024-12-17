from flask import Blueprint, render_template, request
import logging
from Balanceadores_Isolar_NOR.Balanceador_2006 import executar_processo_2006
from Balanceadores_Isolar_NOR.Balanceador_2007 import executar_processo_2007
from Balanceadores_Isolar_NOR.Balanceador_4006 import executar_processo_4006
from Balanceadores_Isolar_NOR.Balanceador_4007 import executar_processo_4007
from Balanceadores_Isolar_NOR.Balanceador_CSS import executar_processo_CSS
from Balanceadores_Isolar_NOR.Balanceador_CYOI import executar_processo_CYOI
import concurrent.futures
import logging



# Criação do Blueprint
Isolar_Nor = Blueprint('Isolar_Nor', __name__)

# Configuração básica do logging
class DevToolsFilter(logging.Filter):
    def filter(self, record):
        return 'DevTools listening on' not in record.getMessage() and \
               'Invalid first_paint' not in record.getMessage()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Manipulador de console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
console_handler.addFilter(DevToolsFilter())

# Manipulador de arquivo
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
file_handler.addFilter(DevToolsFilter())

logger.addHandler(console_handler)
logger.addHandler(file_handler)

from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

Variavel_Ambiente_DRIVER = os.getenv('Variavel_Ambiente_DRIVER')

caminho_do_driver = Variavel_Ambiente_DRIVER


@Isolar_Nor.route('/Isolar')
def index4():
    return render_template('index4.html')

@Isolar_Nor.route('/submitIsolar', methods=['POST'])
def submitIsolar():
    numeros = request.form.get('Numero')
    login = request.form.get('Name')
    senha = request.form.get('PassWord')

    result_message = ""

    if numeros:
        numeros_lista = [numero.strip() for numero in numeros.split(',')]
        processos = [
            ("CSS", executar_processo_CSS),
            ("CYOI", executar_processo_CYOI),
            ("4007", executar_processo_4007),
            ("4006", executar_processo_4006),
            ("2007", executar_processo_2007),
            ("2006", executar_processo_2006)
        ]

        for nome_processo, processo in processos:
            logger.info(f"Iniciando processos para {nome_processo}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(processo, caminho_do_driver, login, senha, numero): numero for numero in numeros_lista}
                
                for future in concurrent.futures.as_completed(futures):
                    numero = futures[future]
                    try:
                        message = future.result()
                        result_message += f"{message}<br>"
                        logger.info(message)
                    except Exception as e:
                        result_message += f"Erro ao processar {nome_processo} para o número {numero}: {e}<br>"
                        logger.error(f"Erro ao processar {nome_processo} para o número {numero}: {e}")

        result_message += "Processo concluído com sucesso!<br>"
    else:
        result_message = "Número da máquina não informado.<br>"

    return result_message






