"""
Simple job description scraper for demonstration purposes
Demonstrates data collection and preprocessing capabilities
"""

import requests
from bs4 import BeautifulSoup
import json
import re

def get_sample_job_descriptions():
    """
    Returns pre-collected sample job descriptions
    This demonstrates data collection capability
    In production, these would be fetched from APIs
    """
    sample_jobs = [
        {
            "title": "Senior Data Analyst",
            "company": "TechCorp",
            "location": "Remote",
            "description": """We are seeking a Senior Data Analyst to join our growing analytics team.

Requirements:
- 5+ years of experience in data analysis
- Expert-level SQL skills (complex queries, optimization, stored procedures)
- Strong Python proficiency (pandas, numpy, scikit-learn, matplotlib)
- Experience with Tableau or Power BI for data visualization
- Bachelor's degree in Statistics, Computer Science, or related field
- Excellent communication skills for presenting to non-technical stakeholders

Responsibilities:
- Analyze large datasets to identify trends, patterns, and business insights
- Create interactive dashboards and reports for executive leadership
- Collaborate with product, engineering, and business teams
- Present data-driven recommendations to C-level executives
- Mentor and train junior analysts on best practices
- Develop and maintain data pipelines and ETL processes

Company Culture:
- Fast-paced, innovative environment focused on data-driven decision making
- Remote-first company with flexible work hours
- Strong emphasis on professional development and learning
- Collaborative team that values diverse perspectives"""
        },
        {
            "title": "Software Engineer - Full Stack",
            "company": "StartupXYZ",
            "location": "San Francisco, CA",
            "description": """Join our engineering team building next-generation SaaS applications.

Requirements:
- 3+ years of professional software development experience
- Strong knowledge of JavaScript/TypeScript and modern frameworks
- Experience with React for frontend and Node.js for backend
- Familiarity with AWS, Docker, and Kubernetes
- CS degree or equivalent practical experience
- Experience with RESTful APIs and microservices architecture

What You'll Do:
- Design and build scalable web applications serving millions of users
- Write clean, maintainable, well-tested code
- Participate in code reviews and technical design discussions
- Work in an agile development environment with 2-week sprints
- Contribute to architectural decisions and technical strategy
- Collaborate with designers and product managers

Benefits:
- Competitive salary ($120K-$180K) plus equity
- Comprehensive health insurance
- Flexible work hours and unlimited PTO
- $2,000 annual learning budget
- Latest MacBook Pro and equipment"""
        },
        {
            "title": "Marketing Manager - Digital",
            "company": "GrowthCo",
            "location": "New York, NY",
            "description": """Looking for a creative Marketing Manager to lead our digital marketing efforts.

Requirements:
- 4+ years in digital marketing with proven track record
- Expert knowledge of SEO, SEM, social media, and content marketing
- Strong analytical skills with experience using Google Analytics, SEMrush
- Excellent written and verbal communication abilities
- Bachelor's degree in Marketing, Business, or related field
- Experience managing marketing budgets of $500K+

Responsibilities:
- Develop and execute comprehensive digital marketing strategies
- Manage marketing budget and track ROI across all channels
- Lead a team of 3-5 marketing specialists
- Analyze campaign performance and optimize for better results
- Collaborate closely with sales team on lead generation
- Create compelling content for various digital channels
- Stay current on marketing trends and best practices

Company Culture:
- Creative, collaborative environment that encourages innovation
- Focus on measurable growth and data-driven decisions
- Regular team building events and company retreats
- Commitment to work-life balance"""
        },
        {
            "title": "Product Manager",
            "company": "InnovateTech",
            "location": "Austin, TX",
            "description": """Seeking an experienced Product Manager to drive product strategy and execution.

Requirements:
- 5+ years of product management experience in tech
- Strong understanding of agile development methodologies
- Experience with user research and data analysis
- Excellent stakeholder management and communication skills
- Technical background or CS degree preferred
- Track record of launching successful products

Responsibilities:
- Define product vision, strategy, and roadmap
- Conduct user research and gather customer feedback
- Write detailed product requirements and user stories
- Work closely with engineering, design, and marketing teams
- Prioritize features based on business value and user needs
- Analyze product metrics and make data-driven decisions
- Present product updates to leadership and stakeholders

What We Offer:
- Competitive compensation with stock options
- Opportunity to shape product direction
- Collaborative and innovative work environment
- Professional development opportunities"""
        },
        {
            "title": "UX/UI Designer",
            "company": "DesignHub",
            "location": "Remote",
            "description": """Join our design team creating beautiful, user-centered digital experiences.

Requirements:
- 3+ years of UX/UI design experience
- Strong portfolio demonstrating design process and thinking
- Proficiency in Figma, Sketch, and Adobe Creative Suite
- Experience with user research, wireframing, and prototyping
- Understanding of HTML/CSS basics
- Bachelor's degree in Design or related field

What You'll Do:
- Design intuitive user interfaces for web and mobile applications
- Conduct user research and usability testing
- Create wireframes, prototypes, and high-fidelity mockups
- Collaborate with product managers and developers
- Maintain and evolve design system
- Present design concepts to stakeholders
- Stay updated on design trends and best practices

Culture:
- Design-led organization that values creativity
- Remote-first with optional office space
- Supportive team environment
- Focus on continuous learning"""
        }
    ]
    
    return sample_jobs


def search_jobs(query="", location=""):
    """
    Search through sample jobs based on query
    Simulates searching external job boards
    """
    all_jobs = get_sample_job_descriptions()
    
    if not query and not location:
        return all_jobs
    
    # Filter jobs based on query
    filtered_jobs = []
    query_lower = query.lower()
    location_lower = location.lower()
    
    for job in all_jobs:
        # Check if query matches title or description
        query_match = (
            query_lower in job['title'].lower() or 
            query_lower in job['description'].lower() or
            not query
        )
        
        # Check if location matches
        location_match = (
            location_lower in job['location'].lower() or
            location_lower == "remote" and "remote" in job['location'].lower() or
            not location
        )
        
        if query_match and location_match:
            filtered_jobs.append(job)
    
    # Return filtered results or all if no matches
    return filtered_jobs if filtered_jobs else all_jobs[:2]


def clean_job_description(raw_text):
    """
    Clean scraped or collected job description data
    
    Cleaning steps:
    1. Remove extra whitespace
    2. Remove special characters
    3. Normalize line breaks
    4. Remove HTML tags if present
    """
    # Remove HTML tags if any
    text = re.sub('<[^<]+?>', '', raw_text)
    
    # Remove extra whitespace
    text = " ".join(raw_text.split())
    
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char.isspace())
    
    # Normalize line breaks (convert to standard format)
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n')
    
    # Remove excessive line breaks
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    
    return text.strip()


def preprocess_job_for_analysis(job_data):
    """
    Preprocess collected job data for AI analysis
    
    Preprocessing steps:
    1. Combine all relevant fields
    2. Clean the text
    3. Validate length
    4. Truncate if necessary
    """
    # Extract and combine relevant fields
    full_description = f"""Job Title: {job_data['title']}
Company: {job_data['company']}
Location: {job_data['location']}

Job Description:
{job_data['description']}
    """.strip()
    
    # Clean the text
    cleaned = clean_job_description(full_description)
    
    # Validate minimum length
    if len(cleaned) < 50:
        raise ValueError("Job description too short after cleaning")
    
    # Truncate if too long (API token limits)
    MAX_LENGTH = 8000
    if len(cleaned) > MAX_LENGTH:
        cleaned = cleaned[:MAX_LENGTH] + "\n\n[Description truncated due to length...]"
    
    return cleaned


def extract_key_info(job_description):
    """
    Extract structured information from job description
    Demonstrates data extraction capabilities
    """
    info = {
        'skills': [],
        'requirements': [],
        'responsibilities': [],
        'benefits': []
    }
    
    # Simple keyword extraction (in production, would use NLP)
    text_lower = job_description.lower()
    
    # Common skills to look for
    common_skills = ['python', 'sql', 'java', 'javascript', 'react', 'aws', 
                    'machine learning', 'data analysis', 'tableau', 'excel']
    
    for skill in common_skills:
        if skill in text_lower:
            info['skills'].append(skill.title())
    
    # Extract experience requirements
    experience_patterns = [r'(\d+)\+?\s*years?', r'(\d+)-(\d+)\s*years?']
    for pattern in experience_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            info['requirements'].append(f"Experience: {matches[0]} years")
            break
    
    return info


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("JOB SCRAPER - DEMONSTRATION")
    print("=" * 60)
    
    # Test 1: Fetch all jobs
    print("\n1. Fetching all sample job descriptions...")
    all_jobs = get_sample_job_descriptions()
    print(f"   ✓ Found {len(all_jobs)} job postings")
    
    # Test 2: Search functionality
    print("\n2. Testing search functionality...")
    results = search_jobs(query="data analyst", location="remote")
    print(f"   ✓ Search for 'data analyst' + 'remote' returned {len(results)} results")
    
    # Test 3: Data cleaning
    print("\n3. Testing data cleaning...")
    sample_job = all_jobs[0]
    cleaned = clean_job_description(sample_job['description'])
    print(f"   ✓ Original length: {len(sample_job['description'])} chars")
    print(f"   ✓ Cleaned length: {len(cleaned)} chars")
    
    # Test 4: Preprocessing
    print("\n4. Testing preprocessing for AI...")
    processed = preprocess_job_for_analysis(sample_job)
    print(f"   ✓ Processed description ready for AI")
    print(f"   ✓ Final length: {len(processed)} chars")
    
    # Test 5: Information extraction
    print("\n5. Testing information extraction...")
    info = extract_key_info(sample_job['description'])
    print(f"   ✓ Extracted {len(info['skills'])} skills: {', '.join(info['skills'][:5])}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    
    # Display one sample
    print(f"\nSample Job Preview:")
    print(f"Title: {sample_job['title']}")
    print(f"Company: {sample_job['company']}")
    print(f"Location: {sample_job['location']}")
    print(f"Description: {sample_job['description'][:200]}...")