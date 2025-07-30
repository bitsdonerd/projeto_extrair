import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm

class BoletimScraper:
    def __init__(self, url_ano, pasta_destino):
        self.url_ano = url_ano
        self.pasta_destino = pasta_destino
        os.makedirs(pasta_destino, exist_ok=True)
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        # options.add_argument("--headless")  
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.abspath(self.pasta_destino),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True  
        })
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def iniciar(self):
        try:
            self.driver.get(self.url_ano)

            try:
                aceitar_cookies = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ACEITAR', 'aceitar'), 'aceitar')]"))
                )
                aceitar_cookies.click()
                print("[i] Cookies aceitos")
            except TimeoutException:
                print("[i] Nenhum aviso de cookies encontrado")

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'Ata - Conselho de Administração nº')]"))
            )

            atas = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Ata - Conselho de Administração nº')]")
            links_atas = [b.get_attribute("href") for b in atas]
            print(f"[i] Encontradas {len(links_atas)} atas")

            for link in tqdm(links_atas, desc="Atas"):
                self._baixar_pdf_das_atas(link)

        finally:
            self.driver.quit()
            print("\n✅ Todos as atas foram processadas.")

    def _baixar_pdf_das_atas(self, link_atas):
        try:
            self.driver.get(link_atas)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '@@download/file')]"))
            )
            
            pdf_element =self.driver.find_element(By.XPATH, "//a[contains(@href, '@@download/file')]")
            link_pdf = pdf_element.get_attribute("href")
            nome_arquivo = link_pdf.split("/")[-1]
            caminho_arquivo = os.path.join(self.pasta_destino, nome_arquivo)

            if os.path.exists(caminho_arquivo):
                print(f"[*] Arquivo já existe: {nome_arquivo}")
                return

            pdf_element.click()
            print(f"[↓] Baixando: {nome_arquivo}")
            self._aguardar_download(nome_arquivo)

        except TimeoutException:
            print(f"[!] Timeout ao acessar ata: {link_atas}")
        except Exception as e:
            print(f"[!] Erro ao processar ata {link_atas}: {e}")
        
    def _aguardar_download(self, nome_arquivo, timeout=30):
        """Espera o Chrome terminar o download do arquivo .crdownload"""
        caminho_arquivo_temp = os.path.join(self.pasta_destino, nome_arquivo + ".crdownload")
        caminho_arquivo_final = os.path.join(self.pasta_destino, nome_arquivo)

        tempo_inicial = time.time()
        while time.time() - tempo_inicial < timeout:
            if os.path.exists(caminho_arquivo_final) and not os.path.exists(caminho_arquivo_temp):
                print(f"[✓] Download concluído: {nome_arquivo}")
                return
            time.sleep(1)

        print(f"[!] Timeout aguardando download: {nome_arquivo}")

if __name__ == "__main__":
    scraper = BoletimScraper(
        url_ano="https://www.gov.br/ebserh/pt-br/governanca/conselhos/conselho-de-administracao/atas-do-conselho-de-administracao/2025?b_start:int=0",
        pasta_destino="2025"
    )
    scraper.iniciar()

