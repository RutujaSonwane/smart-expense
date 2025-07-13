from flask import Flask, render_template, request
from utils.analyzer import analyze_expenses
import os
import pandas as pd
from datetime import datetime
import time
import pdfkit
import numpy as np
import json
import csv

app = Flask(__name__)
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ Helper to fix int64/float64 serialization
def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(x) for x in obj]
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    return obj

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file:
                unique_filename = f"upload_{int(time.time())}.csv"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                uploaded_file.save(file_path)
                result = analyze_expenses(file_path)
        elif request.form.get('manual') == 'true':
            try:
                data = {
                    'date': request.form.getlist('date'),
                    'amount': [float(x) for x in request.form.getlist('amount')],
                    'category': request.form.getlist('category'),
                    'vendor': request.form.getlist('vendor')
                }
                df = pd.DataFrame(data)
                temp_file = os.path.join(app.config['UPLOAD_FOLDER'], f'manual_{datetime.now().timestamp()}.csv')
                df.to_csv(temp_file, index=False)
                result = analyze_expenses(temp_file)
            except Exception as e:
                result = {'error': 'Invalid manual input: ' + str(e)}

    safe_result = convert_numpy(result) if result else None
    return render_template('index.html', result=safe_result)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        with open('data/messages.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, email, message, datetime.now().isoformat()])

        return render_template('contact.html', message_sent=True)
    return render_template('contact.html')

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    import json

    result = request.form['result']
    parsed_result = convert_numpy(json.loads(result))

    html = render_template('pdf_template.html', result=parsed_result)

    config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')  # Adjust path
    pdf = pdfkit.from_string(html, False, configuration=config)

    response = app.response_class(pdf, mimetype='application/pdf')
    response.headers['Content-Disposition'] = 'attachment; filename=expense_report.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
