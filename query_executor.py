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


with conn.cursor() as cursor:
    # cursor.execute("DROP TABLE IF EXISTS `raw-data`;")
    # cursor.execute("""
    #     CREATE TABLE `raw-data` (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         unique_id CHAR(7),
    #         vin_no VARCHAR(25),
    #         createdAt DATETIME,
    #         updatedAt DATETIME,
    #         isDispatched BOOLEAN
    #     );
    # """)
    
    # cursor.execute("INSERT INTO `raw-data` (unique_id, vin_no, createdAt, updatedAt, isDispatched) VALUES('@AA1116', 'BN4222JH', NOW(), NOW(), 0);")
    # cursor.execute("SELECT * FROM `raw-data`;")
    # cursor.execute("""CREATE TABLE `inferences` (
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     unique_id CHAR(7),
    #     image_name VARCHAR(255),
    #     vin_no VARCHAR(25),
    #     quantity INT,
    #     exclusion VARCHAR(255),
    #     createdAt DATETIME,
    #     updatedAt DATETIME,
    #     report_id INT,
    #     is_non_confirmity BOOLEAN,
    #     FOREIGN KEY (report_id) REFERENCES `reports` (id)
    # );""")
    # cursor.execute("INSERT INTO `inferences` \
    #     (unique_id, image_name, vin_no, quantity, \
    #     exclusion, createdAt, updatedAt, report_id, \
    #     is_non_confirmity) \
    #     VALUES \
    #     ('@AA1120', 'DJI_0002.JPG', 'HY322NHD', 1, \
    #     '', NOW(), NOW(), 2, 0);")
    # cursor.execute("SELECT * FROM `inferences`;")
    # cursor.execute("Describe `reports`;")
    # query = f"""use asrs_zypher; create table `raw-data`(unique_id char(7), vin_no varchar(25), createdAt datetime, updatedAt datetime, isDispatched boolean); describe `raw-data`;"""
    # cursor.execute(query)
    # cursor.execute("INSERT INTO reports (report_name, createdAt) VALUES ('Report 1', NOW());")
    # cursor.execute("INSERT INTO `raw-data` (unique_id, vin_no, createdAt, updatedAt, isDispatched) VALUES('@AA1116', 'BN4222JH', NOW(), NOW(), 0);")
    # conn.commit()

    # cursor.execute("SELECT * FROM `raw-data`;")

    # Now write a query to create a new report named as "Report 2"
    # cursor.execute("INSERT INTO reports (report_name, createdAt) VALUES ('Report 2', NOW());")

    # Also write a query to insert 5 rows into inferences table where report_id = 3
    # cursor.execute("INSERT INTO `inferences` (unique_id, image_name, vin_no, quantity, exclusion, createdAt, updatedAt, report_id, is_non_confirmity) VALUES ('@AA1120', 'DJI_0002.JPG', 'HY322NHD', 1, '', NOW(), NOW(), 3, 0);")
    # cursor.execute("INSERT INTO `inferences` (unique_id, image_name, vin_no, quantity, exclusion, createdAt, updatedAt, report_id, is_non_confirmity) VALUES ('@AA1121', 'DJI_0003.JPG', 'HY322NHD', 1, '', NOW(), NOW(), 3, 0);")
    # cursor.execute("INSERT INTO `inferences` (unique_id, image_name, vin_no, quantity, exclusion, createdAt, updatedAt, report_id, is_non_confirmity) VALUES ('@AA1122', 'DJI_0004.JPG', 'HY322NHD', 1, '', NOW(), NOW(), 3, 0);")
    # cursor.execute("INSERT INTO `inferences` (unique_id, image_name, vin_no, quantity, exclusion, createdAt, updatedAt, report_id, is_non_confirmity) VALUES ('@AA1123', 'DJI_0005.JPG', 'HY322NHD', 1, '', NOW(), NOW(), 3, 0);")
    # cursor.execute("INSERT INTO `inferences` (unique_id, image_name, vin_no, quantity, exclusion, createdAt, updatedAt, report_id, is_non_confirmity) VALUES ('@AA1124', 'DJI_0006.JPG', 'HY322NHD', 1, '', NOW(), NOW(), 3, 0);")
    # cursor.execute("SELECT * FROM inferences;")
    cursor.execute("DESCRIBE reports;")

    conn.commit()
    res = cursor.fetchall()
    print(len(res), "rows found in result")
    for row in res:
        print(row)
    # print(res)
