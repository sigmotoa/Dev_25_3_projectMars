import os
from typing import Optional
from fastapi import UploadFile
from supabase import create_client, Client

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL:str = os.getenv("SUPABASE_URL_MIERS")
SUPABASE_KEY:str = os.getenv("SUPABASE_KEY_MIERS")
SUPABASE_BUCKET:str = os.getenv("SUPABASE_BUCKET_MIERS")

_supabase_client:Optional[Client] = None

def get_supabase_client():
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase URL and API key are required.")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

    return _supabase_client

async def upload_file_bucket(file: UploadFile):
    client = get_supabase_client()
    try:
        file_content = await file.read()
        file_path = f"public/{file.filename}"
        result = client.storage.from_(SUPABASE_BUCKET).upload(
            path=file_path,
            file=file_content,
            file_options={
                "content_type": file.content_type
            }

        )
        public_url = client.storage.from_(SUPABASE_BUCKET).get_public_url(file_path)

        return public_url
    except Exception as e:
        raise e

