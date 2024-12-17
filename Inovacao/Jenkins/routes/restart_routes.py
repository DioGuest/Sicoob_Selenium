
from flask import Blueprint, render_template, request
from Restart_Funcoes.Restart_Websphere import restart_Websphere
from Restart_Funcoes.Restart_Liberty import restart_liberty
from Restart_Funcoes.Restart_SRTB import restart_SRTB
from Pesquisar_Cluster import Pesquisar  # Certifique-se de importar o que for necessário
import logging

# Criação do Blueprint
restart_bp = Blueprint('restart', __name__)

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

@restart_bp.route('/')
def restart_page():
    return render_template('index.html')  # Renderiza a página de reinício

@restart_bp.route('/submit', methods=['POST'])
def restart():
    Numeros = request.form.get('Numero')
    Modo = request.form.get('Modo', '').upper()
    Login = request.form.get('Name')
    Senha = request.form.get('PassWord')

    result_message = ""

    if Numeros:
        numeros_lista = [numero.strip() for numero in Numeros.split(',')]
        for numero in numeros_lista:
            logger.info(f"Número recebido: {numero}")
            try:
                valor_codigo, valor_cluster = Pesquisar.pesquisar(numero)
                if valor_codigo and valor_cluster:
                    if valor_codigo.startswith("WASP") or valor_codigo.startswith("TRNP"):
                        mensagem_retorno = restart_Websphere(Modo, valor_cluster, valor_codigo, Login, Senha)
                        result_message += mensagem_retorno
                        logger.info(f"Executando o processo para Websphere: {valor_codigo} Operador: {Login}")

                    elif valor_codigo.startswith("CTRP"):
                        mensagem_retorno = restart_Websphere(Modo, valor_cluster, valor_codigo, Login, Senha)
                        result_message += mensagem_retorno
                        logger.info(f"Executado o Processo Websphere: {valor_codigo} Operador: {Login}")

                        mensagem_retorno = restart_liberty(Modo, valor_cluster, valor_codigo, Login, Senha)
                        result_message += mensagem_retorno
                        logger.info(f"Executado o Processo Liberty: {valor_codigo} Operador: {Login}")

                        mensagem_retorno = restart_SRTB(Modo, valor_cluster, valor_codigo, Login, Senha)
                        result_message += mensagem_retorno
                        logger.info(f"Executado o Processo SRTB: {valor_codigo} Operador: {Login}")
                else:
                    result_message += f"Erro ao localizar o código ou cluster para o número: {numero} "
                    logger.error(f"Erro ao localizar o código ou cluster para o número: {numero}")

            except Exception as e:
                result_message += f"Erro ao processar o número {numero}: {e}<br>"
                logger.error(f"Erro ao processar o número {numero}: {e}")

        result_message += "Restarts realizados com sucesso!"
    else:
        result_message = "Número da máquina não informado."

    return result_message
