from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: str

    age:int 
    weight:float 
    married: bool = False
    email = EmailStr
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]
    linkedin_url = AnyUrl

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    
    @field_validator('name', mode='after')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @model_validator(mode='after')
    def vlidate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model
    
    
    
patient_info = {'name': 'Deepanshu', 'age': '20', 'weight': 75.3, 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details': {'email': 'abc@gmail.com', 'phone': 234535}}


patient1 = Patient(**patient_info)

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('bmi', patient:calculate_bmi)


""" Computed Field """
@computed_field
@property
def calculate_bmi(self) -> float:
    bmi = round(self.weight/(self.height**2), 2)
    return bmi

""" Nested models"""
from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address: Address

address_dict= {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)
patient_dict= {'name': 'Ritz','gender': 'Non-Binary', 'age': 23, 'address': address1}

patient1 = Patient(**patient_dict)

print(patient1)
