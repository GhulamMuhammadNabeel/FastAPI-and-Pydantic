from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json
app= FastAPI()

# Patient model
class Patient(BaseModel):

    id: Annotated[str,Field(...,description='ID of the  patient',examples=['P001,P002'])]
    name : Annotated[str,Field(...,description='Name of the patient')]
    city: Annotated[str,Field(...,description='City of the patient')]
    age: Annotated[int,Field(...,ge=0,le=120,description='Age of the patient')]
    gender: Annotated[Literal['male','female','other'],Field(...,description='Gender of the patient')]
    height: Annotated[float,Field(...,gt=0,le=5,description='Height of the patient')]
    weight: Annotated[float,Field(...,gt=0,description='Weight of the patient')]

    @computed_field()
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/self.height**2,2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

# Update Patient model
class Update_patient(BaseModel):

    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None,ge=0,le=120)]
    gender: Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height: Annotated[Optional[float],Field(default=None,gt=0)]
    weight: Annotated[Optional[float],Field(default=None,gt=0)]

# Load data from json
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

# Save data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

# Home
@app.get('/')
def hello():
    return {'message':'Patients Management System'}

# ABout
@app.get('/about')
def about():
    return {'message':'A Fully functional patient management API'}

# Read all patients
@app.get('/view')
def view():
    data = load_data()
    return data

# Read single patient data
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='Patient Id will be passed here',example='P001,P002.....')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')

# Query
@app.get('/sort')
def sort_by(sort_by:str=Query
            (..., #iska matlab ha k require ha ye
             description='Sort by height,bmi,weight'),order:str=Query
             ('asc', #ye bydefault ha value
              description='Sort by ascending or descending value'
              )):
    valid_fields=['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(400,detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc','des']:
        raise HTTPException(400,detail=f'Invalid order selected ')
    data = load_data()
    sort_order = True if order=='des' else False  # ye check krega k kia pass ho rha ha des ya asc ?
    sorted_data =sorted(
        data.values(), 
        key=lambda x: x. get(sort_by,0), 
        reverse=sort_order  # yahan pr reverse order ka scene ha sara agr oper se True aa rha ha to yani oper des pass hua ha aur reverse == True aa gya ha yahan 
    )
    return sorted_data

# Create new patient
@app.post('/create')
def create_patient(patient: Patient):
    # load existing Data
    data = load_data()
    # Check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    # if not then create new 
   
    data[patient.id] = patient.model_dump(exclude='id')
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'New patient has been added'})

# Update patient
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: Update_patient):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

    # What about the bmi and verdict ?? they will be the same as they were before updating the weight and height 
    # to tackle this issue we'll send the existing_patient_info to Patient model and then that model will return the bmi and verdict as  well
    # and then we'll save that model
    existing_patient_info['id'] = patient_id
    pydantic_patient = Patient(** existing_patient_info)
    existing_patient_info = pydantic_patient.model_dump(exclude='id')

    data[patient_id]= existing_patient_info
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'Patient info has been updated'})

# Delete patient
@app.delete('/delete/{patient_id}')
def delete_patient(patiend_id: str):
    data=load_data()
    if patiend_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    del data[patiend_id]
    save_data(data)

    return JSONResponse(status_code=201, content={'message':"Patient's record has been deleted"})
