import fitz 
import re 
import os 
import json 

palavras_chave = [
    "criação do comitê", "criação do grupo de trabalho", "criação do conselho", "criação do núcleo técnico",
    "instituição do comitê", "instituição do grupo de trabalho", "instituição do conselho", "instituição do núcleo técnico",
    "composição do comitê"
]


pastas_pdfs = "./atas_conselho_de_administração/2012"

resultados = []

def extrair_trechos(texto, palavras):
    encontrados = []
    for palavra in palavras:

        padrao = re.compile(rf".{{0,1000}}{re.escape(palavra)}.{{0,3000}}", re.IGNORECASE)
        matches = padrao.findall(texto) 

        for trecho in matches:
            encontrados.append({
                "palavra_chave": palavra,
                "trecho": trecho.strip()
            })
            

    return encontrados 

for nome_arquivo in os.listdir(pastas_pdfs):

    if nome_arquivo.endswith(".pdf"):
        caminho_pdf = os.path.join(pastas_pdfs, nome_arquivo)
        doc = fitz.open(caminho_pdf)
        texto = ""

        
        for pagina in doc:
            texto += pagina.get_text()
        trechos = extrair_trechos(texto, palavras_chave)

        if trechos:
            for item in trechos:
                resultados.append({
                    "arquivo": nome_arquivo,
                    "palavra_chave": item["palavra_chave"],
                    "trecho": item["trecho"]
                })
        else: 
            resultados.append({
                "arquivo": nome_arquivo,
                "palavra_chave": "Nenhuma encontrada",
                "trecho": "Nenhum trecho com as palavras-chaves foi encontrado nesse arquivo"
            })
        
        doc.close()

with open ("resultados_extraidos.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

for item in resultados:
    print(f"\nArquivo: {item['arquivo']}")
    print(f"Palavra chave: {item['palavra_chave']}")
    print(f"Trecho: {item['trecho']}\n")
    print('----'*50)

   
