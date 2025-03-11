# PDF to GIF Converter

Este script Python monitora um diretório em busca de arquivos PDF e os converte em GIFs. Após a conversão, o script exclui o arquivo PDF original. O script usa as bibliotecas `PyMuPDF` e `Pillow` para realizar a conversão.

## Pré-requisitos

Antes de executar o script, certifique-se de ter os seguintes requisitos instalados:

*   Python 3.6 ou superior
*   `PyMuPDF`
*   `Pillow`


Por padrão, o script monitora o diretório onde ele está localizado (BASE_DIR) em busca de PDFs.

Os GIFs convertidos são salvos em um subdiretório chamado gifs dentro do mesmo diretório do script.

Se você quiser alterar esses diretórios, edite as seguintes variáveis no script:

# Diretório onde os PDFs são monitorados (o mesmo diretório do script)
PDF_DIR = BASE_DIR

# Diretório onde os GIFs serão armazenados
GIF_DIR = os.path.join(BASE_DIR, 'gifs')

Configure os parâmetros de conversão (opcional):

Edite as seguintes variáveis no script para ajustar os parâmetros de conversão:

# DPI para os GIFs (aumentar para melhor legibilidade)
DPI = 150

# Escala para reduzir as dimensões da imagem (ex: 0.9 para reduzir ligeiramente)
SCALE_FACTOR = 0.9

# Número máximo de cores na paleta do GIF
MAX_COLORS = 128 # Ajuste conforme necessário

DPI: Define a resolução (dots per inch) dos GIFs gerados. Aumente para melhor legibilidade, diminua para reduzir o tamanho do arquivo.

SCALE_FACTOR: Um valor menor que 1 reduz as dimensões da imagem antes da conversão.

MAX_COLORS: Limita o número de cores no GIF, o que pode reduzir o tamanho do arquivo.


O script será executado em um loop infinito, monitorando o diretório especificado em busca de arquivos PDF.

Log

O script registra informações sobre a conversão em um arquivo de log chamado pdf_to_gif_converter.log. Este arquivo contém informações sobre:

A data e hora de cada conversão

O nome dos arquivos PDF convertidos

O local dos GIFs gerados

Quaisquer erros que ocorram durante a conversão

Interrupção

Para interromper o script, pressione Ctrl+C no terminal.

Autoria

Este script foi criado por [Gleilson Pedro] ([gleilsonsvo@gmail.com]).

Licença

Este script é distribuído sob a licença [MIT License] (ou a licença que você escolher). Consulte o arquivo LICENSE para obter mais informações.

Disclaimer

Lembre-se de que este script exclui os arquivos PDF originais após a conversão. Certifique-se de ter um backup dos seus arquivos PDF antes de executar o script ou comente as linhas de código responsáveis pela exclusão, caso deseje mantê-los.

# Deleta o arquivo PDF original
    try:
        os.remove(pdf_path)
        logging.info(f"PDF deletado com sucesso: {pdf_path}")
    except OSError as e:
        logging.error(f"Erro ao deletar PDF: {e}")
