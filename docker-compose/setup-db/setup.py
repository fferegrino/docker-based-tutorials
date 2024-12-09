import aiomysql
import asyncio
import os

# Database connection configuration
db_config = {
    "host": os.environ["MYSQL_HOST"],
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "db": os.environ["MYSQL_DATABASE"],
}

async def get_connection():
    conn = await aiomysql.connect(**db_config)
    return conn


async def create_table():
    conn = await get_connection()
    cur = await conn.cursor()
    await cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT
        );
        """.strip())
    await conn.commit()
    await cur.close()
    conn.close()

async def add_items():
    items = [
        {"title": "Item 1", "description": "Description 1"},
        {"title": "Item 2", "description": "Description 2"},
        {"title": "Item 3", "description": "Description 3"},
    ]

    for item in items:
        conn = await get_connection()
        cur = await conn.cursor()

        # Check if the item already exists
        await cur.execute("SELECT * FROM items WHERE title = %s", (item["title"],))
        existing_item = await cur.fetchone()
        if existing_item:
            print(f"Item {item['title']} already exists")
            continue

        # Add the item
        await cur.execute("INSERT INTO items (title, description) VALUES (%s, %s)", (item["title"], item["description"]))
        await conn.commit()
        await cur.close()
        conn.close()

async def main():
    await create_table()
    await add_items()

if __name__ == "__main__":
    asyncio.run(main())