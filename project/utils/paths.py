from pathlib import Path

# Caminho base: raiz do projeto (ajuste conforme a localização deste arquivo)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Diretórios
DOCS_DIR = BASE_DIR / 'docs'
DATA_DIR = BASE_DIR / 'data'
CLIENTS_DIR = BASE_DIR / 'clients'
UI_DIR = BASE_DIR / 'ui'
REPORTS_DIR = BASE_DIR / 'reports'
CERTIFICATES_DIR = BASE_DIR / 'certificates'

# Arquivos JSON
CATEGORIAS_JSON = DOCS_DIR / 'categorias.json'
TIPOS_CLIENTE_JSON = DOCS_DIR / 'tipos_cliente.json'
MUNICIPIOS_JSON = DOCS_DIR / 'municipios.json'
ESTADOS_JSON = DOCS_DIR / 'estados.json'

CLIENTES_JSON = CLIENTS_DIR / 'clients.json'
MEMORIAIS_JSON = REPORTS_DIR / 'reports.json'
CERTIFICADOS_JSON = CERTIFICATES_DIR / 'certificates.json'


if __name__ == '__main__':
    ...