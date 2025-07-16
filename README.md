# 🗂️ Boletim Scraper

Este projeto automatiza o download de boletins de serviço da EBSERH (Empresa Brasileira de Serviços Hospitalares) usando Python e Selenium.

## 📌 Objetivo

Realizar o download automatizado de arquivos PDF dos boletins de serviço de anos específicos, acessando os links individuais de cada boletim na página oficial da EBSERH. Atualmente são mais de 2000 boletins e a cada semana é lançado um novo, o objetico inicial desse projeto é realizar o download automatizado e identificar palavras chaves para cada setor. 

## ⚙️ Tecnologias Utilizadas

- **Python 3.12+**
- **Selenium WebDriver**
- **Google Chrome + ChromeDriver**
- **WebDriver Manager** (`webdriver_manager`)
- **tqdm** (barra de progresso)
- **Requests** (usado anteriormente, mas pode ser removido se não for necessário)
- **XPath e CSS Selectors** para localizar os elementos


## 📥 Requisitos
Google Chrome instalado

Python 3.12+

Conexão com a internet para baixar os drivers via webdriver-manager

## 🛠️ Funcionalidades Automatizadas 
Aceita cookies automaticamente

Acessa a página principal do ano escolhido

Visita cada boletim individualmente

Localiza e clica no botão de download de arquivos .pdf

Evita duplicatas verificando arquivos existentes

## 🧪 Futuras Melhorias
- [] Adicionar suporte para múltiplos anos em um único run

- [] Mapear palavras chaves de cada boletim 

- [] Manipular os dados para criação de uma planilha com as palavras mapeadas 

- [] Projetar uma estrutura de armazenamento de dados e máquinas virtuais para acompanhamento semanal 

- [] Logging mais detalhado

- [] Testes automatizados

- [] Interface Web para facilitar uso por não-programadores

## 📄 Licença
Este projeto é livre para uso acadêmico e pessoa
