import streamlit as st
import json
import random
import time
from streamlit_autorefresh import st_autorefresh


# PAGE CONFIGURATION 

st.set_page_config(
    page_title="AI Decoded",
    layout="centered"
)

# STYLE

st.markdown("""
<style>
:root {
    --primary: #2F6FED;
    --primary-dark: #1F56C7;
    --primary-light: #5B9BFF;
    --primary-soft: #EAF2FF;
    --primary-border: #CFE0FB;
    --primary-text: #1B4DB1;
    --navy: #1E3A8A;
    --bg: #F8FAFC;
    --card: #FFFFFF;
    --border: #E2E8F0;
    --text: #1E293B;
    --text-muted: #64748B;
}

/* App background and content spacing */
.stApp {
    background-color: var(--bg);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

/* Text colours: the app uses a light background, so force readable dark text.
   This also prevents Streamlit's dark-theme defaults from making text invisible. */
.stApp,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp li,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stWidgetLabel"] p,
.stApp label,
.stApp [data-testid="stRadio"] label,
.stApp [data-testid="stRadio"] label p,
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"] {
    color: var(--text) !important;
}

/* Keep the custom welcome banner text white/light on its navy background. */
.welcome-banner .welcome-title {
    color: #FFFFFF !important;
}
.welcome-banner .welcome-tag {
    color: #93C5FD !important;
}
.welcome-banner .welcome-text {
    color: #DBEAFE !important;
}

/* Headings */
h1, h2, h3 {
    color: var(--text) !important;
}

/* Separators */
hr {
    border-color: var(--border);
}

/* Buttons */
.stButton > button {
    background-color: var(--primary-soft);
    color: var(--primary-text);
    border: 1px solid var(--primary-border);
    border-radius: 10px;
    font-weight: 500;
    min-height: 2.5rem;
    padding: 0.45rem 1rem;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #DCEAFF;
    border-color: var(--primary-light);
    color: var(--primary-dark);
}

.stButton > button:active,
.stButton > button:focus:not(:active) {
    background-color: #DCEAFF;
    border-color: var(--primary);
    color: var(--primary-dark);
}

/* Progress bar */
.progress-track {
    background: #DBE4F5;
    border-radius: 999px;
    height: 8px;
    width: 100%;
    overflow: hidden;
    margin: 0.6rem 0 1rem 0;
}

.progress-fill {
    background: var(--navy);
    height: 100%;
    border-radius: 999px;
    transition: width 0.3s ease;
}

/* Leaderboard tabs */
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--navy);
}

div[data-baseweb="tab-highlight"] {
    background-color: var(--navy);
}

/* Radio options (plain list, blue selection dot) */
div[data-testid="stRadio"] > div {
    gap: 0.45rem;
}

label[data-baseweb="radio"]:has(input:checked) > div:first-child {
    background-color: var(--primary) !important;
    border-color: var(--primary) !important;
}

/* Input fields and select boxes */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

/* Feedback and information boxes */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Question card */
.quiz-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    margin: 0.8rem 0 1.2rem 0;
    box-shadow: 0 3px 12px rgba(30, 64, 140, 0.05);
}

.quiz-label {
    color: var(--text-muted);
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.quiz-question {
    color: var(--text);
    font-size: 1.18rem;
    font-weight: 600;
    line-height: 1.6;
    margin-top: 0.55rem;
}

/* Welcome banner */
.welcome-banner {
    background: var(--navy);
    border-radius: 14px;
    padding: 1.8rem;
    margin: 0.8rem 0 1.4rem;
}

.welcome-tag {
    font-size: 0.75rem;
    color: #93C5FD;
    font-weight: 600;
    letter-spacing: 1.5px;
}

.welcome-title {
    font-size: 1.7rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 0.5rem;
}

.welcome-text {
    color: #DBEAFE;
    margin-top: 0.4rem;
}

/* Results score panel */
.result-card {
    background: var(--primary-soft);
    border: 1px solid var(--primary-border);
    border-radius: 16px;
    padding: 1.6rem;
    text-align: center;
    margin: 1rem 0;
}

.result-score {
    color: var(--navy);
    font-size: 2.8rem;
    font-weight: 700;
    margin: 0.3rem 0;
}

.result-caption {
    color: var(--text-muted);
    font-size: 0.95rem;
}

/* Answer review */
div[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_leaderboard(name, score, total, difficulty):
    leaderboard = load_leaderboard()

    percentage = (score / total) * 100 if total > 0 else 0

    leaderboard.append({
        "name": name,
        "score": score,
        "total": total,
        "percentage": round(percentage, 2),
        "difficulty": difficulty
    })

    leaderboard.sort(
        key=lambda item: item["percentage"],
        reverse=True
    )

    # Keep the top 10 for each difficulty level
    trimmed = []
    counts = {}
    for item in leaderboard:
        level = item.get("difficulty", "All Levels")
        counts[level] = counts.get(level, 0) + 1
        if counts[level] <= 10:
            trimmed.append(item)

    with open("leaderboard.json", "w") as file:
        json.dump(trimmed, file, indent=4)


def progress_bar(fraction):
    fraction = max(0.0, min(1.0, fraction))
    st.markdown(
        f"""
        <div class="progress-track">
            <div class="progress-fill" style="width: {fraction * 100:.0f}%;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


# LOAD QUESTION BANK

with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)

# PAGE TITLE

st.title("AI Decoded 🧩")


# INITIALIZE SESSION STATE

if "started" not in st.session_state:
    st.session_state.started = False

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = {}

if "finished" not in st.session_state:
    st.session_state.finished = False

if "deadline" not in st.session_state:
    st.session_state.deadline = None

if "hints_used" not in st.session_state:
    st.session_state.hints_used = []

if "review_answers" not in st.session_state:
    st.session_state.review_answers = {}

if "quiz_difficulty" not in st.session_state:
    st.session_state.quiz_difficulty = "All Levels"

# WELCOME SCREEN

if not st.session_state.started:

    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-tag">
            YOUR AI CHALLENGE
        </div>
        <div class="welcome-title">
            Think. Solve. Score.
        </div>
        <div class="welcome-text">
            Test your knowledge of Artificial Intelligence,
            from intelligent agents to search algorithms.
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.write("Rules:")
    
    st.markdown("""
            - **Units covered:** Unit I and Unit II of Artificial Intelligence
            - **Questions per attempt:** 10 randomly selected questions
            - **Maximum marks:** 10
            - **Marks per question:** 1
            - **Time limit:** 5 minutes
            - **Difficulty:** Choose Easy, Medium, Hard, or All Levels
            - **Feedback:** Receive feedback and explanations after submitting answers
            - **Hints:** Use hints when you need help understanding a concept
            - **Final review:** Review your answers and explanations after finishing
            """)


    difficulty = st.selectbox(
            "Choose difficulty level",
            ["All Levels", "Easy", "Medium", "Hard"]
        )
    
    if st.button("Start Quiz", use_container_width=True):

        if difficulty == "All Levels":
            available_questions = questions
        else:
            available_questions = [
                q for q in questions
                if q["difficulty"] == difficulty
            ]

        if len(available_questions) < 10:
            st.error(
                "There are fewer than 10 questions at this "
                "difficulty. Please choose another level."
            )
        else:
            st.session_state.quiz_questions = random.sample(
                available_questions, 10
            )

            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered = {}
            st.session_state.finished = False
            st.session_state.shuffled_options = {}
            st.session_state.started = True
            st.session_state.quiz_difficulty = difficulty
            st.session_state.deadline = time.time() + 300
            st.session_state.hints_used = []
            st.session_state.shuffled_options = {}

            st.rerun()

    st.divider()

    st.header("🏆 Quiz Leaderboard")

    leaderboard = load_leaderboard()

    levels = ["All Levels", "Easy", "Medium", "Hard"]
    level_tabs = st.tabs(levels)

    for tab, level in zip(level_tabs, levels):
        with tab:
            level_entries = [
                e for e in leaderboard
                if e.get("difficulty", "All Levels") == level
            ]

            if level_entries:
                for rank, entry in enumerate(level_entries[:10], start=1):
                    st.write(
                        f"{rank}. {entry['name']} — "
                        f"{entry['score']}/{entry['total']} marks "
                        f"({entry['percentage']}%)"
                    )
            else:
                st.info("No scores recorded yet. Complete a quiz to appear here!")

# QUIZ SCREEN


elif not st.session_state.finished:
    st_autorefresh(
        interval=1000,
        key="quiz_timer"
    )

    remaining_time = max(
        0,
        int(st.session_state.deadline - time.time())
    )

    minutes = remaining_time // 60
    seconds = remaining_time % 60

    st.metric(
        "Time Remaining",
        f"{minutes:02d}:{seconds:02d}"
    )

    if remaining_time <= 0:
        st.session_state.finished = True
        st.rerun()    

    index = st.session_state.current_question
    question = st.session_state.quiz_questions[index]

    progress_bar(
        (index + 1) / len(st.session_state.quiz_questions)
    )
    
    st.markdown(f"""
    <div class="quiz-card">
        <div class="quiz-label">
            Question {index + 1} of {len(st.session_state.quiz_questions)}
        </div>
        <div class="quiz-question">
            {question["question"]}
        </div>
        <div class="quiz-label" style="margin-top: 12px;">
            {question["topic"]} · {question["difficulty"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    hint_text = {
        "Foundations of AI":
            "Think about the abilities associated with intelligent systems.",
        "Applications of AI":
            "Identify the AI capability that best fits the application.",
        "Turing Test":
            "Focus on the machine's ability to imitate human responses.",
        "Rational Agents":
            "Consider the performance measure and available information.",
        "Intelligent Agents":
            "Recall the roles of sensors, percepts, and actuators.",
        "Agents and Environments":
            "Identify how the agent receives information and performs actions.",
        "Good Behaviour":
            "Consider how the agent's actions are evaluated.",
        "Nature of Environments":
            "Think about observability, uncertainty, and environmental changes.",
        "Problem Formulation":
            "Recall the components needed to define a search problem.",
        "Problem Spaces":
            "Think about possible configurations and reachable states.",
        "State Space Search":
            "Identify what each state represents and how actions connect states.",
        "Production Systems":
            "Recall the condition-action structure of production rules.",
        "Problem Characteristics":
            "Consider the structure of the problem and how it affects solving.",
        "Search Program Design":
            "Think about repeated states, goal tests, and search efficiency.",
        "Issues in Search Program Design":
            "Consider how repeated states and cycles affect search.",
        "Breadth-First Search":
            "Recall the data structure and level-by-level exploration.",
        "Depth-First Search":
            "Think about exploring a branch before backtracking.",
        "BFS State Space Problem":
            "List nodes level by level, following the specified child order.",
        "DFS State Space Problem":
            "Follow one branch deeply before returning to explore siblings.",
        "BFS vs DFS":
            "Compare completeness and the order in which nodes are explored.",
        "Iterative Deepening Search":
            "Think about depth limits that increase after each iteration.",
        "Hill Climbing":
            "Consider how the evaluation of neighbouring states guides movement.",
        "Hill Climbing Limitations":
            "Think about local optima and plateaus.",
        "Hill Climbing Variations":
            "Recall which methods sometimes accept worse moves.",
        "Heuristic Search":
            "A heuristic estimates how promising a state is.",
        "Best-First Search":
            "Identify the evaluation function used to prioritise frontier nodes.",
        "Best-First Search Problem":
            "Compare the heuristic values of all frontier nodes.",
        "Real-World Heuristic Search":
            "Consider how an estimate guides a route search.",
        "Constraint Satisfaction Problems":
            "Recall variables, domains, and constraints.",
        "CSP Applications":
            "Identify what must be assigned and which assignments conflict.",
        "CSP Constraints":
            "Remove values that violate the stated constraint.",
        "Means-End Analysis":
            "Compare the current state with the goal and identify an intermediate step.",
        "Real-World AI Applications":
            "Identify the AI task or capability used in the scenario.",
        "Rational Agents in Applications":
            "Consider the agent's objectives and available percepts.",
        "State Space Search":
            "Trace the possible transitions from the initial state.",
        "Search Cost":
            "Add the costs of the individual actions.",
        "Search Algorithms":
            "Match each algorithm to its defining search strategy.",
        "Assertion and Reasoning":
            "Evaluate the assertion and reason separately.",
        "Integrated AI Problem Solving":
            "Identify the search representation and guidance mechanism."
    }

    question_id = question["id"]

    if st.button("💡 Need a Hint?"):
        st.session_state.hints_used.append(question_id)

    if question_id in st.session_state.hints_used:
        st.info(
            hint_text.get(
                question["topic"],
                "Focus on the main concept in the question."
            )
        )        

    question_id = question["id"]

    if question_id not in st.session_state.answered:
        
        if "shuffled_options" not in st.session_state:
            st.session_state.shuffled_options = {}

        if question_id not in st.session_state.shuffled_options:
            options = question["options"].copy()
            random.shuffle(options)
            st.session_state.shuffled_options[question_id] = options

        selected_answer = st.radio(
            "Select your answer:",
            st.session_state.shuffled_options[question_id],
            key="answer_" + str(question_id)
        )


        if st.button("Submit Answer", use_container_width=True):

            is_correct = selected_answer == question["answer"]

            st.session_state.answered[question_id] = {
                "selected": selected_answer,
                "correct": is_correct
            }

            st.session_state.review_answers[question_id] = selected_answer

            if is_correct:
                st.session_state.score += 1

            st.rerun()

    else:

        result = st.session_state.answered[question_id]

        if result["correct"]:
            st.success("Correct answer! + 1 mark")
        else:
            st.error("Incorrect answer.")

        st.write("Correct answer:", question["answer"])
        st.info(question["explanation"])

        is_last_question = (
            index + 1 == len(st.session_state.quiz_questions)
        )

        if st.button(
            "End Quiz" if is_last_question else "Next Question",
            use_container_width=True
        ):

            if index + 1 < len(st.session_state.quiz_questions):
                st.session_state.current_question += 1
            else:
                st.session_state.finished = True

            st.rerun()

    st.divider()

# FINAL RESULTS SCREEN

else:

    st.balloons()

    st.title("Quiz Completed!")

    percentage = (st.session_state.score / 10) * 100

    st.markdown(f"""
    <div class="result-card">
        <div class="quiz-label">YOUR FINAL SCORE</div>
        <div class="result-score">
            {st.session_state.score} / 10
        </div>
        <div class="result-caption">
            {percentage:.0f}% · Quiz completed
        </div>
    </div>
    """, unsafe_allow_html=True)

    progress_bar(percentage / 100)


    if percentage >= 80:
        st.success("Excellent performance!")
    elif percentage >= 60:
        st.info("Good work! Keep practising.")
    elif percentage >= 40:
        st.warning("Keep revising the concepts.")
    else:
        st.error("Review the topics and try again.")

    
    st.divider()
    st.subheader("📝 Review Your Answers")

    for question in st.session_state.quiz_questions:
        question_id = question["id"]

        with st.expander(question["question"]):
            user_answer = st.session_state.review_answers.get(
                question_id,
                "Not answered"
            )

            st.write(f"**Your answer:** {user_answer}")
            st.write(f"**Correct answer:** {question['answer']}")
            st.write(f"**Explanation:** {question['explanation']}")

            if user_answer == question["answer"]:
                st.success("Correct")
            else:
                st.error("Incorrect")


    st.subheader("Save Your Result")

    player_name = st.text_input(
        "Enter your name",
        key="player_name"
    )

    if st.button("Save Score"):
        if player_name.strip():
            save_leaderboard(
                player_name.strip(),
                st.session_state.score,
                10,
                st.session_state.quiz_difficulty
            )
            st.success("Your score has been saved!")
        else:
            st.warning("Please enter your name first.")

    
    if st.button("Play Again", use_container_width=True):
        st.session_state.started = False
        st.session_state.finished = False
        st.session_state.quiz_questions = []
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = {}
        st.session_state.shuffled_options = {}
        st.session_state.deadline = None
        st.session_state.hints_used = []
        st.session_state.shuffled_options = {}
        st.session_state.review_answers = {}

        st.rerun()
