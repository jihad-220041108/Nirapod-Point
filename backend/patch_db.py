import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

async def patch():
    db_url = os.getenv("DATABASE_URL")
    engine = create_async_engine(db_url)
    
    async with engine.begin() as conn:
        print("🔧 Patching DB: Adding 'relationship' column to emergency_contacts...")
        try:
            await conn.execute(text("ALTER TABLE emergency_contacts ADD COLUMN IF NOT EXISTS relationship VARCHAR"))
            print("✅ Column added successfully")
        except Exception as e:
            print(f"⚠️ Error (might already exist): {e}")

if __name__ == "__main__":
    asyncio.run(patch())
