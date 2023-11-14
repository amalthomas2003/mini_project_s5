'''Created tables in maindb

---LOGIN TABLES:
---admin_login
---student_login
---company_hr_login
---
---STUDENT TABLES:
---student_details
---questions
---
---
---COMPANY TABLES:
---company_requirements
---interview_details
---


'''



import pymysql

# Database connection configuration for a default database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "careerconnect",
    "database": "mysql"
}



# Create a connection to the database
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

#create a new database named logindb
new_database_name = "maindb"
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_database_name}")

db_config["database"]="maindb"
connection = pymysql.connect(**db_config)
cursor = connection.cursor()


# Create the 'admin login' table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        userid VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    )
""")

# Create the 'student login' table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        userid VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    )
""")

# Create the 'company_hr login' table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_hr_login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        userid VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    )
""")

admin_data = [
    ("mathews@rajagiri.admin.in", "12345"),
    ("admin1@rajagiri.admin.in", "password1"),
    ("admin2@rajagiri.admin.in", "password2"),
    ("admin3@rajagiri.admin.in", "password3"),
    ("admin4@rajagiri.admin.in", "password4")
]

for id, password in admin_data:
    cursor.execute("INSERT INTO admin_login (userid, password) VALUES (%s, %s)", (id, password))

# Insert data into the 'student' table
student_data = [
    ("u2109008@rajagiri.edu.in", "u210"),
    ("student1@rajagiri.edu.in", "password1"),
    ("student2@rajagiri.edu.in", "password2"),
    ("student3@rajagiri.edu.in", "password3"),
    ("student4@rajagiri.edu.in", "password4"),
    ("student5@rajagiri.edu.in", "password5"),
    ("student6@rajagiri.edu.in", "password6"),
    ("student7@rajagiri.edu.in", "password7"),
    ("student8@rajagiri.edu.in", "password8"),
    ("student9@rajagiri.edu.in", "password9"),
    ("student10@rajagiri.edu.in", "password10"),
    ("u2109031@rajagiri.edu.in","pp")
]

for id, password in student_data:
    cursor.execute("INSERT INTO student_login (userid, password) VALUES (%s, %s)", (id, password))


company_hr_data=[("rajesh@tcs.in","password1"),
                 ("ajith@wipro.in","ajith")]
for id,password in company_hr_data:
    cursor.execute("INSERT INTO company_hr_login (userid, password) VALUES (%s, %s)", (id, password))



#create table 'student_details' if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_details (
        id INT AUTO_INCREMENT PRIMARY KEY,
        userid VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        name VARCHAR(255) NOT NULL,
        cgpa FLOAT NOT NULL,
        dob DATE NOT NULL,
        batch VARCHAR(50) NOT NULL,
        points INT NOT NULL,
        applied_companies VARCHAR(255)
    )
""")

studentdetails_data=[
    ("u2109008@rajagiri.edu.in","u210","Amal Thomas","8","2003-09-12","CU",0),
    ("student1@rajagiri.edu.in","password1","john doe","9","2002-09-12","ME",0),
    ("student1@rajagiri.edu.in","password1","john doe","10","2005-09-12","EE",0),
    ("student1@rajagiri.edu.in","password1","john doe","6","2007-09-12","CU",0),
    ("student1@rajagiri.edu.in","password1","john doe","2","2009-09-12","CU",0),
    ("akshayg@rajagiri.edu.in","akshay","akshay g","10","2003-12-12","CU",0),
    ("u2109031@rajagiri.edu.in","pp","jose paul","10","2003-12-09","CU",0)
]

for userid, password,name,cgpa,dob,batch,points in studentdetails_data:
    cursor.execute("INSERT INTO student_details (userid, password,name,cgpa,dob,batch,points) VALUES (%s, %s,%s,%s,%s,%s,%s)", (userid, password,name,cgpa,dob,batch,points))



# Create table 'questions' if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        q_id INT AUTO_INCREMENT PRIMARY KEY,
        tags VARCHAR(250),
        userid VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        question TEXT,
        status INT NOT NULL,
        question_date DATE
    )
""")



questions_data=[
    ('oop,data structures,uml','u2109008@rajagiri.edu.in','Amal Thomas',"what is you name ?2@#$#@",0,"2023-12-12"),
    ('oop,data structures,uml','u2109008@rajagiri.edu.in','Amal Thomas',"what is you name ?2@#$#@",1,"2023-09-09"),
    ('oop,data structures,uml','u2109008@rajagiri.edu.in','Amal Thomas',"what is you name ?2@#$#@",0,"2023-08-09"),
    ('oop,data structures,uml','u2109008@rajagiri.edu.in','Amal Thomas',"what is you name ?2@#$#@",1,"2023-07-09"),
    ('akshay,sigma','akshayg@rajagiri.edu.in','akshay',"My name is GG",1,"2023-09-23")
]

for tags,userid,username,question,status,question_date in questions_data:
    cursor.execute("INSERT INTO questions (tags,userid,username,question,status,question_date) VALUES (%s,%s,%s,%s,%s,%s)", (tags,userid,username,question,status,question_date))

#create table 'company_requirements' if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_requirements (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(50) NOT NULL,
        min_cgpa FLOAT NOT NULL,
        max_dob DATE,
        batch VARCHAR(255) NOT NULL
        
    )
""")

company_requirements_data=[
    ("tcs",3,"2004-01-01","CU,EE,ME,EC"),
    ("wipro",4,"2005-01-01","CU"),
    ("infosys",5,"2004-02-01","CU,EE,ME,EC")
]

for company_name, min_cgpa,max_dob,batch in company_requirements_data:
    cursor.execute("INSERT INTO company_requirements (company_name,min_cgpa,max_dob,batch) VALUES (%s, %s,%s,%s)", (company_name, min_cgpa,max_dob,batch))



cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_details(
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(50) NOT NULL,
            company_description TEXT,
            interview_detail TEXT,
            last_date DATE,
            interview_date DATE,
            power INT
            
            
               
        )
    """)

interview_details_data=[
    ("tcs","Tata Consultancy Services Limited is an Indian multinational information technology services and consulting company headquartered in Mumbai. It is a part of the Tata Group and operates in 150 locations across 46 countries. In July 2022, it was reported that TCS had over 600,000 employees worldwide.","interview is held at hotel Blu Radission","2023-12-12","2023-12-30",1),
    ("wipro","We are Wipro","interview is held at hotel Saj Park","2023-12-12","2023-12-30",1),
    ("infosys","We are INfosys","interview is held at hotel Taj","2023-12-12","2023-12-30",1)
]

for company_name,company_description,interview_detail,last_date,interview_date,power in interview_details_data:
    cursor.execute("INSERT INTO interview_details (company_name,company_description,interview_detail,last_date,interview_date,power) VALUES (%s,%s,%s,%s,%s,%s)",(company_name,company_description,interview_detail,last_date,interview_date,power))

connection.commit()
cursor.close()
connection.close()







print("Database Created Successfully")