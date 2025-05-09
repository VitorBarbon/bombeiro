import json
import sqlite3
from colorama import Fore, Style
from clients.models.client import ClientDB
from project.utils import paths
from typing import Dict, Any, Optional


class StorageClient:
    def __init__(self, file_path: str = paths.DATA_DIR / 'clients.db') -> None:
        self.file_path: str = file_path
    
    def __repr__(self) -> str:
        return f'StorageClient(file_path={self.file_path})'
    
    def add_client(self, client: ClientDB) -> None:
        try:
            client_data: Dict[str, Any] = {
                'name': client.name,
                'email': client.email,
                'phone': client.phone,
                'address': client.address,
                'occupation': client.occupation,
                'city_hall_service': client.city_hall_service,
                'fire_department_service': client.fire_department_service
            }
            
            print(type(client_data))
            print(type(client))
            print(client_data)
            conn: sqlite3.Connection = sqlite3.connect(self.file_path)
            cursor: sqlite3.Cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO clients (
                    name, email, phone, address, occupation,
                    city_hall_service, fire_department_service
                )
                VALUES (?, ?, ?, ?, ?, ?, ?) 
                ''', (
                    client_data["name"],
                    client_data["email"],
                    client_data["phone"],
                    client_data["address"],
                    client_data["occupation"],
                    # json.dumps(client_data["city_hall_service"]) \
                    #     if client_data["city_hall_service"] else None,
                    # json.dumps(client_data["fire_department_service"]) \
                    #     if client_data["fire_department_service"] else None
                ))
            
            conn.commit()
            conn.close()
            print(f'Cliente {client.name} adicionado com sucesso.')
        except sqlite3.Error as e:
            print(Fore.RED + f'Error while adding client to database: {e}' + Style.RESET_ALL)
