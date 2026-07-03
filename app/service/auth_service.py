import random
from app.models.user import CreateUsers
from app.models.userteste import UserTeste
from datetime import datetime ,  timedelta
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException , status


async def user_cheking_mail (sessaion : AsyncSession , user_data) :
    
    res_username = await sessaion.execute(select(CreateUsers).where(CreateUsers.username == user_data.username))
    
    if res_username.scalar() :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail="Такой ник уже занят"
                            )
    res_email = await sessaion.execute(select(CreateUsers).where(CreateUsers.email == user_data.email))
    
    if res_email.scalar() :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail= "Такая почта уже занята"
                            )
        
    password_bytes = user_data.password.encode("utf-8")
    password_hash = bcrypt.hashpw(password_bytes , bcrypt.gensalt()) 
    
    code = str(random.randint(100000, 999999))
    
    res = await sessaion.execute(select(UserTeste).where(
        UserTeste.email == user_data.email
    ))
    
    draft = res.scalar()
    
    if draft :
        draft.code = code
        draft.attempts = 0
        draft.expires_at = datetime.utcnow() + timedelta(minutes=5)
        
        draft.username = user_data.username
        draft.password = password_hash.decode("utf-8")
        
    else :
        sessaion.add(UserTeste(
            username = user_data.username,
            password = password_hash.decode("utf-8") ,
            email = user_data.email,
            code = code
            
        ))
        
    await sessaion.commit()
    return code


async def user_check_code_mail (session : AsyncSession , code_mail) :
    
    res = await session.execute(select(UserTeste).where(UserTeste.email == code_mail.email))
    
    draft = res.scalar()
    
    if not draft :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Сначала запросите код"
                            )
        
    if datetime.utcnow() > draft.expires_at:
        await session.delete(draft)
        await session.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Код истёк, запросите новый"
                            )
        
    if draft.attempts >= 3 :
        await session.delete(draft)
        await session.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail="Слишком много попыток, запросите новый код!"
                            )
        
    if draft.code != code_mail.code :
        draft.code += 1
        await session.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail="Неверный код!"
                            )
    new_user = (CreateUsers(
        username = draft.username,
        email = draft.email,
        password = draft.password
    ))
    
    session.add(new_user)
    await session.delete(draft)
    await session.commit()
    return {
        "message" : "Регистрация успешна!"
    }
    
async def user_verification (session : AsyncSession , user_data) :
    
    username = await session.execute(select(CreateUsers).where(CreateUsers.username == user_data.username))
    
    res_user = username.scalar_one_or_none()
    
    if not res_user : 
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail="There is no such user with such a nickname"
                            )
        
    password_result  = bcrypt.checkpw(user_data.password.encode("utf-8"),
                                      res_user.password.encode("utf-8")
                                      )
    
    if password_result :
        return {
            "user_id" : res_user.id,
            "username" : res_user.username
        }  
        
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect password"
                        )