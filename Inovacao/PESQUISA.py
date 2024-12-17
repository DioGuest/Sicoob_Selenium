import requests

def obter_maquinas_producao():
    # URL do endpoint
    url = "https://delivery.sicoob.com.br/sicoob-entrega-continua/configuracoes-clusters?count=1000&page=1"
    
    # Fazendo a requisição ao endpoint
    response = requests.get(url)
    data = response.json()
    
    # Variável para guardar os dados filtrados
    clusters_maquinas_producao = []
    
    # Iterando sobre os clusters
    for cluster in data["resultado"]["dados"]:
        nome_cluster = cluster.get("nomeCluster")
        
        # Filtrando hosts com ambiente PRODUCAO
        hosts_producao = [host.get("hostname") for host in cluster.get("hosts", []) if host.get("ambiente") == "PRODUCAO"]
        
        if hosts_producao:
            clusters_maquinas_producao.append({
                "nomeCluster": nome_cluster,
                "hostsProducao": hosts_producao
            })
    
    return clusters_maquinas_producao

# Chamando a função e armazenando o resultado em uma variável
maquinas_producao = obter_maquinas_producao()

# Exibindo os dados armazenados
for cluster in maquinas_producao:
    print(f"Nome do Cluster: {cluster['nomeCluster']}")
    print("Máquinas de PRODUCAO:")
    for host in cluster["hostsProducao"]:
        print(f"- Hostname: {host}")
    print("\n" + "-"*40 + "\n")
