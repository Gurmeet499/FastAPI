from fastapi import FastAPI
import json
# helper function to load data from patient
def load_data():
    with open('patients.json','r') as f:
      data = json.load(f)

    return data


@app.get("/") # home route
def hello():
    return {'message': 'Patient management System API'}



@app.get("/about")
def info():
    return {'Information':'''
 A fully Functional API to manage your patient records
'''
    }    

@app.get("/view")
def view():
    data = load_data()
    return data


# path parameter
@app.get("/patient/{patient_id}")
def view_patient(patient_id:str= Path(...,description="Id of the patient in the Db",example="P001")):
    data = load_data()
    if patient_id in data: # checks patient id exits in data
        return data[patient_id]
    raise HTTPException(status_code=400,detail='patient not found')



@app.get('/sort')
def sort_patient(sort_by :str= Query(description='sort on the basis of height , weight , bmi and age'
),order: str =Query('asc',description='sort in acs or desc order')):

    valid_fields =["height","weight","bmi","age"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, 
            detail=f'invalid field select from{valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,
        detail='Invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(),key=lambda x : x.get(sort_by,0),reverse = sort_order)
    return sorted_data


    
