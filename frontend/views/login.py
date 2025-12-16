import streamlit as st
import bcrypt
from backend.utils import data_manager

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def show():
    st.markdown("""
        <style>
        .login-container {
            display: flex;
            justify_content: center;
            align-items: center;
            height: 100vh;
        }
        .stTextInput > div > div > input {
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.header("Login to NxtQube")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if not email or not password:
                st.error("Please enter both email and password")
                return

            try:
                user = data_manager.get_user_by_email(email)
                
                if user and check_password(password, user['password']):
                    st.session_state.logged_in = True
                    st.session_state.user_id = user['id']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
