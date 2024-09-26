# Ponderada de Programação do Módulo 7

## Execução:

Para executar o programa, caso o Docker já esteja instalado, basta abrir um terminal e executar 
```
docker-compose up
```
Após a configuração dos containers, basta entrar na página "http://localhost:8501" no navegador de sua escolha

OBS: o programa usa as portas 8000 e 8501, portanto, é necessário que ambas as portas estejam disponíveis

## Exploração dos dados:

A ánalise feita nos dados e a justificativa da escolha do modelo se encontra no arquivo "analise_dados.ipynb"

## Organização do repositório:
```
├── docker-compose.yml
├── analise_dados.ipynb
├── .gitignore
├── README.md
├── frontend/
│   ├── Dockerfile
│   ├── front.py
│   └── requirements.txt
└── backend/
    ├── Dockerfile
    ├── info.json
    ├── logs.json
    ├── retrain.json
    ├── modelCreator.py
    ├── app.py
    ├── requirements.txt
    └── models/
        ├── BTC-USD.h5
        └── ETH-USD.h5
```
