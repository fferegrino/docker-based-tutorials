from fastapi import FastAPI, HTTPException
import aiomysql
import os

app = FastAPI()

# Database connection configuration
db_config = {
    "host": os.getenv("MYSQL_HOST", "db"),
    "user": os.getenv("MYSQL_USER", "user"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "db": os.getenv("MYSQL_DATABASE", "fastapi_db"),
}

async def get_connection():
    conn = await aiomysql.connect(**db_config)
    return conn

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with MySQL"}

@app.get("/items")
async def get_items():
    try:
        conn = await get_connection()
        cur = await conn.cursor()
        
        # Execute a simple SELECT query
        await cur.execute("SELECT * FROM items")
        result = await cur.fetchall()
        
        # Convert result to list of dictionaries
        items = []
        for row in result:
            items.append({
                "id": row[0],
                "title": row[1],
                "description": row[2]
            })
        
        await cur.close()
        conn.close()
        
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 