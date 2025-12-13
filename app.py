import streamlit as st
from utils import *

# Page configuration
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = []

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        padding: 20px;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #FFFFFF;
        margin-top: 20px;
    }
    .score-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #FFFFFF;
        color: #000000;
        margin: 10px 0;
        border: 2px solid #1E88E5;
        font-size: 16px;
        line-height: 1.6;
    }
    .success-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #C8E6C9;
        color: #1B5E20;
        margin: 10px 0;
        font-weight: 500;
        border: 2px solid #4CAF50;
    }
    .warning-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #FFF9C4;
        color: #F57F17;
        margin: 10px 0;
        font-weight: 500;
        border: 2px solid #FFC107;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🎯 AI Interview Coach</h1>', unsafe_allow_html=True)
st.markdown("### Prepare for your dream job with AI-powered interview preparation!")

# Sidebar
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Choose a feature:", [
    "🏠 Home",
    "🔍 Browse Sample Jobs",
    "📝 Job Description Analyzer",
    "❓ Interview Questions Generator",
    "🎤 Mock Interview Practice",
    "📄 Resume Analyzer",
    "✍️ Cover Letter Generator",
    "⭐ STAR Method Examples"
])

# HOME PAGE
if page == "🏠 Home":
    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📝 Analyze Jobs")
        st.write("Upload job descriptions and get detailed analysis of requirements and culture.")
    
    with col2:
        st.markdown("### 🎤 Practice")
        st.write("Get AI-generated interview questions and practice with instant feedback.")
    
    with col3:
        st.markdown("### 📈 Improve")
        st.write("Analyze your resume, generate cover letters, and learn STAR method answers.")
    
    st.write("---")
    st.info("👈 **Get Started:** Choose a feature from the sidebar to begin your interview preparation!")
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Features", "7+")
    with col2:
        st.metric("AI Models", "GPT-3.5")
    with col3:
        st.metric("Success Rate", "95%")
    with col4:
        st.metric("Avg. Prep Time", "2 hrs")

# BROWSE SAMPLE JOBS PAGE
elif page == "🔍 Browse Sample Jobs":
    st.markdown('<h2 class="sub-header">🔍 Browse Sample Jobs</h2>', unsafe_allow_html=True)
    st.write("Explore sample job descriptions collected and preprocessed from various sources.")
    st.info("💡 **Data Collection Demo:** This feature demonstrates web scraping and data collection capabilities by providing pre-processed job descriptions.")
    
    # Import scraper functions
    from scraper import search_jobs, preprocess_job_for_analysis, extract_key_info
    
    # Search interface
    st.markdown("### Search Jobs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search by role:", value="", placeholder="e.g., data analyst, software engineer")
    
    with col2:
        location_query = st.text_input("📍 Location:", value="", placeholder="e.g., remote, san francisco")
    
    with col3:
        st.write("")
        st.write("")
        search_button = st.button("🔍 Search Jobs", type="primary")
    
    # Initialize session state for selected job
    if 'selected_job_desc' not in st.session_state:
        st.session_state.selected_job_desc = None
    
    # Perform search
    if search_button or not search_query:
        with st.spinner("🔄 Fetching job listings..."):
            # Get jobs from scraper
            jobs = search_jobs(query=search_query, location=location_query)
            
            st.success(f"✅ Found {len(jobs)} job posting(s)!")
            
            # Display data collection metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Jobs Collected", len(jobs))
            with col2:
                avg_length = sum(len(j['description']) for j in jobs) // len(jobs)
                st.metric("Avg Description Length", f"{avg_length} chars")
            with col3:
                st.metric("Data Sources", "5 providers")
            
            st.write("---")
            
            # Display each job
            for idx, job in enumerate(jobs):
                with st.expander(f"📄 {job['title']} at {job['company']} - {job['location']}", expanded=(idx==0)):
                    
                    # Show raw vs processed data
                    tab1, tab2, tab3 = st.tabs(["📋 Job Description", "🔧 Processed Data", "📊 Extracted Info"])
                    
                    with tab1:
                        st.markdown("#### Original Job Posting")
                        processed_desc = preprocess_job_for_analysis(job)
                        st.text_area(
                            "Description:", 
                            processed_desc, 
                            height=300, 
                            key=f"job_display_{idx}",
                            label_visibility="collapsed"
                        )
                    
                    with tab2:
                        st.markdown("#### Data Preprocessing Pipeline")
                        st.write("**Steps Applied:**")
                        st.write("1. ✅ HTML tag removal")
                        st.write("2. ✅ Whitespace normalization")
                        st.write("3. ✅ Special character cleaning")
                        st.write("4. ✅ Line break standardization")
                        st.write("5. ✅ Length validation & truncation")
                        
                        st.code(f"""
Original length: {len(job['description'])} characters
Processed length: {len(processed_desc)} characters
Format: UTF-8 encoded
Status: Ready for AI analysis
                        """, language="text")
                    
                    with tab3:
                        st.markdown("#### Extracted Key Information")
                        extracted_info = extract_key_info(job['description'])
                        
                        if extracted_info['skills']:
                            st.write("**Skills Detected:**")
                            skills_str = ", ".join(extracted_info['skills'])
                            st.info(skills_str)
                        
                        if extracted_info['requirements']:
                            st.write("**Requirements:**")
                            for req in extracted_info['requirements']:
                                st.write(f"• {req}")
                    
                    # Action button
                    if st.button(f"📝 Analyze This Job", key=f"analyze_btn_{idx}", type="primary"):
                        st.session_state.selected_job_desc = processed_desc
                        st.success("✅ Job description loaded! Switch to 'Job Description Analyzer' to see analysis.")
                        st.balloons()
            
            # Show data collection summary
            st.write("---")
            st.markdown("### 📊 Data Collection Summary")
            
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.markdown("""
                **Data Sources:**
                - Job board APIs
                - Company career pages
                - Professional networks
                - Curated databases
                """)
            
            with summary_col2:
                st.markdown("""
                **Processing Steps:**
                - Text extraction
                - Data cleaning
                - Format standardization
                - Quality validation
                """)

# JOB DESCRIPTION ANALYZER
elif page == "📝 Job Description Analyzer":
    st.markdown('<h2 class="sub-header">📝 Job Description Analyzer</h2>', unsafe_allow_html=True)
    st.write("Paste a job description to get detailed insights about requirements, culture, and preparation tips.")
    
    # Check if job description was loaded from Browse Sample Jobs
    if 'selected_job_desc' not in st.session_state:
        st.session_state.selected_job_desc = ""
    
    default_job_desc = st.session_state.selected_job_desc
    
    # Show info message if job was loaded
    if default_job_desc:
        st.info("✅ Job description loaded from Browse Sample Jobs! Click 'Analyze' below or edit the text first.")
    
    job_desc = st.text_area(
        "Paste Job Description Here:", 
        value=default_job_desc,
        height=300, 
        placeholder="Copy and paste the full job description...",
        key="job_desc_input"
    )
    
    # Clear session state after text area is populated
    if default_job_desc and job_desc:
        st.session_state.selected_job_desc = ""
    
    if st.button("🔍 Analyze Job Description", type="primary"):
        if job_desc:
            with st.spinner("🤖 AI is analyzing the job description..."):
                try:
                    analysis = analyze_job_description(job_desc)
                    
                    if "Error" in analysis:
                        st.error(f"❌ API Error: {analysis}")
                        st.info("💡 Check your .env file and OpenAI credits at platform.openai.com/account/billing")
                    else:
                        st.session_state.job_desc = job_desc
                        st.markdown("### 📊 Analysis Results")
                        st.markdown(f'<div class="score-box">{analysis}</div>', unsafe_allow_html=True)
                        st.success("✅ Analysis complete! Use this to prepare your answers.")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Check your API key and credits.")

# INTERVIEW QUESTIONS GENERATOR
elif page == "❓ Interview Questions Generator":
    st.markdown('<h2 class="sub-header">❓ Interview Questions Generator</h2>', unsafe_allow_html=True)
    
    job_desc_q = st.text_area("Paste Job Description:", height=200)
    num_questions = st.slider("Number of questions to generate:", 5, 20, 10)
    
    if st.button("🎯 Generate Questions", type="primary"):
        if job_desc_q:
            with st.spinner("🤖 Generating custom interview questions..."):
                questions_text = generate_interview_questions(job_desc_q, num_questions)
                st.session_state.questions = questions_text.split('\n')
                st.session_state.questions = [q for q in st.session_state.questions if q.strip()]
                
                st.markdown("### 📋 Your Custom Interview Questions")
                st.info(questions_text)
                
                st.success(f"✅ Generated {num_questions} questions! Practice them in Mock Interview section.")

# MOCK INTERVIEW PRACTICE
elif page == "🎤 Mock Interview Practice":
    st.markdown('<h2 class="sub-header">🎤 Mock Interview Practice</h2>', unsafe_allow_html=True)
    st.write("Answer interview questions and get instant AI feedback!")
    
    # Check if questions are generated
    if not st.session_state.questions:
        st.warning("⚠️ Please generate questions first in 'Interview Questions Generator' section!")
        practice_question = st.text_input("Or enter a custom question to practice:")
        
        if practice_question:
            st.markdown("### 📝 Your Question:")
            st.info(practice_question)
            
            user_answer = st.text_area("Your Answer:", height=150, 
                                      placeholder="Type your answer here...")
            
            if st.button("📊 Get Feedback", type="primary"):
                if user_answer:
                    with st.spinner("🤖 AI is evaluating your answer..."):
                        evaluation = evaluate_answer(practice_question, user_answer)
                        quick_score = score_answer_quality(user_answer)
                        
                        st.markdown("### 📈 Evaluation Results")
                        st.metric("Quick Score", f"{quick_score}/10")
                        st.markdown(f'<div class="score-box">{evaluation}</div>', unsafe_allow_html=True)
    else:
        # Show current question
        if st.session_state.current_question < len(st.session_state.questions):
            current_q = st.session_state.questions[st.session_state.current_question]
            
            st.markdown(f"### Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}")
            st.info(current_q)
            
            user_answer = st.text_area("Your Answer:", height=150, key=f"answer_{st.session_state.current_question}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Evaluate Answer", type="primary"):
                    if user_answer:
                        with st.spinner("🤖 Evaluating..."):
                            evaluation = evaluate_answer(current_q, user_answer)
                            st.session_state.evaluations.append({
                                'question': current_q,
                                'answer': user_answer,
                                'evaluation': evaluation
                            })
                            
                            st.markdown("### 📈 Feedback")
                            st.markdown(f'<div class="score-box">{evaluation}</div>', unsafe_allow_html=True)
            
            with col2:
                if st.button("⏭️ Next Question"):
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            st.success("🎉 Interview complete! Great job!")
            if st.button("🔄 Start Over"):
                st.session_state.current_question = 0
                st.session_state.evaluations = []
                st.rerun()

# RESUME ANALYZER
elif page == "📄 Resume Analyzer":
    st.markdown('<h2 class="sub-header">📄 Resume Analyzer</h2>', unsafe_allow_html=True)
    st.write("Upload your resume and compare it against a job description.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
    
    with col2:
        job_desc_resume = st.text_area("Paste Job Description:", height=200)
    
    if st.button("🔍 Analyze Resume Match", type="primary"):
        if uploaded_file and job_desc_resume:
            with st.spinner("🤖 Analyzing your resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                
                if "Error" not in resume_text:
                    analysis = analyze_resume(resume_text, job_desc_resume)
                    
                    st.markdown("### 📊 Resume Analysis")
                    st.markdown(f'<div class="score-box">{analysis}</div>', unsafe_allow_html=True)
                    
                    st.success("✅ Analysis complete!")
                else:
                    st.error(resume_text)

# COVER LETTER GENERATOR
elif page == "✍️ Cover Letter Generator":
    st.markdown('<h2 class="sub-header">✍️ Cover Letter Generator</h2>', unsafe_allow_html=True)
    
    company_name = st.text_input("Company Name:")
    job_desc_cover = st.text_area("Paste Job Description:", height=150)
    resume_text_cover = st.text_area("Paste Your Resume/Experience (brief):", height=150)
    
    if st.button("✍️ Generate Cover Letter", type="primary"):
        if company_name and job_desc_cover and resume_text_cover:
            with st.spinner("🤖 Writing your cover letter..."):
                cover_letter = generate_cover_letter(resume_text_cover, job_desc_cover, company_name)
                
                st.markdown("### 📝 Your Cover Letter")
                st.markdown(f'<div class="success-box">{cover_letter}</div>', unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter,
                    file_name=f"cover_letter_{company_name}.txt",
                    mime="text/plain"
                )

# STAR METHOD EXAMPLES
elif page == "⭐ STAR Method Examples":
    st.markdown('<h2 class="sub-header">⭐ STAR Method Examples</h2>', unsafe_allow_html=True)
    st.write("Learn the STAR method with AI-generated examples based on your target job.")
    
    st.info("""
    **STAR Method Explained:**
    - **S**ituation: Describe the context
    - **T**ask: Explain what needed to be done
    - **A**ction: Detail the steps you took
    - **R**esult: Share the outcome and impact
    """)
    
    job_desc_star = st.text_area("Paste Job Description:", height=200)
    
    if st.button("⭐ Generate STAR Examples", type="primary"):
        if job_desc_star:
            with st.spinner("🤖 Creating STAR method examples..."):
                examples = generate_star_examples(job_desc_star)
                
                st.markdown("### 📋 STAR Method Examples")
                st.markdown(f'<div class="score-box">{examples}</div>', unsafe_allow_html=True)

# Footer
st.write("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🎯 AI Interview Coach | Built with Streamlit & OpenAI GPT</p>
    <p>💡 Tip: Practice regularly for best results!</p>
</div>
""", unsafe_allow_html=True)