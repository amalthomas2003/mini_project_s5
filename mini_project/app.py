from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import details

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'amalahsanrohitrohan'  # Replace with a secure secret key

###handle internal error due to missing column values
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html'), 500



# # Handle a "304 Not Modified" error when wrong input data is provided
# @app.errorhandler(304)
# def not_modified_error(error):
#     return render_template('not_modified_error.html'), 304


#initialize variables

element_found=False 




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
                    print(role,logintable)
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

@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' in session and session['role'] == 'student':
        return "Welcome to the student dashboard!"
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
        return render_template('company_hr_dashboard.html', company_name=session["company_name"])
    else:
        return redirect(url_for('login'))
    

@app.route('/login_failed')
def invalid_login_credentials():
    return "ohhhh no"

#############################################################################################################################login ends here############################################


#########################################################################################company hr starts here########################################################
# HR Dashboard - Set Requirements
@app.route('/hr_dashboard/set_requirements', methods=['GET', 'POST'])
def set_requirements():
    if request.method == 'POST':


        min_cgpa = request.form['min_cgpa']
        max_dob = request.form['max_dob']

        # Establish a database connection using the mysql object
        cur = mysql.connection.cursor()

        # Update company requirements in the database
        cur.execute("UPDATE company_requirements SET min_cgpa = %s, max_dob = %s WHERE company_name = %s", (min_cgpa, max_dob,session["company_name"]))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('company_hr_dashboard'))

    return render_template('set_requirements.html')


if __name__ == '__main__':
    app.run(debug=True)
