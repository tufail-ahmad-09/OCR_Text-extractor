from flask import Flask, render_template, request, redirect, url_for
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Check if uploaded file is an image
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and OCR
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    language = request.form['language']  # Get language from the form
    
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Open image and extract text with selected language
        image = Image.open(filepath)
        extracted_text = pytesseract.image_to_string(image, lang=language)
        
        # Save the extracted text to a .txt file
        text_filename = f"{filename.rsplit('.', 1)[0]}.txt"
        text_filepath = os.path.join(app.config['RESULT_FOLDER'], text_filename)
        with open(text_filepath, 'w') as text_file:
            text_file.write(extracted_text)
        
        return redirect(url_for('download_file', filename=text_filename))
    
    return redirect(request.url)

# Route to download the extracted text file
@app.route('/download/<filename>')
def download_file(filename):
    return f"Text extraction complete! File saved as: {filename}. Check the results folder."

if __name__ == "__main__":
    app.run(debug=True)
