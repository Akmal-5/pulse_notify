from pydantic import BaseModel , Field , EmailStr

class CreateUser (BaseModel) :
    
    username : str = Field(description="Имя пользователя" ,
                           min_length=3
                           )
    
    email : EmailStr
    password : str = Field(description="Пароль пользователя")