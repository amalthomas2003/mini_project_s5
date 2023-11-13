from flask import Flask, request, render_template, redirect, url_for, session,jsonify,send_from_directory
from flask_mysqldb import MySQL
import details
from datetime import datetime,date


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
@app.route('/student_dashboard')
def student_dashboard():
    print("1")
    if 'user_id' in session and session['role'] == 'student':
        print("2")
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT name,cgpa,dob,batch FROM student_details WHERE userid = %s", (session["user_id"],))
        details_of_student_for_session_dict=cursor.fetchone()
        session['student_name']=details_of_student_for_session_dict[0]
        session['cgpa']=details_of_student_for_session_dict[1]
        session['dob']=details_of_student_for_session_dict[2]
        session['batch']=details_of_student_for_session_dict[3]
        return render_template(
            'student_dashboard.html', 
            student_name=session['student_name'],
            student_uid=session['user_id'],
            student_dob=session['dob'],
            student_cgpa=session['cgpa'],
            student_branch=session['batch'],
            student_image=session['user_id'][0:8]+'.jpeg'
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

        return render_template('company_hr_dashboard.html', company_name=session["company_name"],power=power)
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







#decoratro function for students

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

        min_cgpa = request.form['min_cgpa']
        max_dob = request.form['max_dob']
        temp_batch=request.form['batch']

        # Establish a database connection using the mysql object
        cur = mysql.connection.cursor()

        # Update company requirements in the database
        cur.execute("UPDATE company_requirements SET min_cgpa = %s, max_dob = %s, batch = %s WHERE company_name = %s", (min_cgpa, max_dob,temp_batch,session["company_name"]))
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
    



@app.route('/hr_dashboard/elgible_students',endpoint="eligible_students_endpoint")
@hr_required
def eligible_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM company_requirements WHERE company_name = %s" , (session['company_name'],))
    temp_company_requirements = cur.fetchone()
    batch_details=tuple(temp_company_requirements[4].upper().split(","))

    cur.execute("SELECT * FROM student_details WHERE cgpa >= %s AND dob <= %s AND batch in %s", (temp_company_requirements[2],temp_company_requirements[3],batch_details))
    eligible_students_data = cur.fetchall()
    cur.close()
    print(eligible_students_data)

    return render_template('eligible_students.html',eligible_students=eligible_students_data)


#code for applied students
@app.route('/hr_dashboard/applied_candidates',endpoint="applied_students_endpoint")
@hr_required
def applied_students():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM student_details WHERE applied_companies LIKE %s ",("%" + str(session['company_name'] + "%"),))
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

    return render_template('company_hr_dashboard.html', company_name=session["company_name"],power=new_power)


#set interview Details

@app.route("/hr_dashboard/change_interview_details",methods=['GET', 'POST'],endpoint="edit_interview_details_endpoint")
@hr_required
def edit_interview_details():
    #print("i am here")
    if request.method == 'POST':
        content = request.form['content']  # Get the edited content from the POST request
        interview_date=request.form['interview_date']
        #interview_date = datetime.strptime(interview_date, "%Y-%m-%d")
        #print(content,interview_date,type(interview_date),sep=" ")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE interview_details SET interview_detail = %s , interview_date = %s WHERE company_name = %s", (content, interview_date, session['company_name']))
        mysql.connection.commit()
        cur.close()

        # Define a success message to be sent to the client
        success_message = "Save Success"

        # Use jsonify to send the success message as JSON
        response = jsonify({'message': success_message})

        # You can also set an HTTP status code for success, e.g., 200
        response.status_code = 200

        return response

    # Render the "change_company_details.html" page for both GET and POST requests
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
        content = request.form['content']  # Get the edited content from the POST request

        cur = mysql.connection.cursor()
        cur.execute("UPDATE interview_details SET company_description = %s WHERE company_name = %s", (content, session['company_name']))
        mysql.connection.commit()
        cur.close()

        # Define a success message to be sent to the client
        success_message = "Save Success"

        # Use jsonify to send the success message as JSON
        response = jsonify({'message': success_message})

        # You can also set an HTTP status code for success, e.g., 200
        response.status_code = 200

        return response

    # Render the "change_company_details.html" page for both GET and POST requests
    return render_template("change_company_details.html")
#define the edit interview details function
'''
@app.route('/hr_dashboard/logout',endpoint="interview_details_endpoint")
@hr_required
def logout():
    global hr_logged_in
    session.clear()
    hr_logged_in=False
    return redirect(url_for('login'))

'''

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
        AND CR.max_dob > %s
        AND CR.batch LIKE %s
        AND ID.power = 1
        AND ID.last_date > %s
        """, (session['cgpa'], session['dob'], '%' + session['batch'] + '%', current_date_str))
    companies = cur.fetchall()    
    if len(companies)>0:
        data = companies
        companies = tuple(item for sublist in data for item in sublist)
    cur.execute("SELECT applied_companies FROM student_details WHERE userid = %s",(session['user_id'],))
    see_applied_companies = cur.fetchall()
    if see_applied_companies[0][0]!=None:
        see_applied_companies=see_applied_companies[0]
        see_applied_companies = tuple(map(lambda x: str(x), see_applied_companies[0].split(',')))

    cur.close()
    return render_template("eligible_companies.html", companies=companies,existing_companies=see_applied_companies)


@app.route('/student_dashboard/handle_application', methods=['POST'])
def handle_application():    
    action=request.form.get('action')
    if action=='apply':
        company_name=request.form.get('company_name')
        cur=mysql.connection.cursor()
        cur.execute("SELECT applied_companies FROM student_details where userid = %s",(session['user_id'],))
        companies_applied=cur.fetchall()[0]
        if companies_applied[0] != None:
            companies_applied = tuple(map(lambda x: str(x), companies_applied[0].split(',')))
            companies_applied+=tuple([company_name])
        else:
            companies_applied=tuple([company_name])
        companies_applied_string=",".join(companies_applied)
        cur.execute("UPDATE student_details SET applied_companies = %s  WHERE userid = %s",(companies_applied_string,session['user_id']))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('eligible_companies_endpoint'))

@app.route('/student_dashboard/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))








if __name__ == '__main__':
    app.run(debug=True)
