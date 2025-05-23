import sys
from tkinter import Tk, filedialog
from typing import Dict, List
from PySide6.QtWidgets import QApplication
from colorama import Fore, Style

from certificates.certificate_creator import Certificate, TEMPLATE_DIR
from certificates.create_template_xlsx import create_template
from certificates.extract_data_xlsx import extract_data_from_xlsx
from ui.main_window import MainWindow
from project.utils import paths
from clients.models.client import ClientDB, FireDepartmentServiceDB, CityHallServiceDB
from clients.storage.storage import StorageClient

def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


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


def selected_folder_and_save() -> str:
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory(title='Escolha a pasta para salvar o Certificado')

    
def create_certificates() -> None:
    """Cria certificados para os participantes com base nos dados extraídos."""
    client: List[Dict[str, str]]
    participants: List[Dict[str, str]]
    client, participants = extract_data_from_xlsx(paths.CERTIFICATES_DIR / 'templates' / 'template.xlsx')
    
    output_dir = selected_folder_and_save()
    certificate = Certificate(TEMPLATE_DIR, output_dir)

    for participant in participants:
        workload: str = get_workload(participant['nivel'])
        print(participant['names'], client[0]['date'], workload, client[0]['company'])
        certificate.create_certificate(participant['names'], client[0]['date'], workload, client[0]['company'])


def create_client() -> None:
    """Cria um novo cliente."""
    client_data = {
        'name': input('Nome do cliente: '),
        'email': input('Email do cliente: '),
        'phone': input('Telefone do cliente: ')
    }
    storage = StorageClient()
    storage.add_client(ClientDB(**client_data))


def create_folder_client() -> None:
    """Cria uma nova pasta para o cliente."""
    client_folder = selected_folder_and_save()
    client_folder.mkdir(parents=True, exist_ok=True)
    print(Fore.GREEN + f'Pasta criada com sucesso: {client_folder}' + Style.RESET_ALL)


def main() -> None:
    """Função principal que controla o fluxo do programa."""
    actions: Dict[str, callable] = {
        '1': create_template,
        '2': create_certificates,
        '3': create_client,
        '4': create_folder_client
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

    # storage = StorageClient()
    # print(*storage.get_all_clients(), sep='\n')
    