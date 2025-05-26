import requests

url = 'http://127.0.0.1:5000/extrair_imoveis_ocr_api'
pdf_path = 'C:/Users/Eduarda.Amorim/Desktop/API/PDF Welby.pdf'  # Verifique se o caminho está certo

with open(pdf_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

print("Código de status:", response.status_code)

try:
    print("Resposta:", response.json())
except Exception as e:
    print("Erro ao converter resposta em JSON:", e)
    print("Conteúdo bruto da resposta:", response.text)
