import streamlit as st
from views import qr_generation, reports, dashboard

def main():
    st.set_page_config(page_title="ASRS Manager", layout="wide")
    
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["QR Generation", "Reports", "Dashboard"])
    
    if selection == "QR Generation":
        qr_generation.show()
    elif selection == "Reports":
        reports.show()
    elif selection == "Dashboard":
        dashboard.show()

if __name__ == "__main__":
    main()
