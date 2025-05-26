from flask import Flask, request, jsonify
import os
import subprocess
import re

app = Flask(__name__)

# Caminho do seu pdftotext.exe (conforme informado)
PDFTOTEXT_PATH = r"C:\Users\Eduarda.Amorim\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin\pdftotext.exe"

# Pasta para uploads temporários
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Função para extrair texto do PDF usando seu caminho do pdftotext.exe
def extrair_texto_pdf(pdf_path):
    temp_txt = "temp_texto.txt"
    try:
        subprocess.run([PDFTOTEXT_PATH, pdf_path, temp_txt], check=True)
        with open(temp_txt, 'r', encoding='utf-8') as f:
            texto = f.read()
        return texto
    except subprocess.CalledProcessError:
        return None
    finally:
        if os.path.exists(temp_txt):
            os.remove(temp_txt)

# Função para extrair imóveis do texto extraído
def extrair_imoveis(texto):
    imoveis = []
    # Divide por "Contrato" para pegar cada imóvel
    contratos = re.split(r"Contrato", texto)
    for contrato in contratos[1:]:
        # Extração de exemplo: valor do aluguel
        aluguel_match = re.search(r"Aluguel\s*-\s*([\d\.,]+)", contrato)
        valor_aluguel = aluguel_match.group(1) if aluguel_match else "Valor não encontrado"
        # Pode adicionar mais extrações aqui
        imoveis.append({
            "descricao": contrato[:200],  # descrição resumida
            "valor_aluguel": valor_aluguel
        })
    return imoveis

@app.route('/extrair_imoveis', methods=['POST'])
def extrair_imoveis_api():
    # Recebe o arquivo enviado
    if 'pdf' not in request.files:
        return jsonify({"error": "Arquivo PDF não enviado"}), 400

    arquivo = request.files['pdf']
    if arquivo.filename == '':
        return jsonify({"error": "Arquivo vazio"}), 400

    # Salva o arquivo enviado
    caminho_pdf = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_pdf)

    try:
        # Extrai o texto usando seu método
        texto = extrair_texto_pdf(caminho_pdf)
        if texto is None:
            return jsonify({"error": "Falha na extração do texto"}), 500

        # Processa o texto para obter imóveis
        imoveis = extrair_imoveis(texto)

        # Retorna os imóveis em JSON
        return jsonify({"imoveis": imoveis})
    finally:
        # Apaga o arquivo PDF enviado após processamento
        os.remove(caminho_pdf)

if __name__ == '__main__':
    # Executa a API
    app.run(debug=True)