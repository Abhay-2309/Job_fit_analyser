# Gemini Job Fit Analyzer

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.x-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A powerful tool that leverages Google's Gemini family of LLMs to provide an in-depth analysis of a candidate's resume against a specific job description. It generates a quantitative fit score, identifies key strengths and weaknesses, and offers actionable suggestions for improvement.

## Live Demo Screenshot

*(Replace this image with a screenshot of your running application)*
![Job Fit Analyzer Screenshot](screenshot.png)

## Features

-   **📄 Smart Document Parsing:** Upload resumes and job descriptions as PDF or DOCX files.
-   **✍️ Flexible Input:** Provides the option to paste job description text directly.
-   **🤖 AI-Powered Analysis:** Uses the Google Gemini API (configurable for Pro or Flash models) for deep contextual comparison.
-   **💯 Quantitative Scoring:** Generates a "Fit Score" from 0 to 100.
-   **✅ Strengths Identification:** Pinpoints the candidate's skills and experiences that directly match the job requirements.
-   **⚠️ Gap Analysis:** Highlights missing skills or experience required for the role.
-   **💡 Actionable Suggestions:** Offers concrete advice on how the candidate can improve their resume for this specific application.
-   **✨ Modern UI:** A clean, responsive, and user-friendly web interface built with Flask.

## Tech Stack

-   **Backend:** Python, Flask
-   **Frontend:** HTML, CSS, JavaScript
-   **LLM:** Google Gemini API (`gemini-1.5-flash-latest`)
-   **File Parsing:** PyMuPDF, python-docx

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

-   Python 3.9 or higher
-   A Google Gemini API Key

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/job-fit-analyzer.git
cd job-fit-analyzer
```

### 3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.
```bash
python -m venv venv
```
- Activate the environment:
```bash
venv\Scripts\activate
```
- On macOS & Linus:
```bash
source venv/bin/activate
```
- Install the requirements:
```bash
pip install -r requirements.txt
```

### 5. Configure Your API Key
1. The application loads the Gemini API key from an environment variable for security.
2. The application loads the Gemini API key from an environment variable for security.
```bash
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```
3. You can get your API key from Google AI Studio. 

## Usage
Once the setup is complete, you can run the application.
1. Make sure your virtual environment is activated.
2. Run the Flask application from the root directory:
```bash
python app.py
```
3. Open your web browser and navigate to:
```bash
http://127.0.0.1:5000
```
4. Upload a resume, provide a job description (via upload or text), and click "Analyze Fit"!

## How It Works
The application follows a simple but powerful workflow:

1. **Frontend**: The user uploads a resume and job description via the web interface.
2. **Flask Backend**: The server receives the files/text.
3. **Text Extraction**: PyMuPDF and python-docx parse the uploaded files to extract raw text.
4. **Prompt Engineering**: The extracted text is formatted into a detailed prompt for the LLM.
5. **Gemini API Call**: The prompt is sent to the Gemini API.
6. **JSON Response**: Gemini returns a structured JSON object containing the full analysis.
7. **Display Results**: The backend sends the parsed JSON to the frontend, where it is displayed to the user in a clean format.
<details>
<summary><strong>Click to see the Core System Prompt</strong></summary>
```bash
**System Role:** You are an expert HR recruitment specialist...

**Instructions:**
Analyze the provided Resume and Job Description. Based on your analysis, provide a response in a strict JSON format...

The JSON object must have the following keys:
- "fit_score"
- "summary"
- "strengths"
- "weaknesses_and_gaps"
- "suggestions_for_improvement"

**Input Data:**
...
</details>

## License
Distributed under the MIT License. See LICENSE for more information.