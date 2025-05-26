import subprocess

def extrair_texto_com_pdtotext(pdf_path, caminho_pdftotext):
    # Define o arquivo temporário onde o texto será salvo
    arquivo_saida = "saida_temp.txt"
    
    # Executa o comando para converter PDF em texto
    subprocess.run([caminho_pdftotext, pdf_path, arquivo_saida], check=True)
    
    # Lê o conteúdo do arquivo de saída
    with open(arquivo_saida, 'r', encoding='utf-8') as f:
        texto = f.read()
        
    return texto

# Caminho do seu arquivo PDF
pdf_path = r"C:\Users\Eduarda.Amorim\Desktop\API\PDF Welby.pdf"  # Substitua pelo caminho real
# Caminho completo do pdftotext.exe
caminho_pdftotext = r"C:\Users\Eduarda.Amorim\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin\pdftotext.exe"

# Extrair o texto
texto_extraido = extrair_texto_com_pdtotext(pdf_path, caminho_pdftotext)

# Mostrar o conteúdo extraído (opcional)
print(texto_extraido)

# Aqui você pode chamar sua função para processar o texto
# exemplo: resultados = sua_funcao(texto_extraido)