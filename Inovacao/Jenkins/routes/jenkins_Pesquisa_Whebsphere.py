# routes/jenkins_routes.py
from flask import Blueprint, render_template, jsonify
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

LOGIN_JENKINS= os.getenv('LOGIN_JENKINS')

TOKEN_JENKINS= os.getenv('TOKEN_JENKINS')




jenkins_Whebsphere = Blueprint('jenkins', __name__)

@jenkins_Whebsphere.route('/pesquisa')
def home():
    jenkins_url = 'http://deploy.sicoob.com.br/job/Restart/job/Websphere/job/websphere-cluster-action/api/json'
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

                    acao = modo = cluster = ambiente = selecionados = "Não disponível"
                    log_url = build['url'] + 'consoleText'
                    log_response = requests.get(log_url, auth=(user, token), headers=headers)
                    
                    if log_response.status_code == 200:
                        log_text = log_response.text
                        for line in log_text.splitlines():
                            if "Ação:" in line:
                                acao = line.split(":")[1].strip()
                            elif "Modo:" in line:
                                modo = line.split(":")[1].strip()
                            elif "Cluster:" in line:
                                cluster = line.split(":")[1].strip()
                            elif "Ambiente:" in line:
                                ambiente = line.split(":")[1].strip()
                            elif "Selecionados:" in line:
                                selecionados = line.split(":")[1].strip()

                    builds.append({
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
                        'selecionados': selecionados
                    })
        else:
            error_message = f"Erro ao acessar Jenkins: {response.status_code}"

    except Exception as e:
        error_message = f"Ocorreu um erro: {e}"

    return render_template('pesquisa.html', builds=builds, error_message=error_message)


@jenkins_Whebsphere.route('/builds')
def get_builds():
    jenkins_url = 'http://deploy.sicoob.com.br/job/Restart/job/Websphere/job/websphere-cluster-action/api/json'
    user = 'diogo.soares'
    token = '11206d14a0f442b78e9bd8790bf496d4e5'

    builds = []

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

                    acao = modo = cluster = ambiente = selecionados = "Não disponível"
                    log_url = build['url'] + 'consoleText'
                    log_response = requests.get(log_url, auth=(user, token), headers=headers)
                    
                    if log_response.status_code == 200:
                        log_text = log_response.text
                        for line in log_text.splitlines():
                            if "Ação:" in line:
                                acao = line.split(":")[1].strip()
                            elif "Modo:" in line:
                                modo = line.split(":")[1].strip()
                            elif "Cluster:" in line:
                                cluster = line.split(":")[1].strip()
                            elif "Ambiente:" in line:
                                ambiente = line.split(":")[1].strip()
                            elif "Selecionados:" in line:
                                selecionados = line.split(":")[1].strip()

                    builds.append({
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
                        'selecionados': selecionados
                    })

        return jsonify({'builds': builds}), 200
    except Exception as e:
        return jsonify({'message': f'Ocorreu um erro: {e}'}), 500
