# Resume Radar 📄✨

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

Resume Radar is an AI-powered web application that provides detailed, actionable feedback on your resume. Get instant analysis of your resume's strengths, weaknesses, and ATS (Applicant Tracking System) compatibility to help you land more interviews.

## ✨ Features

- **AI-Powered Analysis**: Get detailed feedback on your resume using Google's Gemini AI
- **Section-Wise Feedback**: Understand strengths and areas for improvement in each section of your resume
- **ATS Compatibility Check**: See how well your resume performs with Applicant Tracking Systems
- **Keyword Analysis**: Identify missing and present keywords for your target roles
- **Interactive UI**: Clean, modern interface with collapsible sections for easy navigation
- **Export Options**: Copy feedback to clipboard or print it for offline review

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-radar.git
   cd resume-radar
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   Visit `http://localhost:5000` in your web browser

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **AI**: Google Gemini API
- **PDF Processing**: PyPDF2
- **Templating**: Jinja2


## 📝 How It Works

1. **Upload Your Resume**: Simply drag and drop your PDF resume or click to browse
2. **AI Analysis**: Our system extracts text from your resume and sends it to Google's Gemini AI
3. **Get Feedback**: Receive detailed, structured feedback including:
   - Overall score
   - Section-wise analysis (Experience, Education, Skills, etc.)
   - ATS compatibility score
   - Keyword analysis
   - Actionable improvement suggestions

## 🌟 Features in Detail

### Comprehensive Feedback
Get detailed analysis of each section of your resume, including strengths and specific areas for improvement.

### ATS Optimization
Understand how well your resume will perform with Applicant Tracking Systems used by most companies.

### Keyword Analysis
See which important keywords are present in your resume and which ones you might be missing.

### User-Friendly Interface
Clean, responsive design that works on both desktop and mobile devices.

