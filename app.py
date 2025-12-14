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

# Main title
st.markdown("# 🎯 AI Interview Coach")
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
    st.markdown("## 🔍 Browse Sample Jobs")
    st.write("Explore sample job descriptions collected and preprocessed from various sources.")
    st.info("💡 **Data Collection Demo:** This demonstrates web scraping and data collection capabilities.")
    
    from scraper import search_jobs, preprocess_job_for_analysis, extract_key_info
    
    # Search interface
    st.markdown("### Search Jobs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search by role:", value="", placeholder="e.g., data analyst")
    
    with col2:
        location_query = st.text_input("📍 Location:", value="", placeholder="e.g., remote")
    
    with col3:
        st.write("")
        st.write("")
        search_button = st.button("🔍 Search Jobs", type="primary")
    
    if 'selected_job_desc' not in st.session_state:
        st.session_state.selected_job_desc = None
    
    if search_button or not search_query:
        with st.spinner("🔄 Fetching job listings..."):
            jobs = search_jobs(query=search_query, location=location_query)
            
            st.success(f"✅ Found {len(jobs)} job posting(s)!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Jobs Collected", len(jobs))
            with col2:
                avg_length = sum(len(j['description']) for j in jobs) // len(jobs)
                st.metric("Avg Length", f"{avg_length} chars")
            with col3:
                st.metric("Data Sources", "5")
            
            st.write("---")
            
            for idx, job in enumerate(jobs):
                with st.expander(f"📄 {job['title']} at {job['company']} - {job['location']}", expanded=(idx==0)):
                    
                    tab1, tab2, tab3 = st.tabs(["📋 Job Description", "🔧 Processed Data", "📊 Extracted Info"])
                    
                    with tab1:
                        st.markdown("#### Original Job Posting")
                        processed_desc = preprocess_job_for_analysis(job)
                        st.text_area("Description:", processed_desc, height=300, key=f"job_{idx}", label_visibility="collapsed")
                    
                    with tab2:
                        st.markdown("#### Data Preprocessing Pipeline")
                        st.write("**Steps Applied:**")
                        st.write("1. ✅ HTML tag removal")
                        st.write("2. ✅ Whitespace normalization")
                        st.write("3. ✅ Special character cleaning")
                        st.write("4. ✅ Line break standardization")
                        st.write("5. ✅ Length validation")
                        
                        st.code(f"Original: {len(job['description'])} chars\nProcessed: {len(processed_desc)} chars", language="text")
                    
                    with tab3:
                        st.markdown("#### Extracted Information")
                        extracted_info = extract_key_info(job['description'])
                        
                        if extracted_info['skills']:
                            st.write("**Skills Detected:**")
                            st.info(", ".join(extracted_info['skills']))
                        
                        if extracted_info['requirements']:
                            st.write("**Requirements:**")
                            for req in extracted_info['requirements']:
                                st.write(f"• {req}")
                    
                    if st.button(f"📝 Analyze This Job", key=f"btn_{idx}", type="primary"):
                        st.session_state.selected_job_desc = processed_desc
                        st.success("✅ Job loaded! Switch to 'Job Description Analyzer' to see analysis.")
                        st.balloons()

# JOB DESCRIPTION ANALYZER
elif page == "📝 Job Description Analyzer":
    st.markdown("## 📝 Job Description Analyzer")
    st.write("Paste a job description to get detailed insights about requirements, culture, and preparation tips.")
    
    if 'selected_job_desc' not in st.session_state:
        st.session_state.selected_job_desc = ""
    
    default_job_desc = st.session_state.selected_job_desc
    
    if default_job_desc:
        st.info("✅ Job loaded from Browse Sample Jobs!")
    
    job_desc = st.text_area(
        "Paste Job Description Here:", 
        value=default_job_desc,
        height=300, 
        placeholder="Copy and paste the full job description..."
    )
    
    if default_job_desc and job_desc:
        st.session_state.selected_job_desc = ""
    
    if st.button("🔍 Analyze Job Description", type="primary"):
        if job_desc:
            with st.spinner("🤖 AI is analyzing the job description..."):
                try:
                    analysis = analyze_job_description(job_desc)
                    
                    if "Error" in analysis:
                        st.error(f"❌ {analysis}")
                        st.info("💡 Check your OpenAI API key and credits")
                    else:
                        st.markdown("### 📊 Analysis Results")
                        st.success("✅ Analysis Complete!")
                        
                        # Display results
                        st.markdown(f"""
                        <div style='background-color: white; padding: 25px; border-radius: 10px; 
                        border: 3px solid #1E88E5; color: black; font-size: 16px; line-height: 1.8;'>
                        {analysis.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📄 View Plain Text"):
                            st.text(analysis)
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# INTERVIEW QUESTIONS GENERATOR
elif page == "❓ Interview Questions Generator":
    st.markdown("## ❓ Interview Questions Generator")
    
    job_desc_q = st.text_area("Paste Job Description:", height=200)
    num_questions = st.slider("Number of questions:", 5, 20, 10)
    
    if st.button("🎯 Generate Questions", type="primary"):
        if job_desc_q:
            with st.spinner("🤖 Generating questions..."):
                questions_text = generate_interview_questions(job_desc_q, num_questions)
                st.session_state.questions = questions_text.split('\n')
                st.session_state.questions = [q for q in st.session_state.questions if q.strip()]
                
                st.markdown("### 📋 Your Interview Questions")
                st.success(f"✅ Generated {num_questions} questions!")
                st.write(questions_text)

# MOCK INTERVIEW PRACTICE
elif page == "🎤 Mock Interview Practice":
    st.markdown("## 🎤 Mock Interview Practice")
    st.write("Answer questions and get AI feedback!")
    
    if not st.session_state.questions:
        st.warning("⚠️ Generate questions first or enter a custom question.")
        practice_question = st.text_input("Custom question:")
        
        if practice_question:
            st.info(practice_question)
            user_answer = st.text_area("Your Answer:", height=150)
            
            if st.button("📊 Get Feedback", type="primary"):
                if user_answer:
                    with st.spinner("🤖 Evaluating..."):
                        evaluation = evaluate_answer(practice_question, user_answer)
                        quick_score = score_answer_quality(user_answer)
                        
                        st.markdown("### 📈 Results")
                        st.metric("Score", f"{quick_score}/10")
                        st.write(evaluation)
    else:
        if st.session_state.current_question < len(st.session_state.questions):
            current_q = st.session_state.questions[st.session_state.current_question]
            
            st.markdown(f"### Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}")
            st.info(current_q)
            
            user_answer = st.text_area("Your Answer:", height=150, key=f"ans_{st.session_state.current_question}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Evaluate", type="primary"):
                    if user_answer:
                        with st.spinner("🤖 Evaluating..."):
                            evaluation = evaluate_answer(current_q, user_answer)
                            st.markdown("### 📈 Feedback")
                            st.write(evaluation)
            
            with col2:
                if st.button("⏭️ Next"):
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            st.success("🎉 Complete!")
            if st.button("🔄 Start Over"):
                st.session_state.current_question = 0
                st.rerun()

# RESUME ANALYZER
elif page == "📄 Resume Analyzer":
    st.markdown("## 📄 Resume Analyzer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
    
    with col2:
        job_desc_resume = st.text_area("Job Description:", height=200)
    
    if st.button("🔍 Analyze", type="primary"):
        if uploaded_file and job_desc_resume:
            with st.spinner("🤖 Analyzing..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                
                if "Error" not in resume_text:
                    analysis = analyze_resume(resume_text, job_desc_resume)
                    st.markdown("### 📊 Analysis")
                    st.write(analysis)
                else:
                    st.error(resume_text)

# COVER LETTER GENERATOR
elif page == "✍️ Cover Letter Generator":
    st.markdown("## ✍️ Cover Letter Generator")
    
    company_name = st.text_input("Company Name:")
    job_desc_cover = st.text_area("Job Description:", height=150)
    resume_text_cover = st.text_area("Your Experience:", height=150)
    
    if st.button("✍️ Generate", type="primary"):
        if company_name and job_desc_cover and resume_text_cover:
            with st.spinner("🤖 Writing..."):
                cover_letter = generate_cover_letter(resume_text_cover, job_desc_cover, company_name)
                
                st.markdown("### 📝 Your Cover Letter")
                st.write(cover_letter)
                
                st.download_button(
                    label="📥 Download",
                    data=cover_letter,
                    file_name=f"cover_letter_{company_name}.txt",
                    mime="text/plain"
                )

# STAR METHOD EXAMPLES
elif page == "⭐ STAR Method Examples":
    st.markdown("## ⭐ STAR Method Examples")
    
    st.info("""
    **STAR Method:**
    - **S**ituation: Context
    - **T**ask: What needed doing
    - **A**ction: Steps you took
    - **R**esult: Outcome & impact
    """)
    
    job_desc_star = st.text_area("Job Description:", height=200)
    
    if st.button("⭐ Generate", type="primary"):
        if job_desc_star:
            with st.spinner("🤖 Creating examples..."):
                examples = generate_star_examples(job_desc_star)
                st.markdown("### 📋 Examples")
                st.write(examples)

# Footer
st.write("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>🎯 AI Interview Coach | Built with Streamlit & OpenAI GPT</p>
    <p>💡 Practice regularly for best results!</p>
</div>
""", unsafe_allow_html=True)