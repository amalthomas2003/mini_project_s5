from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Sample data for the pie chart
    labels = ['Label 1',]
    data = [30,]

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Convert the image to base64 for HTML embedding
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    # Close the plot to free up resources
    plt.close()

    # Render the HTML template with the base64-encoded image data
    return render_template('test.html', pie_chart_data=img_base64)

if __name__ == '__main__':
    app.run(debug=True)
