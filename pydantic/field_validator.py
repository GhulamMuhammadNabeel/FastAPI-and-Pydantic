from pydantic import BaseModel,field_validator
from typing import List,Dict,Annotated

class Patient(BaseModel):
    name : str
    age : int
    weight: int
    email: str
    allergies: List[str]
    adress: Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['google.com']
        domain_name=value.split('@')[-1]

        if domain_name  not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.adress)
inserted_patient ={
    'name':'Nabeell',
    'age':30,
    'weight':50,
    'email':'nabeel@google.com',
    'allergies':['Nazla','Khaansi'],
    'adress':{
        'City':'Multan',
        'Province':'Punjab',
        'Country':'Pakistan',
    }
}
patient1=Patient(**inserted_patient)
insert_patient(patient1)