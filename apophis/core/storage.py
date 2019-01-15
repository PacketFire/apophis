import asyncio
import asyncpg

async def connect():
    db = await asyncpg.connect('postgresql://postgres:postgres@localhost:15432/apophis')
    return db

