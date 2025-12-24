import streamlit as st

# Initialize session state for questions and score if they don't exist
if 'questions' not in st.session_state:
    # Starting with some default questions 
    st.session_state.questions = [
        {
            "question": "What is the primary service for running containers on Google Cloud?",
            "options": ["Google Kubernetes Engine", "Compute Engine", "Cloud Run", "App Engine"],
            "answer": "Cloud Run"
        },
        {
            "question": "Which Google Cloud storage class is best for data accessed once a year?",
            "options": ["Standard", "Nearline", "Coldline", "Archive"],
            "answer": "Archive"
        }
    ]

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

def add_question():
    """This function adds a new question in the quiz"""
    new_q = st.session_state.get('new_q_text')
    opt1 = st.session_state.get('opt1')
    opt2 = st.session_state.get('opt2')
    opt3 = st.session_state.get('opt3')
    opt4 = st.session_state.get('opt4')
    correct = st.session_state.get('correct_opt')
    
    if new_q and opt1 and opt2 and opt3 and opt4:
        new_entry = {
            "question": new_q,
            "options": [opt1, opt2, opt3, opt4],
            "answer": correct
        }
        st.session_state.questions.append(new_entry)
        #  This resets all selected options
        st.success("Question added successfully!")
    else:
        st.error("Please fill in all fields.")

# --- This is for sidebar navigation ---
with st.sidebar:
    st.title("Settings")
    page = st.radio("Go to:", ["Answer Quiz", "Add Questions"])
    
    st.divider()
    if st.button("Reset Quiz Progress"):
        st.session_state.score = 0
        st.session_state.quiz_submitted = False
        st.rerun()

# --- Main area---
if page == "Add Questions":
    st.title("➕ Add New Questions")
    st.write("Use this section to expand your quiz database.")
    
    with st.container(border=True):
        st.text_input("Enter Question:", key="new_q_text")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Option A:", key="opt1")
            st.text_input("Option B:", key="opt2")
        with col2:
            st.text_input("Option C:", key="opt3")
            st.text_input("Option D:", key="opt4")
        
        # Selection for the correct answer
        # We provide default labels if the fields are empty
        options_list = [
            st.session_state.get('opt1') or "Option A",
            st.session_state.get('opt2') or "Option B",
            st.session_state.get('opt3') or "Option C",
            st.session_state.get('opt4') or "Option D"
        ]
        st.selectbox("Select Correct Answer:", options_list, key="correct_opt")
        
        st.button("Save Question", on_click=add_question)

    st.subheader("Current Questions")
    for i, q in enumerate(st.session_state.questions):
        st.text(f"{i+1}. {q['question']}")

elif page == "Answer Quiz":
    st.title("🧠 Interactive Quiz")
    st.write(f"Total questions available: **{len(st.session_state.questions)}**")

    if not st.session_state.questions:
        st.info("No questions available. Switch to 'Add Questions' to create some!")
    else:
        # Now we handle the form submission part
        with st.form("quiz_form"):
            user_answers = []
            
            for i, q_data in enumerate(st.session_state.questions):
                st.markdown(f"### Q{i+1}: {q_data['question']}")
                choice = st.radio(
                    f"Select an option for Q{i+1}",
                    options=q_data['options'],
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
                user_answers.append(choice)
                st.divider()
                
            submit_button = st.form_submit_button("Submit Answers")

        if submit_button:
            st.session_state.score = 0
            st.session_state.quiz_submitted = True
            
            # Calculates results
            for i, q_data in enumerate(st.session_state.questions):
                if user_answers[i] == q_data['answer']:
                    st.session_state.score += 1
            
            # Display results
            st.balloons()
            st.header("📊 Results")
            final_score = st.session_state.score
            total = len(st.session_state.questions)
            percentage = (final_score / total) * 100
            
            col1, col2 = st.columns(2)
            col1.metric("Score", f"{final_score} / {total}")
            col2.metric("Accuracy", f"{percentage:.1f}%")

            if percentage == 100:
                st.success("Perfect score! You're a pro! 🏆")
            elif percentage >= 70:
                st.info("Great job! You passed!")
            else:
                st.warning("Keep practicing!")

st.markdown("---")

