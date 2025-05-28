from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import pytesseract
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extrair_texto_pdf(pdf_path):
    texto_completo = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            texto_completo += page.get_text()
    return texto_completo

def extrair_dados(texto):
    # Aqui você pode implementar sua lógica de extração de dados
    # Exemplo básico: buscar por palavras-chave ou padrões
    # Para fins de exemplo, vamos retornar o texto completo
    return {"texto_extraido": texto}

@app.route('/extrair_dados_pdf', methods=['POST'])
def extrair_dados_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "Arquivo PDF não enviado"}), 400

    arquivo = request.files['pdf']
    caminho_pdf = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_pdf)

    try:
        texto = extrair_texto_pdf(caminho_pdf)
        dados_extraidos = extrair_dados(texto)
        return jsonify(dados_extraidos)
    finally:
        os.remove(caminho_pdf)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)