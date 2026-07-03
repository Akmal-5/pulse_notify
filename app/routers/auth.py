from app.core.dependencies import create_session
from app.schemas.auth import CreateUser
from app.service.auth_service import user_cheking_mail
from app.email.email_service import send_verification_email
from app.schemas.auth import ModelCheckCode
from app.service.auth_service import user_check_code_mail
from app.schemas.auth import UserAuthorization
from app.service.auth_service import user_verification
from app.core.security import jwt_encode_access , jwt_decode_refresh , jwt_decode , jwt_encode_refresh
from typing import Annotated
from fastapi import APIRouter , status , Depends , BackgroundTasks , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="auth/" , tags=["Авторизация"])


@router.post("/register/",
             summary="Регистрация ✔",
             status_code=status.HTTP_201_CREATED
             )

async def user_register (session : Annotated[AsyncSession ,  Depends(create_session)] ,
                         user : CreateUser,
                         background_task : BackgroundTasks
                         ) :
    code  = await user_cheking_mail(session , user)
    
    background_task.add_task(send_verification_email , user.email ,code)
    return {
        "message" : "Код отправлен на почту"
    }

@router.post("/chekcode_mail/")

async def check_code (session : Annotated[AsyncSession ,  Depends(create_session)] ,
                      check : ModelCheckCode
                      ) :
    return await user_check_code_mail (session , check)


@router.post("/login/" ,
             summary="Авторизация"
             )

async def user_login (session : Annotated[AsyncSession , Depends(create_session)] ,
                      user : UserAuthorization
                      ) :
    result = await user_verification(session , user)
    
    if result :
        encode_access = jwt_encode_access(result)
        encode_refresh = jwt_decode_refresh(result)
        return {
            "access_token" : encode_access,
            "refresh_token" : encode_refresh
        }
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="user not found"
                        )

@router.get("/refresh/",
            summary="Обновление access-токенв"
            )

async def update_access (token : Annotated[dict, Depends(jwt_decode_refresh)]) :
    new_access_token = jwt_encode_access({
        "user_id" : token.get("user_id"),
        "username" : token.get("username") 
    })
    
    return {"access_token" : new_access_token}