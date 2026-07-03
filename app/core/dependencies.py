from app.core.config import AsyncSessionMaker

async def create_session() :
    async with AsyncSessionMaker() as session :
        yield session