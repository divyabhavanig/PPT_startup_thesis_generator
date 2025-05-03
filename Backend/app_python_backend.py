from flask import Flask, request, jsonify
from flask_cors import CORS
from pptx import Presentation
from fpdf import FPDF
import os
import smtplib
from email.message import EmailMessage
from google import genai  # Import the Gemini library
import pandas as pd
from pptx import Presentation

GEMINI_API_KEY = "AIPROXY KEY" #add the key here

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "C:\\Users\\divya\\Desktop\\karo_startup_internship\\Project_3rd\\Backend\\uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_ppt(filepath):
    prs = Presentation(filepath)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text

#generate prompt
def analyze_data_gemini(text):
    """Perform general data analysis using Gemini."""
    list_prompt ={}
    list_prompt["0"] = '''Acting as a startup invester analysing the pitch deck text you need to score the pitch deck text. Condition for scoring from the pitch deck  text is given below:
    1. Problem Statement (Weight: 10%)
         Criteria: Clarity of problem, evidence of customer pain (e.g., stats, quotes),scope of impact.
        Scoring: 0 (no problem stated) to 10 (well-defined with data validation).
    2. Solution/Product (Weight: 15%)
        Criteria: Feasibility, innovation, alignment with problem, clarity of explanation.
        Scoring: 0 (no solution) to 10 (unique, practical, well-articulated).
    3. Market Opportunity (Weight: 20%)
        Criteria: TAM/SAM/SOM defined, realism of estimates, evidence of demand(e.g., trends, surveys).
        Scoring: 0 (no market data) to 10 (specific, credible, data-backed).
    4. Business Model (Weight: 15%)
        Criteria: Revenue streams, scalability, customer acquisition plan, pricing clarity.
        Scoring: 0 (no model) to 10 (detailed, sustainable, logical).
    5. Competitive Landscape (Weight: 10%)
        Criteria: Identification of competitors, strength of UVP, defensibility of position.
        Scoring: 0 (no mention) to 10 (detailed analysis with strong differentiation).
    6. Team (Weight: 15%)
        Criteria: Relevant experience, completeness of roles, evidence of execution ability.
        Scoring: 0 (no team info) to 10 (experienced, balanced, proven track record).
    7. Traction/Milestones (Weight: 10%)
        Criteria: Metrics (e.g., revenue, users), achieved milestones, alignment with funding ask.
        Scoring: 0 (no traction) to 10 (quantifiable, impressive progress).
    8. Financial Projections (Weight: 10%)
        Criteria: 3-5 year forecasts, transparency of assumptions, realism of growth rates.
        Scoring: 0 (no financials) to 10 (detailed, reasonable, supported).
    9. Clarity and Presentation (Weight: 5%)
        Criteria: Logical flow, visual design, grammar, conciseness (max 20 slides).
        Scoring: 0 (incoherent, sloppy) to 10 (polished, professional, concise).
    '''
    print(list_prompt["0"])
    
    list_prompt["1"] = "pitch deck content that you have to consider:" + text
    
    print(list_prompt["1"])
    list_prompt["2"] =''' You are an AI investment analyst. Based on the pitch deck content provided, generate a detailed investment report using the following structure and scoring methodology:

1. Summary Section:
    1.1 Investment Recommendation: Choose one — "Strong Buy", "Hold", or "Pass".
    1.2 Overall Score: Integer between 0 and 100. Use weighted average of 9 category scores.
    1.3 Processing Date: Format "DD-MM-YYYY HH:MM:SS UTC".

2. Category-wise Analysis:
    For each of the following 9 categories, include:
    - Score: Integer between 0 and 10.
    - Weight: Fixed percentage per category.
    - Feedback: 50-150 word paragraph summarizing strengths, weaknesses, and insights.

    Categories:
    1. Problem Statement (10%)
    2. Solution/Product (15%)
    3. Market Opportunity (15%)
    4. Business Model (10%)
    5. Competitive Landscape (10%)
    6. Team (10%)
    7. Traction/Milestones (10%)
    8. Financial Projections (10%)
    9. Clarity and Presentation (10%)

3. Strengths and Weaknesses:
    - Strengths: Bullet points (3-5)
    - Weaknesses: Bullet points (3-5)

4. Recommendations:
    - A 100-200 word actionable paragraph on next steps and suggestions for improvement.

5. Confidence Score:
    - Integer between 0 and 100 based on completeness and coherence of the pitch deck.

Input Pitch Deck Content:
---
[Paste the pitch deck content here — or if it’s a slide upload, indicate slide text or summary of each point.]
---

Scoring should be rational, based on the clarity, completeness, and potential impact of each category.

    '''

    print(list_prompt["2"])
    return list_prompt["0"]+list_prompt["1"]+list_prompt["2"]

def generate_gemini_response(prompt):
    """Sends a prompt to the Gemini API and returns the response."""
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    """
    api_key = GEMINI_API_KEY
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash"  # Use a model that is suitable for text generation

    contents = prompt
    response_text = ""
    try:
        response = client.models.generate_content(
            model=model,
            contents=contents
        )
        response_text = response.text
        print(response_text)
        # response = client.models.generate_content(
        #     model=model,
        #     contents=contents["1"]
        # )
        # response_text = response.text
        # print(response_text)
        # response = client.models.generate_content(
        #     model=model,
        #     contents=contents["2"]
        # )
        # response_text = response.text
        # print(response_text)
    except Exception as e:
        print(f"Error generating content with Gemini: {e}")
        response_text = f"Error: {e}"

    return response_text


def generate_report(gemini_analysis):
    """Create investment_thesis.txt with analysis results."""
    with open(UPLOAD_FOLDER+"investment_thesis.txt", "w") as f:
        f.write(f"# Investment Thesis Report\n\n")
        f.write(gemini_analysis + "\n\n")

def create_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Use a Unicode TTF font
    font_path = os.path.join(os.getcwd(), 'DejaVuSans.ttf')  # place TTF file in same dir
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    lines = text.split("\n")
    for line in lines:
        pdf.multi_cell(0, 10, txt=line)

    filepath = os.path.join('uploads', filename)
    pdf.output(filepath)
    return filepath

def send_email_with_attachment(receiver_email, pdf_path):
    sender_email = # "your-email@example.com"
    sender_password = #"your-app-password"

    msg = EmailMessage()
    msg['Subject'] = 'Your Extracted PDF'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("Here is your extracted PDF from the uploaded PPT.")

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    email = request.form['email']

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = extract_text_from_ppt(filepath)
    gemini_prompt = analyze_data_gemini(text)
    print(gemini_prompt)
    gemini_analysis = generate_gemini_response(gemini_prompt)
    print(gemini_analysis)
    #generate_report(gemini_analysis)
    
    pdf_path = create_pdf(gemini_analysis, file.filename.replace('.pptx', '.pdf'))

    send_email_with_attachment(email, pdf_path)

    return jsonify({'message': 'Email sent successfully!', 'text': text})

if __name__ == '__main__':
    app.run(debug=True)
