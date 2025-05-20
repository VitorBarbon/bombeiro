from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from project.utils import paths


Base = declarative_base()

class CityHallServiceDB(Base):
    __tablename__ = 'city_hall_service'
    id = Column(Integer, primary_key=True)
    owner_name = Column(String)
    owner_cpf = Column(String)
    description = Column(String)
    number_project = Column(String)
    number_process = Column(String)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'owner_name': self.owner_name,
            'owner_cpf': self.owner_cpf,
            'description': self.description,
            'number_project': self.number_project,
            'number_process': self.number_process
        }
   
    
class FireDepartmentServiceDB(Base):
    __tablename__ = 'fire_department_service'
    id = Column(Integer, primary_key=True)
    fire_load = Column(Float)
    number_project = Column(String)
    number_process = Column(String)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'fire_load': self.fire_load,
            'number_project': self.number_project,
            'number_process': self.number_process
        }


class ClientDB(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    address = Column(String, nullable=False)
    area = Column(Float, nullable=False)
    occupation = Column(String, nullable=False)
    
    city_hall_service_id = Column(Integer, ForeignKey('city_hall_service.id'))
    fire_department_service_id = Column(Integer, ForeignKey('fire_department_service.id'))

    city_hall_service = relationship("CityHallServiceDB")
    fire_department_service = relationship("FireDepartmentServiceDB")
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'area': self.area,
            'occupation': self.occupation,
            'city_hall_service': self.city_hall_service.to_dict() if self.city_hall_service else None,
            'fire_department_service': self.fire_department_service.to_dict() if self.fire_department_service else None
        }


engine = create_engine(f'sqlite:///{paths.DATA_DIR / "clients.db"}')

def create_tables() -> None:
    Base.metadata.create_all(engine)