import json
# from project.utils import paths
from typing import Dict, Optional
from pydantic import BaseModel

class CityHallService(BaseModel):
    owner_name: Optional[str]
    owner_cpf: Optional[str]
    property_type: Optional[str]
    

class FireDepartmentService(BaseModel):
    area: Optional[float]
    fire_load: Optional[float]
    
    
class Client(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: str
    occupation: str
    city_hall_service: Optional[CityHallService] = None
    fire_department_service: Optional[FireDepartmentService] = None

    def to_dict(self) -> Dict:
        return json.loads(self.json())

    @classmethod
    def from_dict(cls, data: Dict) -> "Client":
        return cls(**data)

    # drepecated in pydantic, search for the new way to do it
    # @classmethod
    # def from_json(cls, json_str: str) -> "Client":
    #     return cls.parse_raw(json_str) 