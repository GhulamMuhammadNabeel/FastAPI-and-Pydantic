from pydantic import BaseModel
class Adress(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    adress: Adress

adress_dict={
    'city':'Multan',
    'state':'Punjab',
    'pin':'9021'
}
adress1=Adress(**adress_dict)

patient_data= {
    'name':'Nabeel',
    'gender':'Male',
    'age':66,
    'adress':adress1
}
patient1=Patient(**patient_data)
print(patient1.adress.city)