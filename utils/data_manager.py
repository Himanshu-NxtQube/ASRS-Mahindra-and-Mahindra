import streamlit as st
import pandas as pd
from datetime import datetime
import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

conn = pymysql.connect(
    host=os.getenv("rds_host"),  # RDS Endpoint
    user=os.getenv("rds_user"),                    # DB username
    password=os.getenv("rds_password"),                # DB password
    database=os.getenv("rds_dbname"),           # Target DB name
    port=int(os.getenv("rds_port", 3306))                                # Default MySQL port
)

def get_latest_raw_data():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM `raw-data` ORDER BY createdAt DESC LIMIT 1;")
        result = cursor.fetchone()
        return result

def get_new_unique_id():
    _id, unique_id, vin_no, createdAt, updatedAt, isDispatched = get_latest_raw_data()

    if int(unique_id[3:]) != 9999:
        next_unique_id = unique_id[:3] + str(int(unique_id[3:]) + 1)
    else:
        if unique_id[2] != 'Z':
            next_unique_id = unique_id[:2] + chr(ord(unique_id[2]) + 1) + '1111'
        else:
            next_unique_id = unique_id[:1] + chr(ord(unique_id[1]) + 1) + 'A' + '1111'

    return next_unique_id
    
def get_reports():
    """Simulates fetching report list from SQL."""
    # if 'reports' not in st.session_state:
    #     st.session_state.reports = [
    #         {'id': 1, 'name': 'Sales Report Q1', 'date': '2025-11-27'},
    #         {'id': 2, 'name': 'Inventory Log', 'date': '2025-11-26'},
    #         {'id': 3, 'name': 'Employee Audit', 'date': '2025-11-25'},
    #     ]
    # return st.session_state.reports

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM `reports`;")
        result = cursor.fetchall()
        return result

def get_report_details(report_id):
    """Simulates fetching detailed rows for a specific report from SQL."""
    # Just generating some dummy data based on ID
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM `inferances`;")
        result = cursor.fetchone()
        return result


def delete_report(report_id):
    """Simulates deleting a report."""
    st.session_state.reports = [r for r in st.session_state.reports if r['id'] != report_id]
    st.toast(f"Report {report_id} deleted!", icon="🗑️")
