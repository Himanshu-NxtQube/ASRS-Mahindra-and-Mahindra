import streamlit as st
from utils.data_manager import get_reports, get_report_details, delete_report

def show():
    st.header("Reports")

    # Check if we are in "Detail View" mode
    if 'selected_report_id' in st.session_state and st.session_state.selected_report_id is not None:
        # --- Detail View ---
        report_id = st.session_state.selected_report_id
        # Fetch fresh reports list to get the name
        reports = get_reports()
        report_name = next((r[2] for r in reports if r['id'] == report_id), "Unknown Report")
        
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("← Back"):
                st.session_state.selected_report_id = None
                st.rerun()
        with col_title:
            st.subheader(f"Details: {report_name}")
            
        df_details = get_report_details(report_id)
        st.dataframe(df_details, use_container_width=True)
        
    else:
        # --- List View ---
        reports = get_mock_reports()
        
        if not reports:
            st.info("No reports found.")
            return

        # Header Row
        col1, col2, col3 = st.columns([3, 2, 4])
        col1.markdown("**Report Name**")
        col2.markdown("**Date**")
        col3.markdown("**Actions**")
        st.divider()

        # Data Rows
        for report in reports:
            c1, c2, c3 = st.columns([3, 2, 4])
            
            # Report Name (Clickable to view details)
            if c1.button(report['name'], key=f"view_{report['id']}"):
                st.session_state.selected_report_id = report['id']
                st.rerun()
                
            c2.write(report['date'])
            
            # Actions Column
            with c3:
                ac1, ac2, ac3 = st.columns(3)
                with ac1:
                    # Download (Mock)
                    st.download_button(
                        label="⬇️",
                        data=f"Mock data for {report['name']}",
                        file_name=f"{report['name']}.txt",
                        key=f"dl_{report['id']}",
                        help="Download Report"
                    )
                with ac2:
                    # Edit (Mock)
                    if st.button("✏️", key=f"edit_{report['id']}", help="Edit Report"):
                        st.toast(f"Edit feature for {report['name']} coming soon!", icon="🚧")
                with ac3:
                    # Delete
                    if st.button("🗑️", key=f"del_{report['id']}", help="Delete Report"):
                        delete_report(report['id'])
                        st.rerun()
            st.divider()
