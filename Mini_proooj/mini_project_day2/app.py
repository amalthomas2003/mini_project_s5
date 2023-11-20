from flask import Flask, request, render_template, redirect, url_for, session,jsonify,send_from_directory
from flask_mysqldb import MySQL
import details
from datetime import datetime,date
import re


current_date = date.today()
current_date_str = current_date.strftime('%Y-%m-%d') #in yyyy-mm-dd format

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'amalahsanrohitrohan'  # Replace with a secure secret key
app.config['TEMPLATES_AUTO_RELOAD'] = True  
###handle internal error due to missing column values


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html'), 500





#initialize variables
#session={"hr_logged_in","student_logged_in","admin_logged_in"}
element_found=False 
#hr_logged_in=False
#student_logged_in=False
#admin_logged_in=False



# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'careerconnect'
app.config['MYSQL_DB'] = 'maindb'
mysql = MySQL(app)




############################################################################################login starts here###########################################
@app.route('/', methods=['GET', 'POST'])
def login():


    global element_found
    global hr_logged_in
    global student_logged_in
    global admin_logged_in
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        # Check the user's role based on the email domain
        if user_id.endswith(details.student_userid_ends_with()):
            role = 'student'
            logintable='student_login'
            element_found=True
        elif user_id.endswith(details.admin_userid_ends_with()):
            role = 'college_admin'
            logintable='admin_login'
            element_found=True
        elif element_found==False:
            for x in details.company_hr_userid_ends_with():
                if user_id.endswith(x):
                    role = 'company_hr'
                    logintable='company_hr_login'
                    session["company_name"]=user_id[user_id.index("@")+1:-3] #find the name of the company from userid 
                    break

        else:
            session.clear()
            return "Invalid user ID"

        # Query the database to check if the user and password match
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {logintable} WHERE userid = %s AND password = %s", (user_id, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # if  User exists, set a session variable for their role
            session['user_id'] = user[1]
            session['role'] = role
            

            if role == 'student':
                return redirect(url_for('student_dashboard'))
            elif role == 'college_admin':
                return redirect(url_for('college_admin_dashboard'))
            elif role == 'company_hr':
                return redirect(url_for('company_hr_dashboard'))
        else:
            return redirect(url_for('invalid_login_credentials'))

    return render_template('login.html')
@app.route('/student_images/<path:filename>')
def student_images(filename):
    return send_from_directory('student_images', filename)
@app.route('/student_dashboard',methods=["GET","POST"])
def student_dashboard():
    #print("1")
    if 'user_id' in session and session['role'] == 'student':
        #print("2")
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT name,cgpa,dob,batch,points,graduation_year FROM student_details WHERE userid = %s", (session["user_id"],))
        details_of_student_for_session_dict=cursor.fetchone()
        session['student_name']=details_of_student_for_session_dict[0]
        session['cgpa']=details_of_student_for_session_dict[1]
        session['dob']=details_of_student_for_session_dict[2]
        session['batch']=details_of_student_for_session_dict[3]
        session['cc_points']=details_of_student_for_session_dict[4]
        session['graduation_year']=details_of_student_for_session_dict[5]
        return render_template(
            'student_dashboard.html', 
            student_name=session['student_name'],
            student_uid=session['user_id'],
            student_dob=session['dob'],
            student_cgpa=session['cgpa'],
            student_branch=session['batch'],
            student_image=session['user_id'][0:8]+'.jpeg',
            cc_points=session['cc_points']
            
            )
    else:
        return redirect(url_for('login'))
    

@app.route('/college_admin_dashboard')
def college_admin_dashboard():
    if 'user_id' in session and session['role'] == 'college_admin':
        return "Welcome to the college admin dashboard!"
    else:
        return redirect(url_for('login'))

@app.route('/company_hr_dashboard')
def company_hr_dashboard():
    if 'user_id' in session and session['role'] == 'company_hr':
        
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT power FROM interview_details WHERE company_name = %s", (session["company_name"],))
        power=cursor.fetchone()[0]
        if power==0:
            power="Placement Drive is OFF"
        else:
            power="Placement Drive is ON"
        cursor.execute("SELECT company_description,interview_detail FROM interview_details WHERE company_name = %s",(session["company_name"],))
        details_of_company=cursor.fetchone()
        cursor.execute("SELECT min_cgpa,batch,graduation_year FROM company_requirements WHERE company_name = %s",(session["company_name"],))
        company_requirements=cursor.fetchone()
        min_cgpa=company_requirements[0]
        branch=company_requirements[1]
        graduation_year=company_requirements[2]
        company_description=details_of_company[0]
        interview_detail=details_of_company[1]
        cursor.close()

        return render_template('company_hr_dashboard.html', company_name=session["company_name"],power=power,company_description=company_description,interview_detail=interview_detail,min_cgpa=min_cgpa,branch=branch,graduation_year=graduation_year)
    else:
        return redirect(url_for('login'))
    

@app.route('/login_failed')
def invalid_login_credentials():
    return "Invalid Details . Please Retry."


#decorator functtion for hr of the company
def hr_required(view_function):
    def decorated_function(*args, **kwargs):
        if 'user_id' in session and session['role'] == 'company_hr':
            return view_function(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function



#decorator function for company admin
def admin_required(view_function):
    def decorated_function(*args, **kwargs):
        if 'user_id' in session and session['role'] == 'college_admin':
            return view_function(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function







#decorator function for students

def student_required(view_function):
    def decorated_function(*args, **kwargs):
        if 'user_id' in session and session['role'] == 'student':
            return view_function(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function




#####################################login ends here###############################################################


#####################################company hr starts here########################################################
# HR Dashboard - Set Requirements

@app.route('/hr_dashboard/set_requirements', methods=['GET', 'POST'], endpoint='set_requirements_endpoint')
@hr_required  #here no error
def set_requirements():

    if request.method == 'POST':
        min_cgpa = request.form.get('cgpa')
        graduation_year=request.form.get('passoutyear')
        temp_batch= request.form.get('additionalRequirement')
        temp_batch=temp_batch.upper()
        print(temp_batch)
        

        # Establish a database connection using the mysql object
        cur = mysql.connection.cursor()

        # Update company requirements in the database
        cur.execute("UPDATE company_requirements SET min_cgpa = %s, graduation_year = %s, batch = %s WHERE company_name = %s", (min_cgpa, graduation_year,temp_batch,session["company_name"]))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('company_hr_dashboard'))

    return render_template('change_interview_requirements.html')

#For displaying current requirement

@app.route('/hr_dashboard/current_requirements', endpoint='current_requirements_endpoint')
@hr_required 
def current_requirements():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM company_requirements WHERE company_name = %s", (session['company_name'],))
    temp = cur.fetchone()
    cur.close()

    if temp is not None:
        return render_template('current_requirements.html', requirement1=temp[2], requirement2=temp[3], requirement3=temp[4].upper())
    



@app.route('/hr_dashboard/eligible_students',endpoint="eligible_students_endpoint")
@hr_required
def eligible_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM company_requirements WHERE company_name = %s" , (session['company_name'],))
    temp_company_requirements = cur.fetchone()
    batch_details=tuple(temp_company_requirements[4].upper().split(","))

    cur.execute("SELECT * FROM student_details a WHERE cgpa >= %s AND graduation_year= %s AND batch in %s", (temp_company_requirements[2],temp_company_requirements[3],batch_details))
    eligible_students_data = cur.fetchall()
    cur.close()
    print(eligible_students_data)

    return render_template('eligible_students.html',eligible_students=eligible_students_data)


#code for applied students
@app.route('/hr_dashboard/applied_candidates',endpoint="applied_students_endpoint")
@hr_required
def applied_students():
    cur=mysql.connection.cursor()
    cur.execute("""
    SELECT * 
    FROM student_details AS SD
    JOIN applied_companies AS AC
    ON SD.userid = AC.user_id 
    WHERE AC.company_name = %s
""", (session['company_name'],))

    applied_students_details=cur.fetchall()
    print(applied_students_details)
    cur.close()
    return render_template('applied_candidates.html',applied_students=applied_students_details)




#code to start/stop placement drive
@app.route('/hr_dashboard/toggle_power', endpoint='toggle_power_endpoint')
@hr_required
def toggle_power():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT power FROM interview_details WHERE company_name = %s", (session['company_name'],))
    current_power = cur.fetchone()[0]
    new_power = 1 - current_power

    # Update the power value in the database
    cur.execute("UPDATE interview_details SET power = %s WHERE company_name = %s", (new_power, session['company_name']))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('company_hr_dashboard'))


#set interview Details

@app.route("/hr_dashboard/change_interview_details",methods=['GET', 'POST'],endpoint="edit_interview_details_endpoint")
@hr_required
def edit_interview_details():
    if request.method == 'POST':
        content = request.form['content']  # Get the edited content from the POST request
        interview_date=request.form['interview_date']
        interview_deadline=request.form['last_date']
        print(interview_deadline)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE interview_details SET interview_detail = %s , interview_date = %s , last_date = %s  WHERE company_name = %s", (content, interview_date, interview_deadline, session['company_name']))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('company_hr_dashboard'))
    return render_template("change_interview_details.html")




#define the logout function
@app.route('/hr_dashboard/logout',endpoint="logout_endpoint")
@hr_required
def logout():
    session.clear()
    return redirect(url_for('login'))


#define the edit company details function
@app.route('/hr_dashboard/change_company_details', methods=['GET', 'POST'], endpoint="company_details_endpoint")
@hr_required
def change_company_details():
    if request.method == 'POST':
        content = request.form['content']  
        cur = mysql.connection.cursor()
        cur.execute("UPDATE interview_details SET company_description = %s WHERE company_name = %s", (content, session['company_name']))
        mysql.connection.commit()
        cur.close()
        success_message = "Save Success"
        response = jsonify({'message': success_message})
        response.status_code = 200
        return response

    return render_template("change_company_details.html")

# Function to update application status in the applied_companies table
def update_application_status(user_id, decision):
    
    cursor=mysql.connection.cursor()

    # Update the application_status based on the decision
    if decision == 'accept':
        update_query = "UPDATE applied_companies SET application_status = 1 WHERE user_id = %s AND company_name = %s"
    elif decision == 'reject':
        update_query = "UPDATE applied_companies SET application_status = 0 WHERE user_id = %s AND company_name = %s"
    elif decision == 'wait':
            update_query = "UPDATE applied_companies SET application_status = 2 WHERE user_id = %s AND company_name = %s"
    else:
        raise ValueError("Invalid decision")

    cursor.execute(update_query, (user_id,session['company_name']))
    mysql.connection.commit()
    cursor.close()

# Route to display the application scrutiny page
@app.route('/hr_dashboard/application_scrutiny')
def application_scrutiny():
    # Dummy data (replace with actual data retrieval logic)
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT AC.user_id,AC.student_name,SD.batch,application_status FROM applied_companies AS AC JOIN student_details AS SD ON AC.user_id = SD.userid WHERE AC.company_name = %s",(session['company_name'],))
    students=list(cursor.fetchall())
    print(students)
    return render_template('scrutiny.html', students=students)

# Route to process the decision made for each student
@app.route('/hr_dashboard/process_decision', methods=['POST'])
def process_decision():
    user_id = request.form.get('user_id')
    decision = request.form.get('decision')

    update_application_status(user_id, decision)

    return redirect(url_for('application_scrutiny'))




######################################################company hr ends here############################


######################################################Student Starts here################################


@app.route('/student_dashboard/eligible_companies', endpoint="eligible_companies_endpoint")
def eligible_companies():
    cur = mysql.connection.cursor()

    if details.is_valid_date(session['dob']):
        pass
    else:
        date_str = session['dob']
        parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        session['dob'] = parsed_date.strftime('%Y-%m-%d') 


    cur.execute("""
        SELECT CR.company_name
        FROM company_requirements AS CR
        JOIN interview_details AS ID ON CR.company_name = ID.company_name
        WHERE CR.min_cgpa < %s
        AND CR.graduation_year = %s
        AND CR.batch LIKE %s
        AND ID.power = 1
        AND ID.last_date > %s
        """, (session['cgpa'], session['graduation_year'], '%' + session['batch'] + '%', current_date_str))
    companies = cur.fetchall()    
    if len(companies)>0:
        data = companies
        companies = tuple(item for sublist in data for item in sublist)
    cur.execute("SELECT DISTINCT company_name FROM applied_companies WHERE user_id = %s",(session['user_id'],))
    see_applied_companies = cur.fetchall()
    print(see_applied_companies)
    if see_applied_companies!=():
        see_applied_companies = tuple(item[0] for item in see_applied_companies)
        print(see_applied_companies)

    cur.close()
    return render_template("eligible_companies.html", companies=companies,existing_companies=see_applied_companies)


@app.route('/student_dashboard/handle_application', methods=['POST'])
def handle_application():    
    action=request.form.get('action')
    #print(action)
    if action=='apply':
        company_name=request.form.get('company_name')
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO applied_companies (user_id,student_name,company_name,application_status) VALUES (%s,%s,%s,%s)",(session['user_id'],session['student_name'],company_name,2))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('eligible_companies_endpoint'))


@app.route('/student_dashboard/view_inerview_details',methods=['POST'])
def view_interview_details():
    action=request.form.get('action')
    print(action)
    #print("hi")
    if action == 'see_interview_details':
        #print("hi")
        company_name=request.form.get('company_name')
        cur=mysql.connection.cursor()
        cur.execute("SELECT interview_detail,last_date,interview_date,company_description FROM interview_details where company_name = %s",(company_name,))
        view_interview_details_data=cur.fetchone()
        #print(view_interview_details_data)
        cur.close()
    return render_template(
        "view_interviewdetails.html",
        company_name=company_name,
        interview_detail=view_interview_details_data[0],
        interview_date=view_interview_details_data[2],
        last_date=view_interview_details_data[1],
        company_description=view_interview_details_data[3] 
        )

@app.route('/student_dashboard/post_questions', methods=['GET','POST'], endpoint='post_question_endpoint')
#2 for waiting question approval
#1 for approved questtions
#0 for rejected questtions
def post_questions():
    #print("Hi")
    if request.method == 'POST':
        print(request.method)
        tags = request.form.get('tags')
        print(tags)
        c_name=request.form.get('c_name')
        print(c_name)
        content = request.form.get('content')
        print(content)
        cur=mysql.connection.cursor()
        question_date=datetime.now().strftime("%Y-%m-%d")
        if tags !=None and c_name != None:
            print("yay")
            cur.execute("INSERT INTO questions(tags,userid,username,question,status,question_date,company_name) VALUES (%s,%s,%s,%s,%s,%s,%s)",(tags,session['user_id'],session['student_name'],content,1,question_date,c_name))
            mysql.connection.commit()
            cur.close()
        return redirect(url_for('student_dashboard'))
    return render_template("post_interview_questions.html")

@app.route('/student_dashboard/view_questions', methods=['GET','POST'], endpoint='view_question_endpoint')
def view_questions():
    if request.method == 'GET':
        cur=mysql.connection.cursor()
        cur.execute("""
            SELECT Q.username, Q.userid, Q.question, Q.question_date, Q.tags, Q.company_name, SD.points , Q.q_id
            FROM questions AS Q
            JOIN student_details AS SD ON Q.userid = SD.userid
            WHERE Q.status = 1 
            ORDER BY Q.question_date DESC
        """)
        all_questions=cur.fetchall()
        questions_data=list(all_questions)
        cur.close()
        questions_data1=[]
        for question in questions_data:
            rank = details.choose_rank(question[6])
            font_style=rank[0]
            name_color=rank[1]
            style=rank[2]
            weight=rank[3]
            size=rank[4]
            question+=(font_style,name_color,style,weight,size)
            questions_data1.append(question)
        cur=mysql.connection.cursor()
        cur.execute("SELECT COUNT(q_id) FROM questions")
        total_questions=cur.fetchone()
        cur.close()
        #print(total_questions[0])

        


    return render_template('questions.html', questions_data=questions_data1,q_suffix=details.q_suffix(),q_prefix=details.q_prefix(),total_questions=total_questions,items_per_page=10)

@app.route('/student_dashboard/view_result')
def view_result():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT company_name,application_status FROM applied_companies WHERE user_id = %s",(session['user_id'],))
    interview_results=list(cursor.fetchall())
    cursor.close()
    return render_template('results.html', interview_results=interview_results)



@app.route('/student_dashboard/view_my_questions')
def view_my_questions():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT q_id,company_name,question_date,status FROM questions WHERE userid = %s ORDER BY q_id DESC",(session['user_id'],))
    questions=list(cursor.fetchall())
    cursor.close()
    return render_template('myquestions.html', questions=questions ,prefix=details.q_prefix(),suffix=details.q_suffix())



@app.route('/student_dasboard/view_my_questions/view_the_question',methods=["GET","POST"],endpoint="view_the_question_endpoint")
def view_the_question():
    action=request.form.get('action')
    if action=='apply':
        q_id=request.form.get('q_id')
        cur=mysql.connection.cursor()
        cur.execute("SELECT question FROM questions WHERE q_id = %s ",(q_id,))
        the_question=cur.fetchone()
        cur.close()
        print(the_question)
    return render_template('the_question.html',the_question=the_question[0])



@app.route('/student_dashboard/view_question/questions_search', methods=['GET'])
def questions_search():
    search_text = request.args.get('search_text').lower()


    if search_text:
        cur=mysql.connection.cursor()
        cur.execute("""
            SELECT Q.username, Q.userid, Q.question, Q.question_date, Q.tags, Q.company_name, SD.points , Q.q_id
            FROM questions AS Q
            JOIN student_details AS SD ON Q.userid = SD.userid
            WHERE Q.status = 1
            ORDER BY Q.question_date DESC
        """)
        all_questions=cur.fetchall()
        questions_data=list(all_questions)
        cur.close()
        questions_data1=[]
        for question in questions_data:
            rank = details.choose_rank(question[6])
            font_style=rank[0]
            name_color=rank[1]
            style=rank[2]
            weight=rank[3]
            size=rank[4]
            question+=(font_style,name_color,style,weight,size)
            if (re.search(r'{}'.format(re.escape(search_text)),str(question[0]).lower()) or
                re.search(r'{}'.format(re.escape(search_text)),str(question[1]).lower()) or
                re.search(r'{}'.format(re.escape(search_text)),str(question[2]).lower()) or
                re.search(r'{}'.format(re.escape(search_text)),str(question[3]).lower()) or
                re.search(r'{}'.format(re.escape(search_text)),str(question[4]).lower()) or
                re.search(r'{}'.format(re.escape(search_text)),str(question[5]).lower()) or
                re.search(r'{}'.format(re.escape(search_text)),str(question[6]).lower()) or
                re.search(r'{}'.format(re.escape(search_text)),str(question[7]).lower()) or
                re.search(r'{}'.format(re.escape(search_text)),str(details.q_prefix().lower()+str(question[7]).lower())+details.q_suffix().lower())):
                questions_data1.append(question)
    else:
        return redirect(url_for('view_question_endpoint'))


    return render_template('questions.html', questions_data=questions_data1,q_suffix=details.q_suffix(),q_prefix=details.q_prefix())
       
    




@app.route('/student_dashboard/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))








if __name__ == '__main__':
    app.run(debug=True)
