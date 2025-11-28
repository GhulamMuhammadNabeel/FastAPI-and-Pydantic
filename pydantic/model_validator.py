from pydantic import BaseModel,model_validator
from typing import List,Dict

class Patient(BaseModel):
    name : str
    age : int
    weight: int
    email: str
    allergies: List[str]
    contact_details: Dict[str,str]

    @model_validator(mode='after')
    def emergency_contact_for_olds(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Patient is older than 60 and must need an emergency contact number')
        return model


def insert_patient(patient: Patient):
    print(patient.name)
    print(f"The age of patient is {patient.age}")
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact_details)
inserted_patient ={
    'name':'Nabeell',
    'age':61,
    'weight':50,
    'email':'nabeel@google.com',
    'allergies':['Nazla','Khaansi'],
    'contact_details':{
        'City':'Multan',
        'Province':'Punjab',
        'Country':'Pakistan',
        'emergency':'0322837727'
    }
}
patient1=Patient(**inserted_patient)
insert_patient(patient1)