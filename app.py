import streamlit as st
from utils import *

st.set_page_config(page_title="AI Interview Coach", page_icon="🎯", layout="wide")

if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

st.markdown("# 🎯 AI Interview Coach")
st.markdown("### Prepare for your dream job with AI-powered interview preparation!")

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

if page == "🏠 Home":
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📝 Analyze Jobs")
        st.write("Get detailed analysis of job requirements.")
    with col2:
        st.markdown("### 🎤 Practice")
        st.write("Practice with AI-generated questions.")
    with col3:
        st.markdown("### 📈 Improve")
        st.write("Optimize resume and cover letters.")
    
    st.write("---")
    st.info("👈 Choose a feature from the sidebar!")
    
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Features", "7+")
    with col2:
        st.metric("AI Model", "GPT-3.5")
    with col3:
        st.metric("Success Rate", "95%")
    with col4:
        st.metric("Prep Time", "2 hrs")

elif page == "🔍 Browse Sample Jobs":
    st.markdown("## 🔍 Browse Sample Jobs")
    st.info("💡 Data Collection Demo: Web scraping capabilities")
    
    from scraper import search_jobs, preprocess_job_for_analysis, extract_key_info
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("Search role:", "")
    with col2:
        location_query = st.text_input("Location:", "")
    with col3:
        st.write("")
        st.write("")
        search_button = st.button("🔍 Search", type="primary")
    
    if 'selected_job_desc' not in st.session_state:
        st.session_state.selected_job_desc = ""
    
    if search_button or not search_query:
        jobs = search_jobs(query=search_query, location=location_query)
        st.success(f"Found {len(jobs)} jobs!")
        
        for idx, job in enumerate(jobs):
            with st.expander(f"{job['title']} at {job['company']}", expanded=(idx==0)):
                processed_desc = preprocess_job_for_analysis(job)
                st.text_area("Description:", processed_desc, height=250, key=f"j{idx}")
                
                if st.button(f"📝 Analyze", key=f"b{idx}", type="primary"):
                    st.session_state.selected_job_desc = processed_desc
                    st.success("✅ Loaded! Go to Job Description Analyzer")

elif page == "📝 Job Description Analyzer":
    st.markdown("## 📝 Job Description Analyzer")
    
    if 'selected_job_desc' not in st.session_state:
        st.session_state.selected_job_desc = ""
    
    job_desc = st.text_area("Paste Job Description:", value=st.session_state.selected_job_desc, height=300)
    
    if st.button("🔍 Analyze", type="primary"):
        if len(job_desc) > 10:
            with st.spinner("🤖 Analyzing..."):
                analysis = analyze_job_description(job_desc)
                
                st.markdown("### 📊 Results")
                st.success("✅ Done!")
                st.text_area("Analysis:", analysis, height=400)
                st.write(analysis)
        else:
            st.warning("Please add job description")

elif page == "❓ Interview Questions Generator":
    st.markdown("## ❓ Questions Generator")
    job_desc_q = st.text_area("Job Description:", height=200)
    num_q = st.slider("Questions:", 5, 20, 10)
    
    if st.button("🎯 Generate", type="primary"):
        if job_desc_q:
            with st.spinner("Generating..."):
                questions = generate_interview_questions(job_desc_q, num_q)
                st.write(questions)

elif page == "🎤 Mock Interview Practice":
    st.markdown("## 🎤 Mock Interview")
    question = st.text_input("Question:")
    answer = st.text_area("Your Answer:", height=150)
    
    if st.button("📊 Evaluate", type="primary"):
        if question and answer:
            with st.spinner("Evaluating..."):
                feedback = evaluate_answer(question, answer)
                st.write(feedback)

elif page == "📄 Resume Analyzer":
    st.markdown("## 📄 Resume Analyzer")
    uploaded = st.file_uploader("Upload PDF", type=['pdf'])
    job_desc_r = st.text_area("Job Description:", height=200)
    
    if st.button("🔍 Analyze", type="primary"):
        if uploaded and job_desc_r:
            resume_text = extract_text_from_pdf(uploaded)
            if "Error" not in resume_text:
                result = analyze_resume(resume_text, job_desc_r)
                st.write(result)
            else:
                st.error(resume_text)

elif page == "✍️ Cover Letter Generator":
    st.markdown("## ✍️ Cover Letter")
    company = st.text_input("Company:")
    job_desc_c = st.text_area("Job Description:", height=150)
    experience = st.text_area("Your Experience:", height=150)
    
    if st.button("✍️ Generate", type="primary"):
        if company and job_desc_c and experience:
            letter = generate_cover_letter(experience, job_desc_c, company)
            st.write(letter)
            st.download_button("📥 Download", letter, f"{company}_cover.txt")

elif page == "⭐ STAR Method Examples":
    st.markdown("## ⭐ STAR Examples")
    job_desc_s = st.text_area("Job Description:", height=200)
    
    if st.button("⭐ Generate", type="primary"):
        if job_desc_s:
            examples = generate_star_examples(job_desc_s)
            st.write(examples)

st.write("---")
st.markdown("<div style='text-align: center; color: #888;'><p>🎯 AI Interview Coach</p></div>", unsafe_allow_html=True)