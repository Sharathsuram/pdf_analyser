from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from pdf_analyzer import analyze_pdf_file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Call the PDF analysis function from pdf_analyzer.py
        report_filename = analyze_pdf_file(filepath, app.config['REPORT_FOLDER'])
        
        report_url = f'/reports/{report_filename}'
        return jsonify({'success': True, 'report_url': report_url})
    
    return jsonify({'success': False, 'error': 'Invalid file type'})

@app.route('/reports/<filename>')
def serve_report(filename):
    return send_from_directory(app.config['REPORT_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    app.run(debug=True)