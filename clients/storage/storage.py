from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from clients.models.client import ClientDB, engine, create_tables
from colorama import Fore, Style
from typing import Optional, Any


# create session factory
# engine = create_engine(f'sqlite:///{paths.DATA_DIR / "clients.db"}')
Session = sessionmaker(bind=engine)


class StorageClient:
    def __init__(self) -> None:
        self.session = Session()
        self.create_tables()

    def __repr__(self) -> str:
        return 'StorageClient(SQLAlchemy ORM)'

    def add_client(self, client: ClientDB) -> None:
        try:
            self.session.add(client)
            self.session.commit()
            print(Fore.GREEN + 'Cliente adicionado com sucesso.' + Style.RESET_ALL)
        except SQLAlchemyError as e:
            self.session.rollback()
            print(Fore.RED + f'Erro ao adicionar cliente ao banco de dados: {e}'\
                + Style.RESET_ALL)
        finally:
            self.session.close()
    
    def get_client_by_filter(self, filter: str) -> Optional[ClientDB]:
        try:
            clients = self.session.query(ClientDB)\
                .filter(ClientDB.name.ilike(f'%{filter}%')).all()
            list_clients = [client.to_dict() for client in clients]
            return list_clients if list_clients else None
        except SQLAlchemyError as e:
            print(Fore.RED + f'Erro ao buscar cliente no banco de dados: {e}'\
                + Style.RESET_ALL)
            return None
        finally:
            self.session.close()
    
    def get_client_by_id(self, client_id: int) -> Optional[ClientDB]:
        try:
            client = self.session.query(ClientDB)\
                .filter(ClientDB.id == client_id).first()
            return client.to_dict() if client else None
        except SQLAlchemyError as e:
            print(Fore.RED + f'Erro ao buscar cliente no banco de dados: {e}'\
                + Style.RESET_ALL)
            return None
        finally:
            self.session.close()

    def get_all_clients(self) -> list[dict[str, Any]]:
        try:
            clients = self.session.query(ClientDB).all()
            if not clients:
                print(Fore.YELLOW + 'Nenhum cliente encontrado.'\
                    + Style.RESET_ALL)
                return []
            list_clients = [client.to_dict() for client in clients]
            return list_clients
        except SQLAlchemyError as e:
            print(Fore.RED + f'Erro ao buscar todos os clientes no banco de dados: {e}'\
                + Style.RESET_ALL)
            return []
        finally:
            self.session.close()
            
    def update_client(self, client: ClientDB) -> None:
        try:
            existing_client = self.session.query(ClientDB)\
                .filter(ClientDB.id == client.id).first()
            if existing_client:
                existing_client.name = client.name
                existing_client.email = client.email
                existing_client.phone = client.phone
                self.session.commit()
                print(Fore.GREEN + 'Cliente atualizado com sucesso.' + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + 'Cliente não encontrado.' + Style.RESET_ALL)
        except SQLAlchemyError as e:
            self.session.rollback()
            print(Fore.RED + f'Erro ao atualizar cliente no banco de dados: {e}'\
                + Style.RESET_ALL)
        finally:
            self.session.close()
            
    def delete_client(self, client_id: int) -> None:
        try:
            client = self.session.query(ClientDB).filter(ClientDB.id == client_id).first()
            city_hall_service = client.city_hall_service if client else None
            fire_department_service = client.fire_department_service if client else None
            
            if client:
                self.session.delete(client)
                self.session.delete(city_hall_service)
                self.session.delete(fire_department_service)
                self.session.commit()
                print(Fore.GREEN + 'Cliente deletado com sucesso.' + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + 'Cliente não encontrado.' + Style.RESET_ALL)
        except SQLAlchemyError as e:
            self.session.rollback()
            print(Fore.RED + f'Erro ao deletar cliente no banco de dados: {e}'\
                + Style.RESET_ALL)
        finally:
            self.session.close()
