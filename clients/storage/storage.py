import json
from clients.models.client import Client
from project.utils import paths


class StorageClient:
    def __init__(self, file_path: str = paths.DATA_DIR / 'clients.jsonl') -> None:
        self.file_path = file_path
    
    def __repr__(self) -> str:
        return f'StorageClient(file_path={self.file_path})'
    
    def add_client_jsonl(self, client: Client) -> None:
        """Appends the client data to a JSON file with a unique ID."""
        max_id = 0
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if not line.strip():
                        # No line to read, break the loop
                        break
                    data_clients = json.loads(line)
                    max_id = max(max_id, data_clients['id'])
        except (FileNotFoundError, json.JSONDecodeError):
            max_id = 0

        new_client = {
           "id": max_id + 1,
            **client.model_dump(),  # Unpack the client attributes
        }

        with open(self.file_path, 'a', encoding='utf-8') as file:
            client_json = json.dumps(new_client, ensure_ascii=False) + '\n'
            file.write(client_json)
            
        print(f'Cliente {client.name} adicionado com ID {max_id + 1}')
    