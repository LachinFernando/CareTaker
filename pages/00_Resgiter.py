import streamlit as st
import pandas as pd
import os
import time

from db_utils import insert_data, fetch_parent_user, fetch_member_user


# session state
if "is_parent_registered" not in st.session_state:
    st.session_state.is_parent_registered = False

if "is_member_registered" not in st.session_state:
    st.session_state.is_member_registered = False

# app logic
if not st.user.is_logged_in:
    # message to please login with an icon
    st.markdown("⚠️ Please login to register a new user")
    st.stop()

parent_user = fetch_parent_user(st.user.email)
# check if the user is already registered
if parent_user:
    st.session_state.is_parent_registered = True
    # diplay the info in a table
    with st.sidebar:
        st.subheader("User Details")
        st.markdown("**User Name:** " + parent_user["parent_name"])
        st.markdown("**Primary Doctor:** " + parent_user["primary_doctor"])
        st.markdown("**Contact Email:** " + parent_user["parent_email"])
        if parent_user.get("other_doctors", None):
            st.markdown("**Other Doctors:** " + parent_user["other_doctors"])
        st.markdown("**Emergency Contact:** " + parent_user["emergency_contact"])

# check if the user is a member
if fetch_member_user(st.user.email):
    st.session_state.is_member_registered = True

# title for registering
st.title("🏥 CareTaker Register")
st.markdown("*Register as a Primary Account Holder*")

# two tabs foe parent and familary registration
parent_tab, family_tab = st.tabs(["Become Parent/Guardian", "Add Family Member"])

with family_tab:
    st.markdown("## 📝 Add Family Member")
    # only a parent/guardian can add family members
    if not st.session_state.is_parent_registered:
        st.markdown("⚠️ You are not registered as a parent/guardian")
    else:
        # form to add family members    
        with st.form("family_form"):
            st.markdown("### 📝 Family Member Information")
            # field to add the member name, email addresses, illness, and any other relevant information
            member_name = st.text_input("Family Member Name *", placeholder="Enter the family member's name")
            member_email = st.text_input("Family Member Email *", placeholder="Enter the family member's email")
            member_illness = st.text_input("Family Member Illness", placeholder="Enter the family member's illness")
            member_other_info = st.text_area("Family Member Other Information", placeholder="Enter any other relevant information")
            
            # Submit button
            st.markdown("---")
            fam_submitted = st.form_submit_button("🚀 Complete Registration", type="primary", use_container_width=True)
            if fam_submitted:
                # member name and emai are compulsory
                # add the validation
                if member_name and member_email:
                    # create the member data
                    member_data = {"family_member_email": member_email, "family_member_name": member_name, "family_member_illness": member_illness, "family_member_other_info": member_other_info}
                    # add to the database
                    member_response = insert_data("members", member_data)
                    # member parent mapping
                    member_parent_data = {"parent_id": str(st.user.sub), "parent_email": st.user.email, "member_email": member_email}
                    # add to the database
                    member_parent_response = insert_data("member_parent", member_parent_data)
                    if member_response and member_parent_response:
                        st.success("✅ Family member added successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to add family member")

with parent_tab:
    if st.session_state.is_parent_registered:
        st.markdown("⚠️ You are already registered as a parent/guardian")

    # member cannot sign as parent
    elif st.session_state.is_member_registered:
        st.markdown("⚠️ You are already registered as a family member")

    # form to register as a parent user
    else:
        with st.form("registration_form"):
            st.markdown("### � Parent/Guardian Information")
            
            # Parent name field
            parent_name = st.text_input(
                "Parent/Guardian Name *",
                placeholder="Enter your full name",
                help="This will be the primary account holder name"
            )
        
            # Primary care doctor field
            primary_doctor = st.text_input(
                "Primary Care Doctor Name *",
                placeholder="Dr. Smith",
                help="Enter your primary care physician's name"
            )
            
            # Other doctors field
            other_doctors = st.text_area(
                "Other Doctors/Specialists",
                placeholder="Dr. Johnson (Cardiologist)\nDr. Williams (Endocrinologist)\nDr. Brown (Dermatologist)",
                help="List any other doctors or specialists you see regularly, one per line"
            )
            
            # Additional information
            st.markdown("### 📝 Additional Information")
            
            contact_email = st.text_input(
                "Contact Email (Must be your gmail you are logged in with) *",
                placeholder="your.email@example.com",
                help="Email for important medical notifications"
            )
            
            emergency_contact = st.text_input(
                "Emergency Contact Name & Phone *",
                placeholder="John Doe - (555) 123-4567",
                help="Who should we contact in case of emergency?"
            )
            
            # Submit button
            st.markdown("---")
            submitted = st.form_submit_button("🚀 Complete Registration", type="primary", use_container_width=True)
            
            if submitted:
                if parent_name and primary_doctor and contact_email and emergency_contact:
                    # save to database
                    user_response = insert_data("users", {
                        "parent_email": contact_email,
                        "parent_name": parent_name,
                        "primary_doctor": primary_doctor,
                        "other_doctors": other_doctors.replace("\n", ", ") if other_doctors else "",
                        "emergency_contact": emergency_contact
                    })
                    # save the records
                    if user_response:
                        st.success("✅ Registration submitted successfully!")
                        st.balloons()
                        # wait around for 5 seconds
                        time.sleep(5)
                        st.rerun()
                    
                    # Display submitted information
                    st.markdown("### 📄 Registration Summary")
                    st.markdown(f"**Parent/Guardian:** {parent_name}")
                    st.markdown(f"**Primary Care Doctor:** {primary_doctor}")
                    if other_doctors:
                        st.markdown(f"**Other Doctors:**\n{other_doctors}")
                    st.markdown(f"**Contact Email:** {contact_email}")
                    if emergency_contact:
                        st.markdown(f"**Emergency Contact:** {emergency_contact}")
                    
                    st.info("🔔 You can now start uploading medical documents and manage access for family members and caretakers.")
                else:
                    st.error("❌ Please fill in all required fields marked with *")
