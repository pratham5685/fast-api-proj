from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from models import * # Import the PersonalInfo model
from fastapi.middleware.cors import CORSMiddleware


from tortoise import Tortoise, fields
from models import User
app = FastAPI()
from fastapi import FastAPI, Depends, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, fields
from models import User

# adding cors urls
origins = ['http://localhost:3000']

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


@app.get("/")
def index():
    return {"message": "Hello, FastAPI!"}


@app.post('/personal_info/')
async def create_personal_info(payload: PersonalInfo_request):
    new_info = await PersonalInfo.create(**payload.dict())
    response  = await PersonalInfo_pydantic.from_tortoise_orm(new_info)
    return {"status": "success", "response": response}

@app.get('/personal-info/{personal_info_id}')
async def read_personal_info(personal_info_id: int):
    info = await PersonalInfo.get_or_none(id=personal_info_id)
    if info is None:
        raise HTTPException(status_code=404, detail="Personal Info not found")
    return {"response": info}

@app.get('/get_all_personal_info')
async def get_all_personal_info():
    response = await PersonalInfo_pydantic.from_queryset(PersonalInfo.all())
    return {"status": "success", "response": response}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},  # Update to point to the models module
    generate_schemas=True,
    add_exception_handlers=True
)
# Login route
@app.post("/login")
async def login(username: str, password: str):
    user = await User.filter(username=username, password=password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

# Endpoint to get all users
@app.get("/users")
async def get_users():
    users = await User.all()
    return users

# Endpoint to create a new user
@app.post("/users")
async def create_user(username: str, password: str):
    user = await User.create(username=username, password=password)
    return {"message": "User added successfully"}


# test code for fees status 
@app.put('/update_fees_status/{personal_info_id}')
async def update_fees_status(personal_info_id: int):
    personal_info = await PersonalInfo.get_or_none(id=personal_info_id)
    if personal_info is None:
        raise HTTPException(status_code=404, detail="Personal Info not found")
    personal_info.fees_status = True
    await personal_info.save()
    updated_personal_info = await PersonalInfo_pydantic.from_tortoise_orm(personal_info)
    return {"status": "success", "updated_info": updated_personal_info}



#baallee ballee 
# class aur division ka logic idhar 

def determine_class_and_division(age: int, sex: str) -> tuple:
    if age >= 16:
        class_ = "Class 1"
    elif 14 <= age < 16:
        class_ = "Class 2"
    elif 11 <= age < 14:
        class_ = "Class 3"
    elif 9 <= age < 11:
        class_ = "Class 4"
    elif 7 <= age < 9:
        class_ = "Class 5"
    elif 6 <= age < 7:
        class_ = "Class 6"
    else:
        class_ = "Class 7"

    division = "A" if sex == "M" else "B" if sex == "F" else None

    return class_, division

@app.get("/paid_students")
async def get_paid_students():
    paid_students = await PersonalInfo.filter(fees_status=True).values(
        "id", "first_name", "last_name", "age", "sex", "mobile_number"
    )
    paid_students_data = []
    for student in paid_students:
        class_, division = determine_class_and_division(student.get("age", 0), student.get("sex", ""))
        if class_:
            student_data = {
                "id": student.get("id"),
                "first_name": student.get("first_name"),
                "last_name": student.get("last_name"),
                "class": class_,
                "division": division,
                "phone_number": student.get("mobile_number")
            }
            paid_students_data.append(student_data)
    
    return {"status": "success", "paid_students": paid_students_data}