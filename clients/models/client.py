from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class CityHallServiceDB(Base):
    __tablename__ = 'city_hall_service'
    id = Column(Integer, primary_key=True)
    owner_name = Column(String)
    owner_cpf = Column(String)
    property_type = Column(String)

class FireDepartmentServiceDB(Base):
    __tablename__ = 'fire_department_service'
    id = Column(Integer, primary_key=True)
    area = Column(Float)
    fire_load = Column(Float)

class ClientDB(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    address = Column(String, nullable=False)
    occupation = Column(String, nullable=False)
    
    city_hall_service_id = Column(Integer, ForeignKey('city_hall_service.id'))
    fire_department_service_id = Column(Integer, ForeignKey('fire_department_service.id'))

    city_hall_service = relationship("CityHallServiceDB")
    fire_department_service = relationship("FireDepartmentServiceDB")
