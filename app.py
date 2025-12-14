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
    st.info("💡 Data Collection Demo: Pre-collected job descriptions demonstrating data gathering capabilities")
    
    from scraper import search_jobs, preprocess_job_for_analysis, extract_key_info
    
    if 'selected_job_desc' not in st.session_state:
        st.session_state.selected_job_desc = ""
    
    # Auto-load all jobs without search bar
    with st.spinner("Loading sample jobs..."):
        jobs = search_jobs(query="", location="")
    
    st.success(f"✅ Showing {len(jobs)} sample job postings")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jobs Available", len(jobs))
    with col2:
        avg_length = sum(len(j['description']) for j in jobs) // len(jobs)
        st.metric("Avg Length", f"{avg_length} chars")
    with col3:
        st.metric("Industries", "5+")
    
    st.write("---")
    
    for idx, job in enumerate(jobs):
        with st.expander(f"📄 {job['title']} at {job['company']} - {job['location']}", expanded=(idx==0)):
            processed_desc = preprocess_job_for_analysis(job)
            
            tab1, tab2, tab3 = st.tabs(["📋 Description", "🔧 Processed", "📊 Extracted"])
            
            with tab1:
                st.text_area("Job Description:", processed_desc, height=250, key=f"j{idx}", label_visibility="collapsed")
            
            with tab2:
                st.write("**Preprocessing Steps:**")
                st.write("1. ✅ HTML tag removal")
                st.write("2. ✅ Whitespace normalization")
                st.write("3. ✅ Special character cleaning")
                st.write("4. ✅ UTF-8 encoding")
                st.code(f"Original: {len(job['description'])} chars\nProcessed: {len(processed_desc)} chars")
            
            with tab3:
                extracted_info = extract_key_info(job['description'])
                if extracted_info['skills']:
                    st.write("**Skills:**")
                    st.info(", ".join(extracted_info['skills']))
                if extracted_info['requirements']:
                    st.write("**Requirements:**")
                    for req in extracted_info['requirements']:
                        st.write(f"• {req}")
            
            if st.button(f"📝 Analyze This Job", key=f"b{idx}", type="primary"):
                st.session_state.selected_job_desc = processed_desc
                st.success("✅ Job loaded! Go to 'Job Description Analyzer'")
                st.balloons()

elif page == "📝 Job Description Analyzer":
    st.markdown("## 📝 Job Description Analyzer")
    
    if 'selected_job_desc' not in st.session_state:
        st.session_state.selected_job_desc = ""
    
    if st.session_state.selected_job_desc:
        st.info("✅ Job loaded from Browse Sample Jobs!")
    
    job_desc = st.text_area("Paste Job Description:", value=st.session_state.selected_job_desc, height=300, placeholder="Copy and paste job description...")
    
    if st.session_state.selected_job_desc and job_desc:
        st.session_state.selected_job_desc = ""
    
    if st.button("🔍 Analyze Job Description", type="primary"):
        if len(job_desc) > 10:
            with st.spinner("🤖 Analyzing..."):
                analysis = analyze_job_description(job_desc)
                
                if "Error" in analysis:
                    st.error(f"❌ {analysis}")
                    st.info("💡 Check API key and credits")
                else:
                    st.markdown("### 📊 Analysis Results")
                    st.success("✅ Complete!")
                    
                    st.markdown(f"""
                    <div style='background-color: white; padding: 25px; border-radius: 10px; 
                    border: 3px solid #1E88E5; color: black; font-size: 16px; line-height: 1.8;'>
                    {analysis.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📄 View Plain Text"):
                        st.text(analysis)
        else:
            st.warning("Please add a job description")

elif page == "❓ Interview Questions Generator":
    st.markdown("## ❓ Interview Questions Generator")
    job_desc_q = st.text_area("Job Description:", height=200)
    num_q = st.slider("Questions:", 5, 20, 10)
    
    if st.button("🎯 Generate", type="primary"):
        if job_desc_q:
            with st.spinner("Generating..."):
                questions_text = generate_interview_questions(job_desc_q, num_q)
                
                # Parse questions and store in session state for Mock Interview
                questions_list = [q.strip() for q in questions_text.split('\n') if q.strip() and len(q.strip()) > 10]
                st.session_state.questions = questions_list
                st.session_state.current_question = 0
                
                st.markdown("### 📋 Your Interview Questions")
                st.success(f"✅ Generated {len(questions_list)} questions!")
                st.write(questions_text)
                st.info("💡 These questions are now loaded in the Mock Interview Practice section!")

elif page == "🎤 Mock Interview Practice":
    st.markdown("## 🎤 Mock Interview Practice")
    
    if not st.session_state.questions or len(st.session_state.questions) == 0:
        st.warning("⚠️ No questions loaded! Generate questions first in 'Interview Questions Generator'")
        
        st.markdown("### Or practice with a custom question:")
        custom_q = st.text_input("Enter your question:")
        custom_a = st.text_area("Your answer:", height=150)
        
        if st.button("📊 Evaluate", type="primary"):
            if custom_q and custom_a:
                with st.spinner("Evaluating..."):
                    feedback = evaluate_answer(custom_q, custom_a)
                    score = score_answer_quality(custom_a)
                    st.metric("Score", f"{score}/10")
                    st.write(feedback)
    else:
        # Show generated questions
        if st.session_state.current_question < len(st.session_state.questions):
            current_q = st.session_state.questions[st.session_state.current_question]
            
            st.markdown(f"### Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}")
            st.info(current_q)
            
            answer = st.text_area("Your Answer:", height=150, key=f"a{st.session_state.current_question}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Evaluate Answer", type="primary"):
                    if answer:
                        with st.spinner("Evaluating..."):
                            feedback = evaluate_answer(current_q, answer)
                            score = score_answer_quality(answer)
                            
                            st.markdown("### 📈 Feedback")
                            st.metric("Score", f"{score}/10")
                            st.write(feedback)
            
            with col2:
                if st.button("⏭️ Next Question"):
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            st.success("🎉 You've completed all questions!")
            if st.button("🔄 Start Over"):
                st.session_state.current_question = 0
                st.rerun()

elif page == "📄 Resume Analyzer":
    st.markdown("## 📄 Resume Analyzer")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded = st.file_uploader("Upload PDF Resume", type=['pdf'])
    with col2:
        job_desc_r = st.text_area("Job Description:", height=200)
    
    if st.button("🔍 Analyze", type="primary"):
        if uploaded and job_desc_r:
            with st.spinner("Analyzing..."):
                resume_text = extract_text_from_pdf(uploaded)
                if "Error" not in resume_text:
                    result = analyze_resume(resume_text, job_desc_r)
                    st.markdown("### 📊 Analysis")
                    st.write(result)
                else:
                    st.error(resume_text)

elif page == "✍️ Cover Letter Generator":
    st.markdown("## ✍️ Cover Letter Generator")
    
    company = st.text_input("Company Name:")
    job_desc_c = st.text_area("Job Description:", height=150)
    experience = st.text_area("Your Experience Summary:", height=150)
    
    if st.button("✍️ Generate", type="primary"):
        if company and job_desc_c and experience:
            with st.spinner("Writing..."):
                letter = generate_cover_letter(experience, job_desc_c, company)
                st.markdown("### 📝 Your Cover Letter")
                st.write(letter)
                st.download_button("📥 Download", letter, f"{company}_cover.txt")

elif page == "⭐ STAR Method Examples":
    st.markdown("## ⭐ STAR Method Examples")
    
    st.info("""**STAR Method:**
- **S**ituation: Context
- **T**ask: What needed doing
- **A**ction: Steps taken
- **R**esult: Outcome""")
    
    job_desc_s = st.text_area("Job Description:", height=200)
    
    if st.button("⭐ Generate", type="primary"):
        if job_desc_s:
            with st.spinner("Creating..."):
                examples = generate_star_examples(job_desc_s)
                st.markdown("### 📋 Examples")
                st.write(examples)

st.write("---")
st.markdown("<div style='text-align: center; color: #888;'><p>🎯 AI Interview Coach | Built with Streamlit & OpenAI</p></div>", unsafe_allow_html=True)