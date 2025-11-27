import streamlit as st
from utils.data_manager import get_mock_reports

def show():
    st.title("Dashboard")
    st.write("Welcome to the Dashboard.")
    
    # Placeholder metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Reports", len(get_mock_reports()))
    m2.metric("QRs Generated Today", "125")
    m3.metric("System Status", "Active")
    
    st.bar_chart({'Data': [10, 20, 30, 40, 50]})
