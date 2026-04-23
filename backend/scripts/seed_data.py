import asyncio
import os
from IRYM_sdk import init_irym, startup_irym, get_rag_pipeline

async def seed_data():
    print("[*] Initializing IRYM SDK for seeding...")
    init_irym()
    await startup_irym()
    
    rag = get_rag_pipeline()
    
    data_dir = "./data"
    if not os.path.exists(data_dir):
        print(f"[!] Data directory {data_dir} not found.")
        return
        
    print(f"[*] Ingesting data from {data_dir}...")
    await rag.ingest(data_dir)
    print("[+] Seeding complete. Your real estate data is now in ChromaDB.")

if __name__ == "__main__":
    asyncio.run(seed_data())
