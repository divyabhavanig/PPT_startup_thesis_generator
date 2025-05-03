import os
import sys
from google import genai  # Import the Gemini library
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pptx import Presentation

GEMINI_API_KEY = "AIPROXY_KEY"

# extracting the text from ppt
def extract_text(ppt_path):
    prs = Presentation(ppt_path)
    all_text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape,"text"):
                all_text += shape.text +"\n"
    return all_text


#generate prompt
def analyze_data_gemini(ppt_path):
    """Perform general data analysis using Gemini."""
    prompt = "data from ppt:" + extract_text(ppt_path) 
    print(generate_gemini_response(prompt))
    prompt = '''Condition for scoring from the ppt:
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
    print(generate_gemini_response(prompt))
    prompt =''' create content from he previously discussed scoring method and the ppt.
    1. Summary Section:
        1.1 Investment Recommendation: One of three options: "Strong Buy," "Hold,", "Pass."
        1.2 Overall Score: Integer between 0 and 100, calculated as a weighted average of category scores.
        1.3 Processing Date: Timestamp in format "DD-MM-YYYY HH:MM:SS UTC" (e.g.,"07-04-2025 14:30:00 UTC").
    2. Category-wise Analysis:
        2.1 Nine sections, one per evaluation category (listed below).
        2.2 Each section includes:
            Score: Integer between 0 and 10.
            Weight: Fixed percentage (sum of weights = 100%).
        2.3 Qualitative Feedback: 50-150 words summarizing strengths,weaknesses, and observations.
    3. Strengths and Weaknesses:
        Strengths: Bullet list of 3-5 positive findings (e.g., "Clear problem validation with data").
        Weaknesses: Bullet list of 3-5 risks or gaps (e.g., "No financial assumptions provided").
    4. Recommendations:
        100-200 words of actionable advice (e.g., "Conduct due diligence on team execution capacity").
    5. Confidence Score:
        Integer between 0 and 100, reflecting the AI’s certainty in the analysis based on data completeness and coherence.
    '''
    return generate_gemini_response(prompt)


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
    except Exception as e:
        print(f"Error generating content with Gemini: {e}")
        response_text = f"Error: {e}"

    return response_text


def generate_report(gemini_analysis):
    """Create investment_thesis.txt with analysis results."""
    with open("investment_thesis.txt", "w") as f:
        f.write(f"# Investment Thesis Report\n\n")
        f.write(gemini_analysis + "\n\n")
        
def main():
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <d>")
        sys.exit(1)

    filename = sys.argv[1]
    ppt_text = extract_text(filename)
    gemini_analysis = analyze_data_gemini(ppt_text)
    generate_report(gemini_analysis)
    print("Analysis complete. Check investment_thesis.txt")

if __name__ == "__main__":
    main()
