import streamlit as st

# App title and tagline
st.title("🏥 CareTaker")
st.markdown("*Your Intelligent Medical Document Assistant*")

# Login/Logout section
if not st.user.is_logged_in:
    st.markdown("---")
    st.subheader("🔐 Get Started")
    st.markdown("Create an account or log in to manage your medical documents and get AI-powered insights.")
    if st.button("Log in / Sign up", type="primary", use_container_width=True):
        st.login()
else:
    if st.button("Log out", use_container_width=True):
        st.logout()
        st.stop()
    
    # Welcome message
    st.markdown("---")
    st.markdown(f"### 👋 Welcome back, {st.user.name}!")
    
    # Main features overview
    st.markdown("## 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 👥 User Management
        - **Create your primary account** to manage medical records
        - **Grant access** to family members, caretakers, or friends via email
        - **Control permissions** for shared access to sensitive health information
        
        ### 📄 Data Ingestion
        - **Upload PDFs** of medical reports, lab results, and prescriptions
        - **Add images/screenshots** of medical documents or test results
        - **Type notes directly** about symptoms, medications, or appointments
        """)
    
    with col2:
        st.markdown("""
        ### 💬 Q&A Interface
        - **Ask questions** about your medical documents in natural language
        - **Get clarifications** on health parameters (A1C, cholesterol, etc.)
        - **Understand prescriptions** and medication instructions
        - **Track health trends** with AI-powered insights
        
        ### 🔗 Shared Access
        - **Authorized users** can log in and access shared documents
        - **Collaborative care** - family members and caretakers stay informed
        - **Secure communication** about medical history and treatment plans
        """)
    
    # Call to action
    st.markdown("---")
    st.markdown("## 🚀 Ready to Get Started?")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("💬 Ask Questions", use_container_width=True):
            st.switch_page("pages/02_Chat.py")
    
    with action_col2:
        if st.button("👥 Manage Access", use_container_width=True):
            st.switch_page("pages/00_Resgiter.py")
    
    with action_col3:
        if st.button("🔒 Manage Uploads", use_container_width=True):
            st.switch_page("pages/01_Upload.py")
    
    # Help section
    with st.expander("❓ How to Use CareTaker"):
        st.markdown("""
        **1. Create Your Account**: Sign up to create your primary CareTaker account
        
        **2. Upload Medical Documents**: Add PDFs, images, or type notes about your medical history
        
        **3. Ask Questions**: Use our AI chat to understand your health information better
        
        **4. Share Access**: Invite family members or caretakers to collaborate on your care
        
        **5. Stay Informed**: Everyone with access can chat with the documents to understand your health
        """)