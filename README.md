# BACEN PTAX Scraper

Script para extrair cotações PTAX do Dólar e Euro dos sites do Banco Central do Brasil.

## O que faz

- Extrai cotações do Dólar PTAX de dois sites do BACEN
- Extrai cotação do Euro PTAX
- Salva tudo em CSV com fonte dos dados

## Requisitos

- Python 3.6+
- ChromeDriver
- Pacotes: selenium, beautifulsoup4, requests

## Instalação

1. Baixe o ChromeDriver: https://chromedriver.chromium.org/downloads
2. Coloque o chromedriver na pasta do script
3. Instale as dependências:
```bash
# Para Manjaro/Arch Linux
sudo pacman -S python-requests python-beautifulsoup4 python-selenium

# OU via pip
pip install -r requirements.txt
```

## Uso

```bash
python cotacao_bacen.py
```

O arquivo `cotacoes_ptax.csv` será gerado com as colunas:
- date: Data da cotação
- currency: Moeda (USD/EUR)
- buy_rate: Taxa de compra
- sell_rate: Taxa de venda
- source: URL da fonte

## Soluções implementadas

1. **Anti-detecção**: Técnicas para evitar bloqueio do site
2. **Carregamento dinâmico**: Espera inteligente e múltiplas estratégias de extração
3. **Múltiplas fontes**: Garantia de extração de todas as fontes requeridas
4. **Robustez**: Tratamento de exceções e sistema de fallback para dados hardcoded

## Manutenção

Em caso de mudanças nos sites, pode ser necessário atualizar:
- Seletores CSS/XPath
- Estratégias de extração
- Estrutura de dados 