# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import uuid
from werkzeug.utils import secure_filename
from utils.pdf_parser import extract_text_from_pdf
from utils.gemini_api import get_response
import google.generativeai as genai
import markdown2

load_dotenv()

results={}

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # For session/flash messages
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_resume():
    """Handle resume upload and processing"""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    fl = request.files['file']
    if not fl or fl.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if not fl.filename.endswith('.pdf'):
        flash('Only PDF files are allowed!')
        return redirect(url_for('index'))

    # Secure the filename and save the file
    filename = secure_filename(fl.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    fl.save(file_path)

    # Extract text from the PDF
    text = extract_text_from_pdf(file_path)

    # Get feedback from Gemini API
    try:
        feedback = get_response(text)
        if not isinstance(feedback, dict):
            flash('Error: Invalid response from AI service')
            return redirect(url_for('index'))
    except Exception as e:
        print(f"Error getting response: {str(e)}")
        flash('Error generating feedback. Please try again.')
        return redirect(url_for('index'))

    # Generate a unique result ID
    result_id = uuid.uuid4().hex

    # Store results (in-memory dictionary for now)
    results[result_id] = feedback

    # Redirect to the results page
    return redirect(url_for('show_results', result_id=result_id))


@app.route('/results/<result_id>')
def show_results(result_id):
    """Display the feedback results"""
    # Retrieve stored results
    feedback = results.get(result_id)
    if not feedback:
        return redirect(url_for('index'))
    
    # Debug: Print the feedback to console to verify structure
    print("Feedback structure:", type(feedback))
    if isinstance(feedback, dict):
        print("Feedback keys:", feedback.keys())
    
    # Render results template with feedback
    return render_template('results.html', feedback=feedback)

# Error handlers
@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File too large. Maximum size is 16MB.')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)