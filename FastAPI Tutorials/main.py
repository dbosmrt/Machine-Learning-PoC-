from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
import json
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description = 'ID of the patient', example=['P001'])]
    name:Annotated[str, Field(..., description= "name of the patient")]
    city:Annotated[str, Field(..., description= "city where the patient is living")]
    age:Annotated[int, Field(..., gt=0, lt=120, description= "Age of the patient")]
    gender:Annotated[Literal['Male', 'Female', 'Others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, desciption='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description= 'Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi <24:
            return 'Healthy'
        elif self.bmi <30:
            return 'Obese'
        else:
            return 'Normal'


@app.post('/create')
def create_patient(patient: Patient):
    #load existing data
    data = load_data()
    #check if the patient aleady exist
    if patient.id in data:
        raise HTTPException(status_code = 400, detail= 'Patient already exists')
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into 
    save_data(data)
    return JSONResponse(status_code=201, content={'Message': 'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: Patient):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info= data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key]=value
        patient_pydantic_obj= Patient(**existing_patient_info)

        # -> pydantic object -> dict
    data[patient_id]= existing_patient_info

    save_data(data)


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data[data]
    

def save_data():
    with open('patients.json', 'w') as f:
        data = json.dump(f)

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data




@app.get("/")
def hello():
    return{'message': 'Hello World'}


@app.get('/about')
def about():
    return{'messages': 'A fully functional API to manage your patient records.'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description = 'ID of the patient in the DB', example = 'P001')):
    #load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail = 'Patient not found')


@app.get('/sort')
def sort_patient(sort_by: str = Query(..., description='Sort on the basis of hieght, wright or bmi'), order: str = Query(
    'asc', description = 'stort in asc or desc order'
)):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail= f"Invalid field select from {valid_fields}")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc ')
    
    data = load_data()
    sorted_data =sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=False)
    return sorted_data

