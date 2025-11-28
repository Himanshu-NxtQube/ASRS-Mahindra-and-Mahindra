import streamlit as st
from backend.utils.data_manager import get_reports, get_report_details
from datetime import datetime

def show():
    st.header("Visualization")

    date = st.date_input("Date", datetime.now().date())
    
    if 'selected_viz_report_id' in st.session_state and st.session_state.selected_viz_report_id is not None:
        report_id = st.session_state.selected_viz_report_id
        # Fetch report name for display
        reports = get_reports(date)
        
        report_name = "Report Gallery"
        if reports:
             found = next((r[1] for r in reports if r[0] == report_id), None)
             if found:
                 report_name = found
        
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("← Back"):
                st.session_state.selected_viz_report_id = None
                st.rerun()
        with col_title:
            st.subheader(f"{report_name}")
            
        details_data = get_report_details(report_id)
        
        if details_data:
            # Parse data to associate images with info
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
            
    else:
        reports = get_reports(date)
        
        if not reports:
            st.info("No reports found.")
            return

        col1, col2 = st.columns([3, 2])
        col1.markdown("**Report Name**")
        col2.markdown("**Date**")
        st.divider()

        for report in reports:
            if len(report) < 3:
                continue
                
            c1, c2 = st.columns([3, 2])
            
            report_id = report[0]
            report_name = report[1]
            report_date = report[2]
            
            if c1.button(report_name, key=f"viz_view_{report_id}"):
                st.session_state.selected_viz_report_id = report_id
                st.rerun()
                
            c2.write(report_date.strftime('%Y-%m-%d'))
            st.divider()
