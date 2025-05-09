import sys
from tkinter import Tk, filedialog
from typing import Dict, List
from PySide6.QtWidgets import QApplication

from certificates.certificate_creator import Certificate, TEMPLATE_DIR
from certificates.create_template_xlsx import create_template
from certificates.extract_data_xlsx import extract_data_from_xlsx
from ui.main_window import MainWindow
from project.utils import paths
from clients.models.client import Client, FireDepartmentService, CityHallService
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
    client = Client(
        name='Vitor Barbon 2',
        address='Rua 1, 123 - Bairro - Cidade - SP',
        email='email@email.com',
        phone='(11) 99999-9999',
        occupation='C-2',
        fire_department_service=FireDepartmentService(
            area=100.0,
            fire_load=200.0
        ),
    )
    storage = StorageClient(paths.DATA_DIR / 'clients.jsonl')
    storage.add_client_jsonl(client)
    