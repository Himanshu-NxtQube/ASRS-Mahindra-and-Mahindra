import streamlit as st
import pandas as pd
from utils.data_manager import get_reports, get_report_details, delete_report
from datetime import datetime

def show():
    st.header("Reports")
    date = st.date_input("Date", datetime.now().date())
    if 'selected_report_id' in st.session_state and st.session_state.selected_report_id is not None:
        report_id = st.session_state.selected_report_id
        reports = get_reports(date)
        
        if reports:
            # Note: User swapped indices: 1 is Name, 2 is Date (based on list view logic below)
            # But wait, the list view logic says: report_name = report[1], report_date = report[2]
            # So here we should probably match that if we want consistency.
            # However, the previous code had report_name = r[2]. 
            # The user explicitly changed the list view to be report[1] for name.
            # So I should update this lookup to match report[1] for name.
            report_name = next((r[1] for r in reports if r[0] == report_id), "Unknown Report")
        else:
            report_name = "Unknown Report"
        
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("← Back"):
                st.session_state.selected_report_id = None
                st.rerun()
        with col_title:
            st.subheader(f"Details: {report_name}")
            
        details_data = get_report_details(report_id)
        
        if details_data:
            df_details = pd.DataFrame(details_data)
            # Select 2nd, 3rd, 4th, 5th, 6th columns and rename
            df_details = df_details.iloc[:, [1, 2, 3, 4, 5]]
            df_details.columns = ['Unique ID', 'Image Name', 'VIN No.', 'Quantity', 'Exclusion']
            st.dataframe(df_details, use_container_width=True)
        else:
            st.info("No details available for this report.")
        
    else:
        reports = get_reports(date)
        
        if not reports:
            st.info("No reports found.")
            return

        col1, col2, col3 = st.columns([3, 2, 4])
        col1.markdown("**Report Name**")
        col2.markdown("**Date**")
        col3.markdown("**Actions**")
        st.divider()

        for report in reports:
            if len(report) < 3:
                continue
                
            c1, c2, c3 = st.columns([3, 2, 4])
            
            report_id = report[0]
            report_name = report[1]
            report_date = report[2]
            
            if c1.button(report_name, key=f"view_{report_id}"):
                st.session_state.selected_report_id = report_id
                st.rerun()
                
            c2.write(report_date.strftime('%Y-%m-%d'))
            
            with c3:
                ac1, ac2, ac3 = st.columns(3)
                with ac1:
                    st.download_button(
                        label="⬇️",
                        data=f"Mock data for {report_name}",
                        file_name=f"{report_name}.txt",
                        key=f"dl_{report_id}",
                        help="Download Report"
                    )
                with ac2:
                    if st.button("✏️", key=f"edit_{report_id}", help="Edit Report"):
                      st.toast(f"Edit feature for {report_name} coming soon!", icon="🚧")
                with ac3:
                    if st.button("🗑️", key=f"del_{report_id}", help="Delete Report"):
                        delete_report(report_id)
                        st.rerun()
            st.divider()
