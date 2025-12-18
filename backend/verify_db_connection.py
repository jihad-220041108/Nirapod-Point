import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Load the exact same .env file provided to the backend
load_dotenv()

async def verify():
    db_url = os.getenv("DATABASE_URL")
    print(f"🔌 Checking Connection...")
    print(f"Target Host: {db_url.split('@')[1].split(':')[0]}") # Print host part only for security
    
    try:
        engine = create_async_engine(db_url)
        async with engine.connect() as conn:
            # 1. Check Table Existence
            print("🔍 Checking crime_reports table...")
            result = await conn.execute(text("SELECT count(*) FROM crime_reports"))
            count = result.scalar()
            
            print(f"✅ Connection Successful!")
            print(f"📊 Total Crime Reports Found: {count}")
            
            if count > 40000:
                print("🚀 CONFIRMED: Connected to Supabase (High data volume detected)")
            elif count == 0:
                print("⚠️ WARNING: Table is empty. Might be local DB or import failed.")
            else:
                print("ℹ️  Connected, but data volume is low. Verify if this matches your expectation.")
                
            # 2. Check a specific recent record to be sure
            result = await conn.execute(text("SELECT title FROM crime_reports LIMIT 1"))
            row = result.scalar()
            print(f"📝 Sample Record: {row}")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
