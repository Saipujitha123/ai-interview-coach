import os
from dotenv import load_dotenv
import PyPDF2
import re
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt(prompt, system_message="You are a helpful AI interview coach.", temperature=0.7):
    """Call OpenAI GPT API using the new client format"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_job_description(job_desc):
    """Analyze job description and extract key information"""
    prompt = f"""Analyze this job description and provide:

1. KEY SKILLS REQUIRED: (list 5-7 main skills)
2. EXPERIENCE LEVEL: (entry/mid/senior)
3. COMPANY CULTURE: (what the culture seems like)
4. MAIN RESPONSIBILITIES: (3-5 key duties)
5. POTENTIAL CHALLENGES: (concerns or red flags)

Job Description:
{job_desc}

Be specific and actionable."""
    
    return call_gpt(prompt)

def generate_interview_questions(job_desc, num_questions=10):
    """Generate custom interview questions based on job description"""
    prompt = f"""Based on this job description, generate {num_questions} interview questions.

Include this mix:
- 40% Technical/Skills questions (test specific abilities)
- 30% Behavioral questions (STAR method situations)
- 20% Company/Culture fit questions
- 10% Problem-solving scenarios

Job Description:
{job_desc}

Format: Number each question clearly (1., 2., 3., etc.)"""
    
    return call_gpt(prompt)

def evaluate_answer(question, user_answer):
    """Evaluate user's interview answer"""
    prompt = f"""You are an expert interviewer. Evaluate this answer:

QUESTION: {question}

CANDIDATE'S ANSWER: {user_answer}

Provide:
1. SCORE: (1-10 where 10 is excellent)
2. STRENGTHS: (what was good)
3. WEAKNESSES: (what could improve)
4. IMPROVED VERSION: (rewrite the answer better)

Be specific and constructive."""
    
    return call_gpt(prompt)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF resume"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_resume(resume_text, job_desc):
    """Analyze resume against job description"""
    prompt = f"""Compare this resume with the job requirements:

JOB DESCRIPTION:
{job_desc}

RESUME:
{resume_text}

Provide:
1. MATCH SCORE: (0-100%)
2. MATCHING SKILLS: (skills candidate has that job needs)
3. MISSING SKILLS: (what candidate lacks)
4. RESUME STRENGTHS: (what stands out positively)
5. IMPROVEMENT SUGGESTIONS: (how to improve resume for this job)

Be specific and actionable."""
    
    return call_gpt(prompt)

def generate_cover_letter(resume_text, job_desc, company_name):
    """Generate personalized cover letter"""
    prompt = f"""Write a professional cover letter for this job application:

COMPANY: {company_name}
JOB DESCRIPTION: {job_desc}
CANDIDATE BACKGROUND: {resume_text}

Write a compelling 3-paragraph cover letter that:
- Shows enthusiasm for the role
- Highlights relevant experience
- Explains why they're a great fit
- Uses professional tone

Keep it under 300 words."""
    
    return call_gpt(prompt, temperature=0.8)

def generate_star_examples(job_desc):
    """Generate STAR method example answers"""
    prompt = f"""Based on this job description, create 3 STAR method answer examples for common behavioral questions.

Job Description:
{job_desc}

For each example, provide:
- The Question
- Situation: (context)
- Task: (what needed to be done)
- Action: (what you did)
- Result: (outcome with metrics if possible)

Make examples relevant to the job requirements."""
    
    return call_gpt(prompt)

def score_answer_quality(answer):
    """Quick scoring of answer quality"""
    score = 5  # Base score
    
    # Check length
    word_count = len(answer.split())
    if word_count < 20:
        score -= 2
    elif word_count > 50:
        score += 1
    
    # Check for specific examples
    if any(word in answer.lower() for word in ['example', 'instance', 'specifically', 'when i']):
        score += 1
    
    # Check for metrics/numbers
    if re.search(r'\d+', answer):
        score += 1
    
    # Check for structure
    if any(word in answer.lower() for word in ['first', 'then', 'finally', 'resulted']):
        score += 1
    
    return min(max(score, 1), 10)  # Keep between 1-10