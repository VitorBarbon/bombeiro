from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from clients.models.client import ClientDB, CityHallServiceDB, FireDepartmentServiceDB, engine
from colorama import Fore, Style
from typing import Optional


# create session factory
# engine = create_engine(f'sqlite:///{paths.DATA_DIR / "clients.db"}')
Session = sessionmaker(bind=engine)


class StorageClient:
    def __init__(self) -> None:
        self.session = Session()

    def __repr__(self) -> str:
        return 'StorageClient(SQLAlchemy ORM)'

    def add_client(self, client: ClientDB) -> None:
        try:
            self.session.add(client)
            self.session.commit()
            print(Fore.GREEN + 'Cliente adicionado com sucesso.' + Style.RESET_ALL)
        except SQLAlchemyError as e:
            self.session.rollback()
            print(Fore.RED + f'Erro ao adicionar cliente ao banco de dados: {e}' + Style.RESET_ALL)
        finally:
            self.session.close()
