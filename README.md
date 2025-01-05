# Análise de Impacto das Visualizações de Vídeos no YouTube sobre o Mercado de Ações

Este projeto tem como objetivo analisar a relação entre as visualizações de vídeos no YouTube e o desempenho do mercado de ações de empresas específicas, como Sony, Nvidia, Microsoft, Dell, IBM e Intel. A análise busca identificar como a exposição digital através de vídeos pode influenciar o crescimento das organizações e o valor de suas ações no mercado financeiro.

## Tecnologias Utilizadas

- **PySpark:** Framework para processamento distribuído de grandes volumes de dados.
- **MongoDB:** Banco de dados NoSQL utilizado para armazenar dados em formato JSON.
- **Streamlit:** Biblioteca para criação de dashboards interativos e visualizações dinâmicas.
- **Docker:** Contêineres utilizados para encapsular o MongoDB e o Jupyter Notebook, facilitando a execução em diferentes ambientes.

## Como Rodar o Projeto

### Pré-requisitos

- Python 3.x
- MongoDB
- Docker (para rodar containers)
- Streamlit

### Passos

1. **Configuração do Ambiente:**
   - Clone este repositório para sua máquina local.
   - Da run ao seguinte comando na diretoria do projeto
   ```bash
   docker-compose up --build
   ```
   - Instale as dependências necessárias utilizando o seguinte comando:
     ```bash
     pip install -r requirements.txt
     ```

2. **Inicie o Dashboard Streamlit:**
   - Para visualizar os resultados, inicie o Streamlit:
     ```bash
     streamlit run app.py
     ```
