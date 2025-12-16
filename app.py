import streamlit as st
from frontend.views import qr_generation, reports, dashboard, visualization

def main():
    st.title("NxtQube - ASRS Drone Inventory Verification System")

    st.set_page_config(page_title="ASRS Manager", layout="wide")
    
    st.sidebar.image("frontend/logos/mahindra-auto-logo-png_seeklogo-613492.webp", use_container_width=True)
    st.sidebar.title("Navigation")
    if "current_view" not in st.session_state:
        st.session_state.current_view = "QR Generation"

    # Navigation Buttons
    if st.sidebar.button("QR Generation", use_container_width=True, type="primary" if st.session_state.current_view == "QR Generation" else "secondary"):
        st.session_state.current_view = "QR Generation"
        st.rerun()
        
    if st.sidebar.button("Reports", use_container_width=True, type="primary" if st.session_state.current_view == "Reports" else "secondary"):
        st.session_state.current_view = "Reports"
        st.rerun()

    if st.sidebar.button("Visualization", use_container_width=True, type="primary" if st.session_state.current_view == "Visualization" else "secondary"):
        st.session_state.current_view = "Visualization"
        st.rerun()

    if st.sidebar.button("Dashboard", use_container_width=True, type="primary" if st.session_state.current_view == "Dashboard" else "secondary"):
        st.session_state.current_view = "Dashboard"
        st.rerun()
    st.sidebar.image("frontend/logos/Mahindra-Logistics.png", use_container_width=True)
    
    selection = st.session_state.current_view
    
    if selection == "QR Generation":
        qr_generation.show()
    elif selection == "Reports":
        reports.show()
    elif selection == "Visualization":
        visualization.show()
    elif selection == "Dashboard":
        dashboard.show()

if __name__ == "__main__":
    main()
