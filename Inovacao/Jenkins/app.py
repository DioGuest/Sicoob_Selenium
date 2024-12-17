
from Pesquisar_Cluster import Pesquisar
from Restart_Funcoes.Restart_Liberty import restart_liberty
from Restart_Funcoes.Restart_SRTB import restart_SRTB
from Restart_Funcoes.Restart_Websphere import restart_Websphere
from flask import Flask, render_template, request, jsonify


from routes.Pesquisa_CCS import submit
from routes.jenkins_Pesquisa_Whebsphere import jenkins_Whebsphere  # Importa as rotas do Jenkins
from routes.jenkins_Pesquisa_Liberty import jenkins_Liberty
from routes.jenkins_Pesquisa_SRTB import jenkins_SRTB
from routes.restart_routes import restart_bp
from routes.Isolar_Nor import Isolar_Nor
# from routes.Pesquisa_CCS import pesquisaCcs
from routes.Isolar_ENABLE import Habilitar
from routes.SSH_Outofmemory import move_bp
from routes.SSH_Disco_opt import ssh_bp
from routes.RestartCompleto import RestartCompleto
from routes.RestartCompleto_SEGUENCIAL import RestartCompleto_SEGUENCIAL
import concurrent.futures
import logging
import time
from flask import Flask, request


app = Flask(__name__)

# Registra o Blueprint das rotas do Jenkins
app.register_blueprint(jenkins_Whebsphere)
# Registra o Blueprint das rotas de reinício
app.register_blueprint(restart_bp)

app.register_blueprint(jenkins_Liberty)

app.register_blueprint(jenkins_SRTB)

app.register_blueprint(Isolar_Nor)

app.register_blueprint(Habilitar)

# app.register_blueprint(pesquisaCcs)

app.register_blueprint(ssh_bp)

app.register_blueprint(move_bp)

app.register_blueprint(RestartCompleto)

app.register_blueprint(RestartCompleto_SEGUENCIAL)







from Pesquisar_Cluster import Pesquisar
from Restart_Funcoes.Restart_Liberty import restart_liberty
from Restart_Funcoes.Restart_SRTB import restart_SRTB
from Restart_Funcoes.Restart_Websphere import restart_Websphere
from flask import Flask, render_template, request, jsonify

from routes.jenkins_Pesquisa_Whebsphere import jenkins_Whebsphere
from routes.jenkins_Pesquisa_Liberty import jenkins_Liberty
from routes.jenkins_Pesquisa_SRTB import jenkins_SRTB
from routes.restart_routes import restart_bp
from routes.Isolar_Nor import Isolar_Nor
from routes.Isolar_ENABLE import Habilitar
from routes.SSH_Outofmemory import move_bp
from routes.SSH_Disco_opt import ssh_bp
from routes.RestartCompleto import RestartCompleto
from routes.RestartCompleto_SEGUENCIAL import RestartCompleto_SEGUENCIAL
import schedule
import threading
import time

from routes.envioTeams import main

# Inicializa a aplicação Flask
app = Flask(__name__)

# Registra os Blueprints
app.register_blueprint(jenkins_Whebsphere)
app.register_blueprint(restart_bp)
app.register_blueprint(jenkins_Liberty)
app.register_blueprint(jenkins_SRTB)
app.register_blueprint(Isolar_Nor)
app.register_blueprint(Habilitar)
app.register_blueprint(ssh_bp)
app.register_blueprint(move_bp)
app.register_blueprint(RestartCompleto)
app.register_blueprint(RestartCompleto_SEGUENCIAL)



# # Função para agendar tarefas
# def agendar_submit():
#     schedule.every(1).hours.do(submit)  # Executa a função `submit()` a cada 1 hora
    
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# # Executa o agendamento em uma thread separada
# threading.Thread(target=agendar_submit, daemon=True).start()

# main()

# Função para agendar tarefas
def agendar_submit():
    submit()  # Executa imediatamente quando o projeto for iniciado
    
    # Agora, agendar a função para ser executada a cada 10 minutos
    schedule.every(10).minutes.do(submit)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Executa o agendamento em uma thread separada para não bloquear o fluxo principal
threading.Thread(target=agendar_submit, daemon=True).start()


if __name__ == '__main__':
    app.run(debug=False, port=8080, host='0.0.0.0')


# # if __name__ == '__main__':
# #     app.run(debug=False, port=8080)  # Definindo a porta aqui


