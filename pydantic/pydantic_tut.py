from pydantic import BaseModel,Field
from typing import List,Dict,Optional,Annotated
class Patient(BaseModel):
    name: str
    age: Annotated[int,Field(...,ge=0,le=120,title='Age of patient',description='The age of patient should be less than equals to 120 or greater than equals to 0')]
    weight: Optional[int]=Field(50,ge=0,strict=True)
    married:bool
    allergies: Optional[List[str]] = None
    contact: Dict[str,str]

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact)

patient_info={'name':'Nabeel',
              'weight':434,
              'age':90,
              'married':True,
            #   'allergies':['Nazla','khaansi'],
              'contact': {'email':'nabeel@gmail.com','phone':'303308278'}
              }
patient1=Patient(**patient_info)
insert_patient(patient1)