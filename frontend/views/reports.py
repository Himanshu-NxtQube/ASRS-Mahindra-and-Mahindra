import streamlit as st
import pandas as pd
from backend.utils.data_manager import get_reports, get_report_details, delete_report, create_report
from datetime import datetime
import threading
import os
from backend.inferences import get_inferences

def show():
    st.title("Reports")
    
    # Show toast if it exists in session state
    if 'toast_msg' in st.session_state:
        st.toast(st.session_state['toast_msg'], icon=st.session_state.get('toast_icon'))
        del st.session_state['toast_msg']
        if 'toast_icon' in st.session_state:
            del st.session_state['toast_icon']

    date = st.date_input("Date", datetime.now().date())
    # Create Report Section
    if "show_create_form" not in st.session_state:
        st.session_state.show_create_form = False

    if st.button("➕ Create Report"):
        st.session_state.show_create_form = not st.session_state.show_create_form

    if st.session_state.show_create_form:
        with st.container(border=True):
            st.subheader("Create New Report")
            new_report_name = st.text_input("Report Name")
            uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True)
            
            if st.button("Submit Report"):
                if new_report_name and uploaded_files:
                    report_id = create_report(new_report_name)
                    
                    st.session_state.show_create_form = False
                    st.session_state['toast_msg'] = f"Report '{new_report_name}' created! Saved {len(uploaded_files)} images"
                    st.session_state['toast_icon'] = "✅"
                    safe_name = "".join([c if c.isalnum() or c in (' ', '-', '_') else '_' for c in new_report_name]).strip().replace(' ', '_')

                    base_dir = "uploaded_reports"
                    report_dir = os.path.join(base_dir, safe_name)
    
                    
                    os.makedirs(report_dir, exist_ok=True)
                
                    saved_count = 0
                    for img_file in uploaded_files:
                        file_path = os.path.join(report_dir, img_file.name)
                        with open(file_path, "wb") as f:
                            f.write(img_file.getbuffer())
                        saved_count += 1
                    thread = threading.Thread(target=get_inferences, args=(report_dir, report_id))
                    st.toast("Inferences are being generated", icon="✅")
                    thread.start()
                    # except Exception as e:
                    #     st.error(f"Failed to save report images: {e}")
                    st.rerun()
                else:
                    st.error("Please provide a report name and upload at least one image.")

    
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
