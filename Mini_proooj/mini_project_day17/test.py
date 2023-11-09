from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/handle_button', methods=['POST'])
def handle_button():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'see_details':
            # Handle the "See Company Details" action
            return "View Company Details"
        elif action == 'apply':
            # Handle the "Apply" action
            return "Apply to Company"
    
    # Handle other cases or redirect if needed
    return "Invalid Action"

if __name__ == '__main__':
    app.run(debug=True)
