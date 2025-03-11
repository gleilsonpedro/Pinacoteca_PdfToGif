# Autor: Gleilson Pedro
# Email: gleilsonsvo@gmail.com
# Descrição: Script para converter PDFs em GIFs.

import os
import time
from datetime import datetime
import fitz  # pymupdf
from PIL import Image, ImageOps
import logging

# Configuração de logging
LOG_FILE = 'pdf_to_gif_converter.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Diretório base onde o código está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretório onde os PDFs são monitorados (o mesmo diretório do script)
PDF_DIR = BASE_DIR

# Diretório onde os GIFs serão armazenados
GIF_DIR = os.path.join(BASE_DIR, 'gifs')

# Intervalo de verificação em segundos (5 minutos)
SCAN_INTERVAL = 300  # 5 minutos * 60 segundos

# DPI para os GIFs (aumentar para melhor legibilidade)
DPI = 100

# Escala para reduzir as dimensões da imagem (ex: 0.9 para reduzir ligeiramente)
SCALE_FACTOR = 0.80

# Número máximo de cores na paleta do GIF
MAX_COLORS = 15 
def create_directories():
    """Cria os diretórios necessários caso não existam."""
    try:
        if not os.path.exists(GIF_DIR):
            os.makedirs(GIF_DIR)
        logging.info("Diretórios criados ou já existentes.")
    except OSError as e:
        logging.error(f"Erro ao criar diretórios: {e}")
        raise

def convert_pdf_to_gif(pdf_path, dpi=DPI, scale_factor=SCALE_FACTOR, max_colors=MAX_COLORS):
    """Converte um PDF em GIF (escala de cinza) e salva no diretório de GIFs usando PyMuPDF."""
    try:
        pdf_filename = os.path.basename(pdf_path)
        gif_filename = os.path.splitext(pdf_filename)[0] + '.gif'
        gif_path = os.path.join(GIF_DIR, gif_filename)

        logging.info(f"Convertendo PDF: {pdf_filename} para GIF: {gif_filename}")

        doc = fitz.open(pdf_path)
        page = doc[0]  # Pega a primeira página
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72)) # Converte para imagem com DPI especificado

        # Converter para PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Converter para escala de cinza
        img = ImageOps.grayscale(img)

        # Escalonar a imagem
        if scale_factor != 1.0:
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS) # Usar um filtro de resampling

        # Reduzir a paleta de cores (mais suave)
        img = img.convert("P", palette=Image.ADAPTIVE, colors=max_colors)

        # Salvar como GIF
        img.save(gif_path, 'GIF', optimize=True)

        doc.close()

        logging.info(f"GIF criado com sucesso: {gif_path}")

        # Deleta o arquivo PDF original
        try:
            os.remove(pdf_path)
            logging.info(f"PDF deletado com sucesso: {pdf_path}")
        except OSError as e:
            logging.error(f"Erro ao deletar PDF: {e}")

        return True

    except Exception as e:
        logging.error(f"Erro ao converter PDF para GIF: {e}")
        return False

def process_pdfs():
    """Procura por PDFs no diretório e os converte."""
    converted_count = 0
    try:
        for filename in os.listdir(PDF_DIR):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(PDF_DIR, filename)
                if convert_pdf_to_gif(pdf_path):
                    converted_count += 1
        logging.info(f"Total de PDFs convertidos nesta iteração: {converted_count}")
        return converted_count
    except Exception as e:
        logging.error(f"Erro ao processar PDFs: {e}")
        return 0

def main():
    """Função principal para executar o script em loop."""
    create_directories()
    logging.info("Iniciando o monitoramento de PDFs...")

    total_converted = 0
    start_time = datetime.now()

    try:
        while True:
            converted = process_pdfs()
            total_converted += converted
            logging.info(f"Aguardando {SCAN_INTERVAL} segundos para a próxima verificação...")
            time.sleep(SCAN_INTERVAL)

    except KeyboardInterrupt:
        logging.info("Script interrompido pelo usuário.")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
    finally:
        end_time = datetime.now()
        duration = end_time - start_time
        logging.info(f"Script finalizado.")
        logging.info(f"Tempo de execução total: {duration}")
        logging.info(f"Total de PDFs convertidos durante a execução: {total_converted}")

if __name__ == "__main__":
    main()