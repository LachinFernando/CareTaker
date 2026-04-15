import os
import streamlit as st
from pathlib import Path
import mimetypes
import requests
from supabase import create_client, Client


os.environ["SUPABASE_URL"] = st.secrets["database"]["SUPABASE_URL"]
os.environ["SUPABASE_KEY"] = st.secrets["database"]["SUPABASE_KEY"]
BUCKET_NAME = "caretaker"

# setup client 
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


def guess_content_type(file_path: str) -> str:
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"


def upload_file(local_file_path: str, remote_path: str):
    """
    Upload a local file to Supabase Storage.
    """
    content_type = guess_content_type(local_file_path)

    with open(local_file_path, "rb") as f:
        result = supabase.storage.from_(BUCKET_NAME).upload(
            path=remote_path,
            file=f,
            file_options={
                "content-type": content_type,
                "upsert": "true",   # overwrite if exists
                "cache-control": "3600",
            },
        )

    return result

def list_files_in_directory(directory_path: str):
    """
    List all files in a directory within the Supabase storage bucket
    
    Args:
        directory_path (str): Path to the directory in the bucket (e.g., "upload/parent_id")
        
    Returns:
        list: List of file names in the directory, empty list if directory doesn't exist or no files
    """
    try:
        # List all files in the specified directory
        result = supabase.storage.from_(BUCKET_NAME).list(directory_path)
        if result:
            # Extract just the file names from the response
            file_names = [file_dict['name'] for file_dict in result]
            return file_names
        else:
            return []
            
    except Exception as e:
        st.error(f"Error listing files in directory '{directory_path}': {str(e)}")
        return []


def directory_exists(directory_path: str):
    """
    Check if a directory exists in the Supabase storage bucket
    
    Args:
        directory_path (str): Path to the directory in the bucket (e.g., "upload/parent_id")
        
    Returns:
        bool: True if directory exists, False otherwise
    """
    try:
        # Try to list files in the directory
        result = supabase.storage.from_(BUCKET_NAME).list(directory_path)
        
        # If we get a result (even if empty), the directory exists
        # If we get an error, the directory likely doesn't exist
        return True
        
    except Exception as e:
        # Most common error is "The resource was not found" which means directory doesn't exist
        return False


def get_public_url(remote_path: str) -> str:
    """
    Returns the public URL for a file in a public bucket.
    """
    result = supabase.storage.from_(BUCKET_NAME).get_public_url(remote_path)

    # Depending on version, this may return a dict-like object or plain data.
    if isinstance(result, dict):
        if "publicUrl" in result:
            return result["publicUrl"]
        if "data" in result and isinstance(result["data"], dict) and "publicUrl" in result["data"]:
            return result["data"]["publicUrl"]

    # Fallback for object-like responses
    if hasattr(result, "get") and result.get("publicUrl"):
        return result.get("publicUrl")

    # Last-resort fallback using the standard public URL shape from the docs
    return f"{os.environ['SUPABASE_URL']}/storage/v1/object/public/{BUCKET_NAME}/{remote_path}"


def download_from_public_url(url: str, output_path: str):
    """
    Downloads a file using its public URL.
    """
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)