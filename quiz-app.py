import streamlit as st
import json
import glob

def create_new_quiz(num_questions, file_name):
    new_quiz = {}
    for i in range(num_questions):
        
        new_quiz[f"Question {i+1}"] = {"question": "",
                                        "type": "",
                                        "answers": ""
                                      }
    
        with open (file_name, "w") as f:
            json.dump(new_quiz, f, indent=4)
            
            
st.title("JupyterQuiz Generator")
main_option = st.sidebar.selectbox("New vs. Old Quiz", ["Create a New Quiz", "Work with an Existing Quiz"])

if main_option == "Create a New Quiz":
    new_quiz_form = st.form("New Quiz")
    num_questions = new_quiz_form.slider("Number of Questions", 1,10)
    file_name = new_quiz_form.text_input("Type Your File Name")
    file_name = f"temp_quizzes/{file_name}.json"
    if new_quiz_form.form_submit_button():
        create_new_quiz(num_questions, file_name)

else:
 
    
    #Get all the Quizzes Loaded in the Temp_Quizzes Directory
    quizzes = glob.glob("temp_quizzes/*.json")
    
    #Have the user select which quiz they want to modify
    quiz_file = st.sidebar.selectbox("Select Quiz", quizzes)
    with open (quiz_file, "r") as f:
        quiz_data = json.load(f)
        
    #Establish How many Questions this quiz will have
    st.sidebar.header("Quiz Params")
    num_questions = st.sidebar.slider("Number of Questions", 1, 10)
    
    
    #This can be modified within each new form so that a user can select the type of question they are framing
    #And they can select the number of answers the current question will have. This gets around the limitations of nested
    #forms in Streamlit
    st.sidebar.header("Question Params")
    question_type = st.sidebar.selectbox("Type of Question",
                                         ["multiple_choice", "many_choice", "numeric"]
                                        )
    
    num_answers = st.sidebar.slider("Number of Potential Answers", 1, 5)
    
    #This allows us to store in ST's session state the current question we are on
    #We start our index at 1, rather than 0
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = 1
    
    #This modifies the number of questions into a more human-readable form
    questions  = []
    for i in range(num_questions):
        questions.append(f"Question {i+1}")
    
    
    current_question = st.selectbox("Question Number", questions)
    current_question = int(current_question.replace("Question ", ""))
    
    #We start generating the new Quiz. At each stage, we use the current question number and current answer number to ensure that we
    #Have a unique session state piece of data in the key attribute
    main_quiz = st.form(f"Question {current_question}")
    main_quiz.header(f"Question {current_question}")
    
    #Check to see if the current Quiz already has some data for this question. If so, it loads it up.
    if f"Question {current_question}" in quiz_data:
        temp_question = main_quiz.text_input(f"Question Text",
                                             quiz_data[f"Question {current_question}"]["question"]
                                            )
        main_quiz.write("<br><br>", unsafe_allow_html=True)
        for x in range(num_answers):
            main_quiz.header(f"Answer {x+1}")
            try:
                temp_answer = main_quiz.text_input(f"Answer Text",
                                                   quiz_data[f"Question {current_question}"]["answers"][x]["answer"],
                                                   key=f"answer_{x+1}")

                temp_correct = main_quiz.radio(f"Correct Data",
                                               [True, False],
                                               key=f"correct_{x+1}")

                temp_feedback = main_quiz.text_input(f"Feedback Text",
                                                     quiz_data[f"Question {current_question}"]["answers"][x]["feedback"],
                                                     key=f"feedback_{x+1}")
            #If a usere is trying to add questions to an existing quiz, there will be an index error. In this case, we simply populate the fields
            #with empty space
            except:
                IndexError
                temp_answer = main_quiz.text_input(f"Answer Text",
                                                   key=f"answer_{x+1}")

                temp_correct = main_quiz.radio(f"Correct Data",
                                               [True, False],
                                               key=f"correct_{x+1}")

                temp_feedback = main_quiz.text_input(f"Feedback Text",
                                                     key=f"feedback_{x+1}")
            main_quiz.write("<br>", unsafe_allow_html=True)
    
    #If there is nothing preopulated in the quiz for this particular question number, then we populate blank fields
    else:
        temp_question = main_quiz.text_input(f"Question {current_question}")
        for x in range(num_answers):
            main_quiz.header(f"Answer {x+1}")
            temp_answer = main_quiz.text_input(f"Answer Text",
                                               key=f"answer_{x+1}")

            temp_correct = main_quiz.radio(f"Correct Data",
                                           [True, False],
                                           key=f"correct_{x+1}")

            temp_feedback = main_quiz.text_input(f"Feedback Text",
                                                 key=f"feedback_{x+1}")
            main_quiz.write("<br>", unsafe_allow_html=True)
    
    #This submits the current question and answer data from the form
    submit = main_quiz.form_submit_button(f"Submit {current_question}")
    if submit:
        #we iterate through the different answers for this question and grab the unique session state key
        #for each part of each answer. We then recreate this as JupyterQuiz formatted data.
        temp_answers = []
        for x in range(num_answers):
            answer_data = {"answer": st.session_state[f"answer_{x+1}"],
                           "correct": st.session_state[f"correct_{x+1}"],
                          "feedback": st.session_state[f"feedback_{x+1}"],

                          }
            temp_answers.append(answer_data)
        
        #We now add this to our main quiz_data dictionary to the corresponding question.
        quiz_data[f"Question {current_question}"] = {"question": temp_question,
                                                     "type": question_type,
                                                    "answers": temp_answers
                                                            }
        
        #We need to still restructure the data into JupyterQuiz format as a list, rather than a dictionary with each
        #Question as a key
        final_quiz = []
        for item in quiz_data:
            final_quiz.append(quiz_data[item])

        #We store 2 different files: one for the temp quizzes, used by the app
        #The second for final quizzes that can be imported into JupyterQuiz
        st.write(final_quiz)
        with open (quiz_file, "w") as f:
            json.dump(quiz_data, f, indent=4)

        with open (quiz_file.replace("temp_quizzes", "final_quizzes"), "w") as f:
            json.dump(quiz_data, f, indent=4)