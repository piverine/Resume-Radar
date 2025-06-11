import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown2
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_response(text):
    """Generate AI response using Gemini API with structured feedback."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Enhanced prompt to get structured feedback
    prompt = """
    Analyze this resume and provide detailed feedback in a VALID JSON format with the following structure:
    
    ```json
    {
        "overall_score": number (0-100),
        "sections": [
            {
                "name": "string (e.g., 'Experience', 'Skills', 'Education')",
                "score": number (0-100),
                "strengths": ["string"],
                "improvements": ["string"],
                "ats_compatibility": boolean,
                "keywords": {
                    "present": ["string"],
                    "missing": ["string"]
                }
            }
        ],
        "summary": "string (overall feedback)",
        "ats_compatibility": {
            "score": number (0-100),
            "issues": ["string"],
            "suggestions": ["string"]
        }
    }
    ```
    
    IMPORTANT RULES:
    1. Your response MUST be valid JSON that can be parsed with json.loads()
    2. Do NOT include any markdown formatting, code blocks, or any text outside the JSON object
    3. Make sure all strings are properly escaped
    4. Ensure all brackets and quotes are properly closed
    5. Do not include any comments in the JSON
    
    Be brutally honest and specific in your feedback. Focus on actionable improvements.
    Here's the resume text:
    """ + text
    
    try:
        response = model.generate_content(prompt)
        print("Raw response:", response)  # Debug log
        
        # Check if response has parts (Gemini API response format)
        if hasattr(response, 'parts') and response.parts:
            # Extract text from the first part
            text = response.parts[0].text.strip()
            print("Extracted text:", text[:500] + "..." if len(text) > 500 else text)  # Debug log
            
            # Handle JSON wrapped in markdown code blocks
            if '```json' in text:
                # Extract JSON from between ```json and ```
                json_str = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                # Handle case where language isn't specified
                json_str = text.split('```')[1].strip()
            else:
                json_str = text
            
            # Try to parse the JSON
            try:
                feedback = json.loads(json_str)
                if isinstance(feedback, dict):
                    return feedback
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Problematic JSON string: {json_str[:500]}...")
                pass
            
            # If not valid JSON or not a dict, return as summary
            return {
                "summary": text,
                "overall_score": 0,
                "sections": [],
                "ats_compatibility": {
                    "score": 0,
                    "issues": ["Could not parse structured feedback"],
                    "suggestions": ["The AI response was not in the expected format"]
                }
            }
        
        # Fallback if no parts found
        return {
            "summary": "No valid response from AI service",
            "overall_score": 0,
            "sections": [],
            "ats_compatibility": {
                "score": 0,
                "issues": ["Empty response from AI service"],
                "suggestions": ["Please try again later"]
            }
        }
        
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return {
            "summary": f"Error generating feedback: {str(e)}",
            "overall_score": 0,
            "sections": [],
            "ats_compatibility": {
                "score": 0,
                "issues": ["Error processing your request"],
                "suggestions": ["Please try again later"]
            }
        }