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
