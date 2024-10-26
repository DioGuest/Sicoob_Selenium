from flask import Blueprint, render_template, jsonify
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

LOGIN_JENKINS= os.getenv('LOGIN_JENKINS')

TOKEN_JENKINS= os.getenv('TOKEN_JENKINS')


jenkins_SRTB = Blueprint('jenkins_SRTB', __name__)

# Configurações do Jenkins
JENKINS_URL = 'https://deploy.sicoob.com.br/view/OperacoesTI/job/Restart/job/SRTB/job/restart-srtb/api/json'
USER = LOGIN_JENKINS
TOKEN = TOKEN_JENKINS
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

def fetch_build_data(build):
    """Busca dados de uma build específica."""
    build_url = build['url'] + 'api/json'
    response = requests.get(build_url, auth=(USER, TOKEN), headers=HEADERS)
    
    if response.status_code == 200:
        build_data = response.json()
        timestamp = datetime.fromtimestamp(build_data['timestamp'] / 1000.0)

        user_name = "Desconhecido"
        for action in build_data.get('actions', []):
            if 'causes' in action:
                for cause in action['causes']:
                    if 'userName' in cause:
                        user_name = cause['userName']

        log_url = build['url'] + 'consoleText'
        log_response = requests.get(log_url, auth=(USER, TOKEN), headers=HEADERS)

        if log_response.status_code == 200:
            log_text = log_response.text
            acao, modo, cluster, ambiente, selecionados = "Não disponível", "Não disponível", "Não disponível", "Não disponível", "Não disponível"
            servidores = ""

            for line in log_text.splitlines():
                if "Ação:" in line:
                    acao = line.split("Ação:")[-1].strip()
                if "Modo:" in line:
                    modo = line.split("Modo:")[-1].strip()
                if "Cluster:" in line:
                    cluster = line.split("Cluster:")[-1].strip()
                if "Ambiente:" in line:
                    ambiente = line.split("Ambiente:")[-1].strip()
                if "Servidores:" in line:
                    servidores = line.split("Servidores:")[-1].strip()

            builds_info = {
                'number': build_data['number'],
                'url': build_data['url'],
                'result': build_data['result'],
                'timestamp': timestamp,
                'duration': build_data['duration'],
                'user': user_name,
                'acao': acao,
                'modo': modo,
                'cluster': cluster,
                'ambiente': ambiente,
                'selecionados': selecionados,
                'servidores': servidores
            }

            return builds_info
    return None

@jenkins_SRTB.route('/pesquisa3')
def home():
    builds = []
    error_message = None

    try:
        response = requests.get(JENKINS_URL, auth=(USER, TOKEN), headers=HEADERS)

        if response.status_code == 200:
            job_data = response.json()
            for build in job_data.get('builds', []):
                build_info = fetch_build_data(build)
                if build_info:
                    builds.append(build_info)
        else:
            error_message = f"Erro ao acessar Jenkins: {response.status_code}"

    except Exception as e:
        error_message = f"Ocorreu um erro: {e}"

    return render_template('pesquisa3.html', builds=builds, error_message=error_message)

@jenkins_SRTB.route('/builds')
def get_builds():
    builds = []

    try:
        response = requests.get(JENKINS_URL, auth=(USER, TOKEN), headers=HEADERS)

        if response.status_code == 200:
            job_data = response.json()
            for build in job_data.get('builds', []):
                build_info = fetch_build_data(build)
                if build_info:
                    builds.append(build_info)

        return jsonify({'builds': builds}), 200
    except Exception as e:
        return jsonify({'message': f'Ocorreu um erro: {e}'}), 500
