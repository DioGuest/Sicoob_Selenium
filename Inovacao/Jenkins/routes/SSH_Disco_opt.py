import paramiko
import time
from flask import Blueprint, render_template, request
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração de logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Manipulador de console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# Manipulador de arquivo
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Criação do Blueprint para reiniciar
ssh_bp = Blueprint('ssh_bp', __name__)

@ssh_bp.route('/ssh_disco_opt', methods=['GET'])
def ssh_disco_opt():
    return render_template('index8.html')  # Renderiza a página desejada

def execute_ssh_commands(host, username, password):
    port = 22  # Definido como 22 para SSH
    sudo_password = password  # Reutiliza a senha para comandos sudo
    result_message = ""

    # Cria uma sessão SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conecta ao servidor
        logger.info(f"Conectando ao servidor {host} com o usuário {username}")
        ssh.connect(host, port, username, password)
        result_message += f"Conectado ao servidor {host}<br>"

        # Executa o comando para verificar o tamanho da pasta temp ANTES da exclusão
        size_command_before = 'du -sh /opt/IBM/WAS/WebSphere/AppServer/temp'
        stdin, stdout, stderr = ssh.exec_command(size_command_before)
        size_before = stdout.read().decode().strip()
        result_message += f"Tamanho da pasta temp ANTES da exclusão: {size_before}<br>"
        logger.info(f"Tamanho da pasta temp ANTES da exclusão: {size_before}")

        # Executa o comando que deleta os arquivos temporários como sudo
        delete_command = 'sudo find /opt/IBM/WAS/WebSphere/AppServer/temp -name "*.tmp" -delete'
        stdin, stdout, stderr = ssh.exec_command(delete_command)
        stdin.write(sudo_password + '\n')
        stdin.flush()
        time.sleep(2)  # Aguardando o comando ser executado

        # Verifica o resultado do comando
        output = stdout.read().decode().strip()
        result_message += f"Resultado da exclusão de arquivos temporários:<br>{output}<br>"
        logger.info(f"Resultado da exclusão: {output}")

        error_output = stderr.read().decode()
        if error_output:
            result_message += f"Erro: {error_output}<br>"
            logger.error(f"Erro ao excluir arquivos: {error_output}")

        # Executa o comando para verificar o tamanho da pasta temp DEPOIS da exclusão
        size_command_after = 'du -sh /opt/IBM/WAS/WebSphere/AppServer/temp'
        stdin, stdout, stderr = ssh.exec_command(size_command_after)
        size_after = stdout.read().decode().strip()
        result_message += f"Tamanho da pasta temp DEPOIS da exclusão: {size_after}<br>"
        logger.info(f"Tamanho da pasta temp DEPOIS da exclusão: {size_after}")

    except Exception as e:
        result_message += f"Erro ao conectar ou executar o comando no servidor {host}: {str(e)}<br>"
        logger.error(f"Erro ao conectar ou executar o comando: {str(e)}")

    finally:
        ssh.close()
        logger.info(f"Conexão SSH encerrada para o servidor {host}.")

    return result_message

# Rota para processar a solicitação (POST)
@ssh_bp.route('/ssh_disco_opt', methods=['POST'])
def ssh_clean():
    # Recebe os dados do formulário
    hosts_string = request.form.get('Numero')  # Pega a string de hosts
    username = request.form.get('Name')
    password = request.form.get('PassWord')

    # Separa os hosts por vírgula e remove espaços em branco
    hosts = [host.strip() for host in hosts_string.split(',')] if hosts_string else []
    logger.info(f"Hosts recebidos para conexão: {hosts}")

    result_messages = []
    
    if not hosts or not username or not password:
        result_message = "Parâmetros inválidos!"
        logger.error(result_message)
        return result_message

    # Usando ThreadPoolExecutor para executar comandos em paralelo
    with ThreadPoolExecutor() as executor:
        future_to_host = {executor.submit(execute_ssh_commands, host, username, password): host for host in hosts}
        
        for future in as_completed(future_to_host):
            host = future_to_host[future]
            try:
                result = future.result()
                result_messages.append(result)
            except Exception as e:
                logger.error(f"Erro ao processar o servidor {host}: {str(e)}")
                result_messages.append(f"Erro ao processar o servidor {host}: {str(e)}")

    # Retorna os resultados concatenados
    return "<br>".join(result_messages)
