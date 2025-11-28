import streamlit as st
import pandas as pd
import datetime
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

def get_latest_unique_id():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM `raw-data` ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
        return result[1]

def insert_raw_data(vin_no, date):
    next_unique_id = get_next_unique_id()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO `raw-data` (unique_id, vin_no, createdAt, updatedAt, isDispatched) VALUES(%s, %s, %s, NOW(), 0);", (next_unique_id, vin_no, date))
        conn.commit()

def get_next_unique_id():
    unique_id = get_latest_unique_id()

    if int(unique_id[3:]) != 9999:
        next_unique_id = unique_id[:3] + str(int(unique_id[3:]) + 1)
    else:
        if unique_id[2] != 'Z':
            next_unique_id = unique_id[:2] + chr(ord(unique_id[2]) + 1) + '1111'
        else:
            next_unique_id = unique_id[:1] + chr(ord(unique_id[1]) + 1) + 'A' + '1111'

    return next_unique_id
    
def get_reports(date=None):
    """Fetches report list from SQL, optionally filtered by date."""
    with conn.cursor() as cursor:
        if date:
            if isinstance(date, datetime.date):
                date_str = date.strftime('%Y-%m-%d')
            elif isinstance(date, str):
                date_str = date
            else:
                raise ValueError("Date must be a string or datetime.date object.")
            cursor.execute("SELECT * FROM `reports` WHERE createdAt = %s;", (date_str,))
        else:
            cursor.execute("SELECT * FROM `reports`;")
        result = cursor.fetchall()
        return result

def get_report_details(report_id):
    """Simulates fetching detailed rows for a specific report from SQL."""
    # Just generating some dummy data based on ID
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `inferences` where report_id = {report_id};")
        result = cursor.fetchall()
        return result


def delete_report(report_id):
    """Simulates deleting a report."""
    with conn.cursor() as cursor:
        cursor.execute(f"DELETE FROM `inferences` WHERE report_id = {report_id};")  
        cursor.execute(f"DELETE FROM `reports` WHERE id = {report_id};")
        conn.commit()
        