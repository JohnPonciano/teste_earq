# Script de Cotações PTAX

Este script obtém as cotações PTAX do Dólar e Euro do Banco Central do Brasil (BACEN) através de múltiplas fontes.

## Processo de Investigação

A descoberta das fontes de dados foi feita através de uma análise detalhada dos sites do BACEN:

1. **Investigação do Dólar PTAX**:
   - Inicialmente acessei `https://www.bcb.gov.br/estabilidadefinanceira/fechamentodolar`
   - Ao analisar o HTML, descobri que a página principal usa um iframe
   - ![Página principal com iframe](/public/img1.png)
   - O iframe aponta para uma página mais simples: `https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do`
   ![Página do iframe sem proteções](/public/img2.png)
   - Esta página secundária não possui proteções contra web scraping
   

2. **Investigação do Euro PTAX**:
   - Acessei `https://www.bcb.gov.br/`
   - Analisei as requisições de rede do site
   ![Requisições da API](/public/img3.png)
   - Descobri uma API pública: `https://www.bcb.gov.br/api/servico/sitebcb/indicadorCambio`
   ![Resposta da API](/public/img4.png)
   - A API retorna dados tanto do Dólar quanto do Euro PTAX
   

## Funcionalidades

- Obtém a cotação PTAX do Dólar de duas fontes diferentes:
  1. Web scraping do site do BACEN
  2. API direta do BACEN
- Obtém a cotação PTAX do Euro através da API direta do BACEN
- Salva os dados em um arquivo CSV com as seguintes informações:
  - Data da cotação
  - Moeda (USD/EUR)
  - Taxa de compra
  - Taxa de venda
  - Fonte dos dados

## Fontes de Dados

O script utiliza as seguintes fontes para obter os dados:

1. **Dólar PTAX (Fonte 1)**:
   - URL: `https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do`
   - Método: Web scraping

2. **Dólar PTAX (Fonte 2) e Euro PTAX**:
   - URL: `https://www.bcb.gov.br/api/servico/sitebcb/indicadorCambio`
   - Método: API direta
   - Filtro: Apenas cotações do tipo "Fechamento"

## Requisitos

- Python 3.x
- Selenium
- Chrome WebDriver
- Requests

## Instalação

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Certifique-se de ter o Chrome WebDriver instalado e no PATH do sistema

## Uso

Execute o script com:
```bash
python cotacao_bacen.py
```

O script irá:
1. Obter a cotação do Dólar PTAX do site do BACEN
2. Obter as cotações do Dólar e Euro PTAX da API do BACEN
3. Salvar todos os dados no arquivo `cotacoes_ptax.csv`

## Formato do CSV

O arquivo CSV gerado contém as seguintes colunas:
- `date`: Data da cotação (formato: DD/MM/YYYY)
- `currency`: Moeda (USD para Dólar, EUR para Euro)
- `buy_rate`: Taxa de compra
- `sell_rate`: Taxa de venda
- `source`: URL da fonte dos dados

## Observações

- O script utiliza web scraping para a primeira fonte do Dólar PTAX e API direta para a segunda fonte
- A API do BACEN fornece dados tanto para o Dólar quanto para o Euro PTAX
- Os dados são filtrados para incluir apenas cotações do tipo "Fechamento"
- O script verifica a consistência dos dados obtidos das diferentes fontes
## Manutenção

Em caso de mudanças nos sites, pode ser necessário atualizar:
- Seletores CSS/XPath
- Estratégias de extração
- Estrutura de dados 