from typing import Dict, List, Optional, Tuple
from certificates.certificate_creator import Certificate, TEMPLATE_DIR
from certificates.create_template_xlsx import create_template
from certificates.extract_data_xlsx import extract_data_from_xlsx
from project.utils import paths

def handle_input() -> str:
    """Exibe o menu e retorna a opção escolhida pelo usuário."""
    options: Dict[str, str] = {
        '1': 'Criar template .xlsx',
        '2': 'Criar certificado',
        '3': 'Sair'
    }
    for key, value in options.items():
        print(f'{key} - {value}')
    return input('Escolha uma opção: ')

def get_workload(level: str) -> str:
    """Retorna a carga horária com base no nível do participante."""
    level = level.lower()
    workloads: Dict[str, str] = {
        'básico': '4',
        'intermediário': '8'
    }
    return workloads.get(level, '16')

def create_certificates() -> None:
    """Cria certificados para os participantes com base nos dados extraídos."""
    client: List[Dict[str, str]]
    participants: List[Dict[str, str]]
    client, participants = extract_data_from_xlsx(paths.CERTIFICATES_DIR / 'templates' / 'template.xlsx')
    certificate = Certificate(TEMPLATE_DIR, paths.CERTIFICATES_DIR)

    for participant in participants:
        workload: str = get_workload(participant['nivel'])
        print(participant['names'], client[0]['date'], workload, client[0]['company'])
        certificate.create_certificate(participant['names'], client[0]['date'], workload, client[0]['company'])

def main() -> None:
    """Função principal que controla o fluxo do programa."""
    actions: Dict[str, callable] = {
        '1': create_template,
        '2': create_certificates
    }

    while True:
        option: str = handle_input()
        if option in actions:
            actions[option]()
        elif option == '3':
            print('Saindo...')
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == '__main__':
    main()