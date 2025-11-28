import streamlit as st
<<<<<<< HEAD
import pandas as pd
from utils.data_manager import get_reports, get_report_details, delete_report
=======
from backend.utils.data_manager import get_reports, get_report_details
>>>>>>> cd02358 (feat: Implement a new visualization page with image galleries, add a custom Streamlit theme, and update sidebar navigation.)
from datetime import datetime

def show():
    st.header("Visualization")
<<<<<<< HEAD
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
=======

    date = st.date_input("Date", datetime.now().date())
    
    if 'selected_viz_report_id' in st.session_state and st.session_state.selected_viz_report_id is not None:
        report_id = st.session_state.selected_viz_report_id
        # Fetch report name for display
        reports = get_reports(date)
        # We need to handle the case where the report might not be in the current date filter if the user changed date while inside a report
        # But for now, let's assume the user flow is linear. 
        # Actually, if I change date, the list updates. If I am in details view, I should probably stay there or reset?
        # The user requirement says "date selector and below that report names".
        # If I click a report, it opens gallery.
        # It doesn't explicitly say the date selector should disappear or stay.
        # In reports.py, the date selector is at the top.
        
        # Let's try to find the name. If not found (e.g. date changed), just show "Report Details" or similar.
        # Or better, fetch the specific report by ID if I had a function for that.
        # I'll just look in the current list for now, or default to "Report Gallery".
        
        report_name = "Report Gallery"
        if reports:
             found = next((r[1] for r in reports if r[0] == report_id), None)
             if found:
                 report_name = found
>>>>>>> cd02358 (feat: Implement a new visualization page with image galleries, add a custom Streamlit theme, and update sidebar navigation.)
        
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("← Back"):
<<<<<<< HEAD
                st.session_state.selected_report_id = None
                st.rerun()
        with col_title:
            st.subheader(f"Details: {report_name}")
            
        # details_data = get_report_details(report_id)
        
        # if details_data:
        #     df_details = pd.DataFrame(details_data)
        #     # Select 2nd, 3rd, 4th, 5th, 6th columns and rename
        #     df_details = df_details.iloc[:, [1, 2, 3, 4, 5]]
        #     df_details.columns = ['Unique ID', 'Image Name', 'VIN No.', 'Quantity', 'Exclusion']
        #     st.dataframe(df_details, use_container_width=True)
        # else:
        #     st.info("No details available for this report.")
        
=======
                st.session_state.selected_viz_report_id = None
                st.rerun()
        with col_title:
            st.subheader(f"{report_name}")
            
        details_data = get_report_details(report_id)
        
        if details_data:
            # Parse data to associate images with info
            # Assuming columns based on reports.py logic: 
            # 1: Unique ID, 2: Image Name, 3: VIN No., 4: Quantity, 5: Exclusion
            # And looking for URL in the row as before
            
            gallery_items = []
            for row in details_data:
                url = None
                # Look for URL
                for item in row:
                    if isinstance(item, str) and (item.startswith("http://") or item.startswith("https://")):
                        url = item
                        break
                if not url and isinstance(row[-1], str) and len(row[-1]) > 5:
                    url = row[-1]
                
                if url:
                    # Store info. Note: row indices might need adjustment if the query changes, 
                    # but we stick to what reports.py uses + observation.
                    # reports.py uses: df_details.iloc[:, [1, 2, 3, 4, 5]] -> Unique ID, Image Name, VIN No., Quantity, Exclusion
                    # So:
                    # row[1] -> Unique ID
                    # row[2] -> Image Name
                    # row[3] -> VIN No.
                    # row[4] -> Quantity
                    # row[5] -> Exclusion
                    
                    info = {
                        "Unique ID": row[1] if len(row) > 1 else "N/A",
                        "Image Name": row[2] if len(row) > 2 else "N/A",
                        "VIN No.": row[3] if len(row) > 3 else "N/A",
                        "Quantity": row[4] if len(row) > 4 else "N/A",
                        "Exclusion": row[5] if len(row) > 5 else "N/A"
                    }
                    gallery_items.append({"url": url, "info": info})

            if 'selected_viz_image_index' not in st.session_state:
                st.session_state.selected_viz_image_index = None

            if st.session_state.selected_viz_image_index is not None:
                # Show Detail View
                idx = st.session_state.selected_viz_image_index
                if 0 <= idx < len(gallery_items):
                    item = gallery_items[idx]
                    
                    if st.button("← Back to Gallery"):
                        st.session_state.selected_viz_image_index = None
                        st.rerun()
                        
                    c_img, c_info = st.columns([1, 1])
                    with c_img:
                        st.image(item['url'], use_container_width=True)
                    with c_info:
                        with st.container(border=True):
                            st.subheader("Image Details")
                            st.divider()
                            
                            # Use metrics for key values
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.metric("Unique ID", item['info'].get("Unique ID", "N/A"))
                                st.metric("VIN No.", item['info'].get("VIN No.", "N/A"))
                            with col_b:
                                st.metric("Quantity", item['info'].get("Quantity", "N/A"))
                                st.metric("Exclusion", item['info'].get("Exclusion", "N/A"))
                            
                            st.divider()
                            st.caption(f"Image Name: {item['info'].get('Image Name', 'N/A')}")
                else:
                    st.error("Selected image not found.")
                    st.session_state.selected_viz_image_index = None
                    if st.button("Reset"):
                        st.rerun()
            
            elif gallery_items:
                # Display gallery
                cols = st.columns(4) # 4 columns grid
                for i, item in enumerate(gallery_items):
                    with cols[i % 4]:
                        st.image(item['url'], use_container_width=True)
                        if st.button("View Details", key=f"viz_img_{i}"):
                            st.session_state.selected_viz_image_index = i
                            st.rerun()
            else:
                st.info("No images found for this report.")
        else:
            st.info("No details available for this report.")
            
>>>>>>> cd02358 (feat: Implement a new visualization page with image galleries, add a custom Streamlit theme, and update sidebar navigation.)
    else:
        reports = get_reports(date)
        
        if not reports:
            st.info("No reports found.")
            return

<<<<<<< HEAD
        col1, col2, col3 = st.columns([3, 2, 4])
        col1.markdown("**Report Name**")
        col2.markdown("**Date**")
        #col3.markdown("**Actions**")
=======
        col1, col2 = st.columns([3, 2])
        col1.markdown("**Report Name**")
        col2.markdown("**Date**")
>>>>>>> cd02358 (feat: Implement a new visualization page with image galleries, add a custom Streamlit theme, and update sidebar navigation.)
        st.divider()

        for report in reports:
            if len(report) < 3:
                continue
                
<<<<<<< HEAD
            c1, c2, c3 = st.columns([3, 2, 4])
=======
            c1, c2 = st.columns([3, 2])
>>>>>>> cd02358 (feat: Implement a new visualization page with image galleries, add a custom Streamlit theme, and update sidebar navigation.)
            
            report_id = report[0]
            report_name = report[1]
            report_date = report[2]
            
<<<<<<< HEAD
            if c1.button(report_name, key=f"view_{report_id}"):
                st.session_state.selected_report_id = report_id
                st.rerun()
                
            c2.write(report_date.strftime('%Y-%m-%d'))
            
            with c3:
                ac1, ac2, ac3 = st.columns(3)
                # with ac1:
                #     st.download_button(
                #         label="⬇️",
                #         data=f"Mock data for {report_name}",
                #         file_name=f"{report_name}.txt",
                #         key=f"dl_{report_id}",
                #         help="Download Report"
                #     )
                # with ac2:
                #     if st.button("✏️", key=f"edit_{report_id}", help="Edit Report"):
                #       st.toast(f"Edit feature for {report_name} coming soon!", icon="🚧")
                # with ac3:
                    # if st.button("🗑️", key=f"del_{report_id}", help="Delete Report"):
                    #     delete_report(report_id)
                    #     st.rerun()
=======
            if c1.button(report_name, key=f"viz_view_{report_id}"):
                st.session_state.selected_viz_report_id = report_id
                st.rerun()
                
            c2.write(report_date.strftime('%Y-%m-%d'))
>>>>>>> cd02358 (feat: Implement a new visualization page with image galleries, add a custom Streamlit theme, and update sidebar navigation.)
            st.divider()
