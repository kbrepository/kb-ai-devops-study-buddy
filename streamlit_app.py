import streamlit as st

from agent.planner import generate_study_plan
from agent.interviewer import get_interview_questions
from agent.memory import (
    add_study_session,
    add_weak_topic,
    view_progress,
    get_recommended_topic,
    get_latest_session_summary,
)
from agent.evaluator import evaluate_answer
from agent.roadmap import generate_learning_path


st.set_page_config(
    page_title="KB AI DevOps Study Buddy",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 KB AI DevOps Study Buddy")
st.write("Your personal AWS, Terraform, Kubernetes and DevOps interview preparation assistant.")

menu = st.sidebar.radio(
    "Choose Feature",
    [
        "Study Plan",
        "Interview Questions",
        "Evaluate Answer",
        "Progress",
        "Weak Topics",
        "Learning Path",
        "Session Summary",
    ],
)

if menu == "Study Plan":
    st.header("📘 Generate Study Plan")

    topic = st.text_input("Topic", placeholder="Example: Terraform State")
    duration = st.number_input("Duration in minutes", min_value=15, max_value=180, value=45)
    difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])

    if st.button("Generate Plan"):
        plan = generate_study_plan(topic, int(duration), difficulty)
        st.text(plan)
        add_study_session(topic, int(duration), difficulty)
        st.success("Study session saved.")

elif menu == "Interview Questions":
    st.header("🎯 Interview Questions")

    topic = st.text_input("Topic", placeholder="Example: Terraform")
    if st.button("Generate Questions"):
        questions = get_interview_questions(topic)
        for index, question in enumerate(questions, start=1):
            st.write(f"{index}. {question}")

elif menu == "Evaluate Answer":
    st.header("🧠 Evaluate Interview Answer")

    topic = st.text_input("Evaluation Topic", placeholder="Example: terraform state")
    answer = st.text_area("Your Answer")

    if st.button("Evaluate"):
        result = evaluate_answer(topic, answer)

        st.subheader(f"Score: {result['score']}/10")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Matched Points")
            for item in result["matched"]:
                st.success(item)

        with col2:
            st.write("Missing Points")
            for item in result["missing"]:
                st.warning(item)

        st.info(result["feedback"])

        if result["score"] < 7:
            add_weak_topic(topic)
            st.warning(f"{topic} added to weak topics.")

elif menu == "Progress":
    st.header("📊 Progress Tracker")

    progress = view_progress()

    st.subheader("Completed Topics")
    st.write(progress.get("completed_topics", []))

    st.subheader("Weak Topics")
    st.write(progress.get("weak_topics", []))

    st.subheader("Study Sessions")
    st.write(progress.get("study_sessions", []))

elif menu == "Weak Topics":
    st.header("⚠️ Weak Topic Manager")

    topic = st.text_input("Add Weak Topic", placeholder="Example: Kubernetes Probes")

    if st.button("Add Weak Topic"):
        add_weak_topic(topic)
        st.success(f"{topic} added to weak topics.")

    st.subheader("Recommended Topic")
    st.info(get_recommended_topic())

elif menu == "Learning Path":
    st.header("🛣️ Recommended Learning Path")

    path = generate_learning_path()

    for index, item in enumerate(path, start=1):
        st.write(f"{index}. {item}")

elif menu == "Session Summary":
    st.header("📝 Latest Session Summary")
    st.text(get_latest_session_summary())