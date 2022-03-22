import streamlit as st
import json
import glob


def clean(item):
    return item.split(":")[1].strip()

##Functions
def create_quiz(data):
    jupyterquiz_data = []
    for item in data:
        question, other = item.split(":", 1)[1].split("\n", 1)
        type_quiz, other = other.split("\n", 1)
        type_quiz = clean(type_quiz)
        answers = other.split("\n\n")
        answer_data = []
        for answer in answers:
            answer, correct, feedback = answer.strip().split("\n")
            answer = clean(answer)
            correct = bool(clean(correct))
            feedback = clean(feedback)
            answer_data.append(
                {"answer": answer,
                "correct": correct,
                 "feedback": feedback
                 })
        jupyterquiz_data.append({"question": question,
                                 "type": type_quiz,
                               "answers": answer_data})
            
            
        st.write(jupyterquiz_data)

def load_quiz(file):
    pass

def save_quiz(file):
    pass


st.title("Markdown-Based Quiz Generator for JupyterQuiz")
st.sidebar.header("Quiz Setup")
num_questions = st.sidebar.slider("Number of Questions", 1, 20)
num_answers = st.sidebar.slider("Default Number of Answers", 1, 5, 4)

default_data = ["Question:", "Type:\n"]
for x in range(num_answers):
    default_data.append(f"Answer {x+1}:")
    default_data.append(" - Correct:")
    default_data.append(" - Feedback:\n")

default_data = "\n".join(default_data)

quiz = st.form("Quiz Form")
for i in range(num_questions):
    
    
    qnum = i+1
    quiz.text_area(f"Question {qnum}", default_data, key=f"question_{qnum}", height=400)

if quiz.form_submit_button():
    all_questions = []
    for i in range(num_questions):
        qnum = i+1
        temp_question = st.session_state[f"question_{qnum}"]
        all_questions.append(temp_question)
    st.write(create_quiz(all_questions))