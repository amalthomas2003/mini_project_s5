
import re

date_pattern = r'\d{4}-\d{2}-\d{2}'  # Regular expression pattern for 'yyyy-mm-dd' format

# Check if a date string matches the 'yyyy-mm-dd' format
def is_valid_date(date_string):
    return bool(re.match(date_pattern, date_string))

def student_userid_ends_with():
    return 'rajagiri.edu.in' #update to change student_userid ending string


def admin_userid_ends_with():
    return 'rajagiri.admin.in' #update to change admin_userid ending string


def company_hr_userid_ends_with():
    company_list=['tcs','wipro','infosys']  #update the name of recruting companies, automatically reflected in company hr userid
    updated_company_list=['@'+x+'.in' for x in company_list]
    return updated_company_list

def default_cgpa():
    return 7                #if the company doesn't specify a min_cgpa while updating requiremtns


def default_dob():
    return "2003-01-01"         #if the company doesn't specify a max_dob while updating requiremtns
