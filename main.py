from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import models
from database import SessionLocal, engine

app = FastAPI(title="RPG Backend API")

class Query(BaseModel):
    table: str
    action: str
    payload: dict = {}
    filters: dict = {}

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/read")
async def read(query: Query, db: AsyncSession = Depends(get_db)):
    try:
        model = getattr(models, query.table.capitalize())
    except AttributeError:
        raise HTTPException(400, f"Unknown table {query.table}")
    stmt = model.__table__.select()
    for k, v in query.filters.items():
        stmt = stmt.where(getattr(model, k) == v)
    result = await db.execute(stmt)
    return [dict(r._mapping) for r in result.fetchall()]

@app.post("/write")
async def write(query: Query, db: AsyncSession = Depends(get_db)):
    try:
        model = getattr(models, query.table.capitalize())
    except AttributeError:
        raise HTTPException(400, f"Unknown table {query.table}")
    if query.action == "insert":
        obj = model(**query.payload)
        db.add(obj)
        await db.commit()
        return {"status": "inserted"}
    elif query.action == "update":
        stmt = model.__table__.update().where(
            *[getattr(model, k) == v for k, v in query.filters.items()]
        ).values(**query.payload)
        await db.execute(stmt)
        await db.commit()
        return {"status": "updated"}
    elif query.action == "delete":
        stmt = model.__table__.delete().where(
            *[getattr(model, k) == v for k, v in query.filters.items()]
        )
        await db.execute(stmt)
        await db.commit()
        return {"status": "deleted"}
    else:
        raise HTTPException(400, f"Invalid action {query.action}")
