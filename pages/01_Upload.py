import streamlit as st
import os

from db_utils import fetch_parent_id_from_member_parent
from storage_utils import upload_file, directory_exists, list_files_in_directory

REMOTE_PREFIX = "upload"


if not st.user.is_logged_in:
    # ask to login
    # message to please login with an icon
    st.markdown("⚠️ Please login to register a new user")
    st.stop()

# get the parent member table
try:
    parent_folder_id = fetch_parent_id_from_member_parent(st.user.email)
except Exception as e:
    st.error("Error fetching parent member table! No parent folder or parent registered!")
    st.stop()

# check if path is exists
try:
    if not os.path.exists(parent_folder_id):
        os.makedirs(parent_folder_id)
except Exception as e:
    st.error("Error creating parent folder! No parent folder or parent registered!")
    st.stop()

# title for uploading
st.title("🏥 CareTaker Upload")
st.markdown("*Upload your medical documents*")

# show existing files
with st.sidebar:
    if directory_exists(f"{REMOTE_PREFIX}/{parent_folder_id}"):
        st.markdown("### 📁 Existing Files")
        # fetch files from remote storage
        files = list_files_in_directory(f"{REMOTE_PREFIX}/{parent_folder_id}")
        for file_ in files:
            st.markdown(f"- {file_}")

# file upload
files = st.file_uploader("Upload your medical documents", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

# submit button
if st.button("Upload"):
    if not files:
        st.error("Please select at least one file to upload!")
        st.stop()
    # save these files inside the parent folder
    for file_ in files:
        with open(os.path.join(parent_folder_id, file_.name), "wb") as f:
            f.write(file_.getbuffer())

    for file_item in os.listdir(parent_folder_id):
        remote_path = f"{REMOTE_PREFIX}/{parent_folder_id}/{file_item}"
        upload_file(os.path.join(parent_folder_id, file_item), remote_path)

    st.toast("Files uploaded successfully!")
    st.rerun()

    