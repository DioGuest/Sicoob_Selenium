import requests
from flask import jsonify

def restart_SRTB(Modo, valor_cluster, valor_codigo, Login, Senha):
    jenkins_url = 'https://deploy.sicoob.com.br/view/OperacoesTI/job/Restart/job/SRTB/job/restart-srtb/buildWithParameters'


    # Debug: Imprimir parâmetros antes de enviar
    print({
        'ACTION': 'RESTART',
        'MODE': Modo,
        'NOMECLUSTER': valor_cluster,  # Este campo foi corrigido
        'AMBIENTE': 'PRODUCAO',
        'SELECIONADOS': valor_codigo
    })

    try:
        # Enviar request para Jenkins
        response = requests.post(
            jenkins_url,
            params={
                'ACTION': 'RESTART',
                'MODE': Modo,
                'NOMECLUSTER': valor_cluster,  # Use o nome correto aqui
                'AMBIENTE': 'PRODUCAO',
                'SELECIONADOS': valor_codigo
            },
            auth=(Login, Senha)
        )

        if response.status_code == 201:
            return f"Build iniciado com sucesso para o código {valor_codigo}! (Status: {response.status_code})<br>"
        else:
            return f"Erro ao iniciar o build para o código {valor_codigo}: {response.status_code}<br>"
    except Exception as e:
        return f"Ocorreu um erro ao iniciar o build para o código {valor_codigo}: {e}<br>"