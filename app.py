import fitz  # PyMuPDF
import os

def extrair_repasses_pdf(caminho_arquivo, exportar=False):
    # Verifica se o arquivo existe antes de abrir
    if not os.path.isfile(caminho_arquivo):
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return

    doc = fitz.open(caminho_arquivo)
    texto_completo = ""

    for pagina in doc:
        texto_completo += pagina.get_text()

    # Aqui você coloca a lógica de extração dos repasses do texto
    # Exemplo simples: só printar o texto extraído
    print("=== Conteúdo extraído do PDF ===")
    print(texto_completo)
    print("=== Fim do conteúdo ===")

    # Se quiser exportar para arquivo txt
    if exportar:
        nome_arquivo_saida = os.path.splitext(caminho_arquivo)[0] + "_extraido.txt"
        with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
            f.write(texto_completo)
        print(f"Conteúdo exportado para: {nome_arquivo_saida}")

if __name__ == "__main__":
    # Configure o caminho do PDF aqui:
    caminho_pdf = r"C:\Users\Eduarda.Amorim\Desktop\API\PDF Welby.pdf"

    extrair_repasses_pdf(caminho_pdf, exportar=False)
