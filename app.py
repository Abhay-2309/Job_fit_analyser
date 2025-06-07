import os
import json
import fitz  # PyMuPDF
import docx  # python-docx
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables from .env file
load_dotenv()

# Configure the Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    # Use the correct, fast 'Flash' model.
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("Successfully configured Gemini with model: gemini-1.5-flash-latest")
except Exception as e:
    print(f"!!! FATAL ERROR: Could not configure Gemini API: {e}")
    exit()

# --- Helper functions for text extraction ---
# The indentation has been corrected here.

def extract_text_from_pdf(file_stream):
    """Extracts text from a PDF file stream."""
    try:
        doc = fitz.open(stream=file_stream.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def extract_text_from_docx(file_stream):
    """Extracts text from a DOCX file stream."""
    try:
        doc = docx.Document(file_stream)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return None

def extract_text(file):
    """Extracts text from an uploaded file (PDF or DOCX)."""
    filename = secure_filename(file.filename)
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(file)
    else:
        return None  # Unsupported file type

# --- The Gemini prompt (No changes needed here) ---
def get_gemini_prompt(resume_text, jd_text):
    """Formats the resume and job description into the prompt."""
    return f"""
    **System Role:** You are an expert HR recruitment specialist and career coach with deep expertise in tech and business roles. Your task is to analyze a candidate's resume against a job description and provide a detailed, objective, and constructive fit analysis.

    **Instructions:**
    Analyze the provided Resume and Job Description. Based on your analysis, provide a response in a strict JSON format. Do not include any text outside of the JSON object. The JSON should be clean and ready for parsing.

    The JSON object must have the following keys:
    - "fit_score": A numerical score from 0 to 100 representing how well the candidate's experience and skills match the job requirements.
    - "summary": A brief, one-paragraph summary of the candidate's overall fit for the role.
    - "strengths": A JSON array of strings. Each string should be a key strength of the candidate that directly aligns with a requirement in the Job Description.
    - "weaknesses_and_gaps": A JSON array of strings. Each string should identify a potential weakness or a missing skill/experience required by the Job Description.
    - "suggestions_for_improvement": A JSON array of strings. Each string should be an actionable suggestion for the candidate to improve their resume or highlight their experience better for this specific role.

    **Input Data:**

    **[JOB DESCRIPTION]**
    ---
    {jd_text}
    ---

    **[RESUME]**
    ---
    {resume_text}
    ---
    """

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # This is the upgraded 'analyze' function with logging
    print("\n--- [START] NEW REQUEST RECEIVED ---")

    try:
        # 1. Get Resume Text
        print("[1/5] Processing resume file...")
        if 'resume_file' not in request.files or request.files['resume_file'].filename == '':
            return jsonify({"error": "Resume file is required."}), 400
        resume_file = request.files['resume_file']
        resume_text = extract_text(resume_file)
        if resume_text is None:
            return jsonify({"error": "Unsupported resume file type. Please use PDF or DOCX."}), 400

        # 2. Get Job Description Text
        print("[2/5] Processing job description...")
        jd_text = None
        if 'jd_file' in request.files and request.files['jd_file'].filename != '':
            jd_file = request.files['jd_file']
            jd_text = extract_text(jd_file)
            if jd_text is None:
                return jsonify({"error": "Unsupported job description file type. Please use PDF or DOCX."}), 400
        elif 'jd_text' in request.form and request.form['jd_text'].strip() != '':
            jd_text = request.form['jd_text']

        if jd_text is None:
            return jsonify({"error": "Job description is required. Please upload a file or paste the text."}), 400

        print("[3/5] Sending prompt to Gemini API. This may take a moment...")
        prompt = get_gemini_prompt(resume_text, jd_text)

        # 3. Call Gemini API
        response = model.generate_content(prompt)

        print("[4/5] Received response from Gemini API. Parsing JSON...")
        # Clean the response to ensure it's valid JSON
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()

        analysis_result = json.loads(response_text)

        print("[5/5] Success! Sending analysis to frontend.")
        print("--- [END] REQUEST PROCESSED SUCCESSFULLY ---")
        return jsonify(analysis_result)

    except json.JSONDecodeError as e:
        print(f"!!! ERROR: Failed to parse JSON from Gemini response. Error: {e}")
        # Make sure to define response_text before using it in the error message
        raw_response = "N/A"
        if 'response' in locals() and hasattr(response, 'text'):
            raw_response = response.text
        print(f"--- Raw Gemini Response was: ---\n{raw_response}\n-------------------------------")
        return jsonify({"error": "The AI returned an invalid response. Please try rephrasing your job description."}), 500
    except Exception as e:
        print(f"!!! AN UNEXPECTED ERROR OCCURRED: {e}")
        print("--- [END] REQUEST FAILED ---")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)