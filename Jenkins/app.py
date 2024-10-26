from Pesquisar_Cluster import Pesquisar
from Restart_Funcoes.Restart_Liberty import restart_liberty
from Restart_Funcoes.Restart_SRTB import restart_SRTB
from Restart_Funcoes.Restart_Websphere import restart_Websphere
from flask import Flask, render_template, request, jsonify
from routes.jenkins_Pesquisa_Whebsphere import jenkins_Whebsphere  # Importa as rotas do Jenkins
from routes.jenkins_Pesquisa_Liberty import jenkins_Liberty
from routes.jenkins_Pesquisa_SRTB import jenkins_SRTB
from routes.restart_routes import restart_bp
from routes.Isolar_Nor import Isolar_Nor
from routes.Pesquisa_CCS import pesquisaCcs
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

app.register_blueprint(pesquisaCcs)

app.register_blueprint(ssh_bp)

app.register_blueprint(move_bp)

app.register_blueprint(RestartCompleto)

app.register_blueprint(RestartCompleto_SEGUENCIAL)








if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')

# # if __name__ == '__main__':
# #     app.run(debug=False, port=8080)  # Definindo a porta aqui


