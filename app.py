from flask import Flask, request, jsonify
import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simulação de banco de dados de imóveis
imoveis_db = {
    "IMV123": {
        "id": "IMV123",
        "endereco": "Rua das Flores, 123",
        "valor_aluguel": "1.500,00",
        "condominio": "R$ 300,00",
        "situacao": "Disponível"
    },
    "IMV456": {
        "id": "IMV456",
        "endereco": "Av. Brasil, 456",
        "valor_aluguel": "2.300,00",
        "condominio": "R$ 450,00",
        "situacao": "Alugado"
    }
}

# Função para extrair texto de PDF escaneado usando OCR
def extrair_texto_ocr(pdf_path):
    texto_completo = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap()
            image_path = os.path.join(UPLOAD_FOLDER, "temp_page.png")
            pix.save(image_path)

            image = Image.open(image_path)
            texto = pytesseract.image_to_string(image, lang='por')
            texto_completo += texto + "\n"
            os.remove(image_path)
    return texto_completo

# Função para extrair dados do texto
def extrair_dados(texto):
    match = re.search(r"ID do Imóvel[:\s]*([A-Za-z0-9]+)", texto)
    id_imovel = match.group(1) if match else "Não encontrado"
    aluguel_match = re.search(r"Aluguel\s*-\s*([\d\.,]+)", texto)
    valor_aluguel = aluguel_match.group(1) if aluguel_match else "Não encontrado"
    
    return {
        "id_imovel": id_imovel,
        "valor_aluguel": valor_aluguel,
        "resumo": texto[:300]
    }

@app.route('/extrair_dados_pdf', methods=['POST'])
def extrair_dados_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "Arquivo PDF não enviado"}), 400

    arquivo = request.files['pdf']
    caminho_pdf = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_pdf)

    try:
        texto = extrair_texto_ocr(caminho_pdf)
        dados_extraidos = extrair_dados(texto)
        return jsonify(dados_extraidos)
    finally:
        os.remove(caminho_pdf)

@app.route('/consultar_imovel/<id_imovel>', methods=['GET'])
def consultar_imovel(id_imovel):
    imovel = imoveis_db.get(id_imovel)
    if imovel:
        return jsonify(imovel)
    return jsonify({"error": "Imóvel não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
