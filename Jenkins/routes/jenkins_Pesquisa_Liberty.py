from flask import Blueprint, render_template, jsonify
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

LOGIN_JENKINS= os.getenv('LOGIN_JENKINS')

TOKEN_JENKINS= os.getenv('TOKEN_JENKINS')


jenkins_Liberty = Blueprint('jenkins_liberty', __name__)



@jenkins_Liberty.route('/pesquisa2')
def home():
    jenkins_url = 'https://deploy.sicoob.com.br/view/OperacoesTI/job/Restart/job/Liberty/job/Restart-Liberty/api/json'
    user = LOGIN_JENKINS
    token = TOKEN_JENKINS

    builds = []
    error_message = None

    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(jenkins_url, auth=(user, token), headers=headers)

        if response.status_code == 200:
            job_data = response.json()
            for build in job_data.get('builds', []):
                build_url = build['url'] + 'api/json'
                build_response = requests.get(build_url, auth=(user, token), headers=headers)

                if build_response.status_code == 200:
                    build_data = build_response.json()
                    timestamp = datetime.fromtimestamp(build_data['timestamp'] / 1000.0)

                    user_name = "Desconhecido"
                    for action in build_data.get('actions', []):
                        if 'causes' in action:
                            for cause in action['causes']:
                                if 'userName' in cause:
                                    user_name = cause['userName']

                    acao, modo, cluster, ambiente, selecionados = "Não disponível", "Não disponível", "Não disponível", "Não disponível", "Não disponível"
                    log_url = build['url'] + 'consoleText'
                    log_response = requests.get(log_url, auth=(user, token), headers=headers)

                    if log_response.status_code == 200:
                        log_text = log_response.text
                        for line in log_text.splitlines():
                            if "Executado" in line:
                                acao = line.split("Executado")[0].strip() if "Executado" in line else acao
                            if "Será executado RESTART" in line:
                                acao = "RESTART"  # Captura a ação "RESTART"
                            if "[Pipeline]" in line and "Branch:" in line:
                                selecionados = line.split("Branch:")[1].strip(' )')
                            if "Ambiente:" in line:
                                ambiente = line.split("Ambiente:")[-1].strip() if "Ambiente:" in line else ambiente
                            if "Modo:" in line:
                                modo = line.split("Modo:")[-1].strip() if "Modo:" in line else modo

                    builds.append({
                        'number': build_data['number'],
                        'url': build_data['url'],
                        'result': build_data['result'],
                        'timestamp': timestamp,
                        'duration': build_data['duration'],
                        'user': user_name,
                        'acao': acao,
                        'modo': modo,
                        'cluster': cluster,  # Se você ainda quiser manter a captura do cluster
                        'ambiente': ambiente,
                        'selecionados': selecionados
                    })
        else:
            error_message = f"Erro ao acessar Jenkins: {response.status_code}"

    except Exception as e:
        error_message = f"Ocorreu um erro: {e}"

    return render_template('pesquisa2.html', builds=builds, error_message=error_message)

