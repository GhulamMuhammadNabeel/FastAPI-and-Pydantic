from pydantic import BaseModel,computed_field
from typing import List,Dict

class Patient(BaseModel):
    name : str
    age : int
    weight: int #kg
    height: float #meters
    email: str
    allergies: List[str]
    contact_details: Dict[str,str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/self.height**2,2)
        return bmi

def insert_patient(patient: Patient):
    print(patient.name)
    print(f"The age of patient is {patient.age}")
    print(f'weight is {patient.weight}')
    print(f'height is {patient.height}')
    print(f'BMI is {patient.calculate_bmi}')
    print(patient.allergies)
    print(patient.contact_details)
inserted_patient ={
    'name':'Nabeell',
    'age':61,
    'height':5.4,
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