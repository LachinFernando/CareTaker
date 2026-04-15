import supabase
import os
import streamlit as st
from supabase import create_client

os.environ["SUPABASE_URL"] = st.secrets["database"]["SUPABASE_URL"]
os.environ["SUPABASE_KEY"] = st.secrets["database"]["SUPABASE_KEY"]

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def insert_data(table_name: str, row: dict):
    try:
        response = supabase.table(table_name).insert(row).execute()
        return True
    except Exception as e:
        st.error(f"Error inserting data: {str(e)}")
        return False


def fetch_parent_user(email: str):
    """
    Fetch user data from the users table based on email ID
    
    Args:
        email (str): Email address to search for
        
    Returns:
        dict: User data if found, None if not found
    """
    try:
        response = supabase.table("users").select("*").eq("parent_email", email).execute()
        if response.data:
            return response.data[0]  # Return the first user found
        return None
    except Exception as e:
        st.error(f"Error fetching user: {str(e)}")
        return None


def fetch_member_user(member_email: str):
    """
    Fetch member information from the members table based on member_email
    
    Args:
        member_email (str): Email address of the family member to search for
        
    Returns:
        dict: Member data if found, None if not found
    """
    try:
        response = supabase.table("members").select("*").eq("family_member_email", member_email).execute()
        if response.data:
            return response.data[0]  # Return the first member found
        return None
    except Exception as e:
        st.error(f"Error fetching member: {str(e)}")
        return None


def fetch_parent_id_from_member_parent(email: str):
    """
    Fetch parent_id from member_parent table using either parent_email or member_email
    
    Args:
        email (str): Email address (can be either parent_email or member_email)
        
    Returns:
        str: parent_id if found, None if not found
    """
    try:
        # First try to find by parent_email
        response = supabase.table("member_parent").select("*").eq("parent_email", email).execute()
        if response.data:
            return response.data[0]["parent_id"]
        
        # If not found, try to find by member_email
        response = supabase.table("member_parent").select("*").eq("member_email", email).execute()
        if response.data:
            return response.data[0]["parent_id"]
        
        return None
    except Exception as e:
        st.error(f"Error fetching parent_id: {str(e)}")
        return None