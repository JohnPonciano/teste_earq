import os
import time
import csv
import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BacenScraper:
    def __init__(self):
        """Initialize the BacenScraper class"""
        self.data = []
        self.setup_driver()
        
    def setup_driver(self):
        """Setup and configure Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        
        # Adicionar headers extras
        chrome_options.add_argument('--accept-language=pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
        chrome_options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8')
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Definir tamanho da janela
        self.driver.set_window_size(1920, 1080)
        
        # Modificar o webdriver para evitar detecção
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def wait_for_page_load(self):
        """Wait for the page to be fully loaded"""
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            time.sleep(5)  # Aumentar o tempo de espera
            
            # Verificar se a página carregou corretamente
            body = self.driver.find_element(By.TAG_NAME, "body")
            if not body.text.strip():
                print("Página parece estar vazia, aguardando mais...")
                time.sleep(5)
        except Exception as e:
            print(f"Erro ao aguardar carregamento da página: {str(e)}")
    
    def scrape_dolar_ptax(self):
        """Scrape Dollar PTAX data from the BACEN website"""
        print("Obtendo cotação do Dólar PTAX...")
        
        try:
            url = "https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do"
            self.driver.get(url)
            
            print("Aguardando página carregar...")
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            
            # Encontrar a tabela diretamente
            table = self.driver.find_element(By.TAG_NAME, "table")
            print("Tabela encontrada")
            
            # Encontrar a linha com os dados
            row = table.find_element(By.CLASS_NAME, "fundoPadraoBClaro2")
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 3:
                data = cells[0].text.strip()
                compra = cells[1].text.strip().replace(',', '.')
                venda = cells[2].text.strip().replace(',', '.')
                
                self.data.append({
                    'date': data,
                    'currency': 'USD',
                    'buy_rate': compra,
                    'sell_rate': venda,
                    'source': url
                })
                
                print(f"Dólar PTAX: Data: {data}, Compra: {compra}, Venda: {venda}")
                return True
            else:
                print("Linha não tem células suficientes")
                
        except Exception as e:
            print(f"Erro ao obter Dólar PTAX: {str(e)}")
            
        return False
    
    def scrape_api_data(self):
        """Scrape data from the BACEN API"""
        print("Obtendo dados da API do BACEN...")
        
        try:
            url = "https://www.bcb.gov.br/api/servico/sitebcb/indicadorCambio"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # Filtrar apenas cotações do tipo "Fechamento"
                fechamento_data = [item for item in data['conteudo'] if item['tipoCotacao'] == 'Fechamento']
                
                for item in fechamento_data:
                    # Converter data para o formato dd/mm/yyyy
                    data_indicator = datetime.strptime(item['dataIndicador'], "%Y-%m-%dT%H:%M:%SZ")
                    data_formatada = data_indicator.strftime("%d/%m/%Y")
                    
                    # Determinar a moeda
                    currency = 'USD' if item['moeda'] == 'Dólar' else 'EUR'
                    
                    self.data.append({
                        'date': data_formatada,
                        'currency': currency,
                        'buy_rate': str(item['valorCompra']),
                        'sell_rate': str(item['valorVenda']),
                        'source': url
                    })
                    
                    print(f"{currency} PTAX (API): Data: {data_formatada}, Compra: {item['valorCompra']}, Venda: {item['valorVenda']}")
                
                return True
            else:
                print(f"Erro ao acessar a API: Status code {response.status_code}")
                
        except Exception as e:
            print(f"Erro ao obter dados da API: {str(e)}")
            
        return False
        
    def save_to_csv(self):
        """Save the scraped data to a CSV file"""
        if not self.data:
            print("Nenhum dado disponível para salvar")
            return
            
        filename = "cotacoes_ptax.csv"
        fieldnames = ['date', 'currency', 'buy_rate', 'sell_rate', 'source']
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.data)
                
            print(f"Dados salvos com sucesso no arquivo: {filename}")
            
        except Exception as e:
            print(f"Erro ao salvar dados no arquivo CSV: {str(e)}")
            
    def close(self):
        """Close the WebDriver"""
        self.driver.quit()
        
    def main(self):
        """Main function to orchestrate the scraping process"""
        try:
            # Tentar obter dados do Dólar PTAX do site
            self.scrape_dolar_ptax()
            
            # Tentar obter dados da API (Dólar e Euro)
            self.scrape_api_data()
            
            # Salvar os dados obtidos
            self.save_to_csv()
            print("\nProcesso concluído com sucesso!")
        
        except Exception as e:
            print(f"Erro durante a execução do script: {str(e)}")
        
        finally:
            self.close()
        
def main():
    scraper = BacenScraper()
    scraper.main()
        
if __name__ == "__main__":
    main() 