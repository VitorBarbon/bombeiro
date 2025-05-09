import json
import sqlite3

from clients.models.client import Client
from project.utils import paths
from typing import Dict, Any, Optional


class StorageClient:
    def __init__(self, file_path: str = paths.DATA_DIR / 'clients.db') -> None:
        self.file_path: str = file_path
    
    def __repr__(self) -> str:
        return f'StorageClient(file_path={self.file_path})'
    
    def add_client(self, client: Client) -> None:
        try:
            client_data: Dict[str, Any] = {
                **client
            }
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
                    json.dumps(client_data["city_hall_service"].dict()) \
                        if client_data["city_hall_service"] else None,
                    json.dumps(client_data["fire_department_service"].dict()) \
                        if client_data["fire_department_service"] else None
                ))
            
            conn.commit()
            conn.close()
            print(f'Cliente {client.name} adicionado com sucesso.')
        except sqlite3.Error as e:
            print(f'Error while adding client to database: {e}')
