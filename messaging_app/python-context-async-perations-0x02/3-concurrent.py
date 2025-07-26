import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('test.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect('test.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    all_users, older_users = results
    print("All users:", all_users)
    print("Users older than 40:", older_users)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
