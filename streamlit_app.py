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
# from agent.bedrock_client import generate_ai_interview_questions, evaluate_answer_with_ai
from agent.usage_tracker import get_usage_summary
from agent.evaluation_history import save_ai_evaluation, get_evaluation_history
from agent.bedrock_client import (
    generate_ai_interview_questions,
    evaluate_answer_with_ai,
    generate_ai_study_plan,
    answer_from_notes,
    answer_from_notes_semantic,
    answer_from_notes_faiss
)

st.set_page_config(
    page_title="KB AI DevOps Study Buddy",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 KB AI DevOps Study Buddy")
st.write("Your personal AWS, Terraform, Kubernetes and DevOps interview preparation assistant.")
st.markdown("""
### What this app does

- Creates DevOps study plans
- Generates interview questions
- Evaluates your answers
- Tracks weak topics
- Builds a learning path
- Prepares you for AWS, Terraform and Kubernetes interviews
""")

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
        "AI Interview Questions",
        "Bedrock Usage Dashboard",
        "AI Answer Evaluation",
        "Evaluation History",
        "AI Study Plan",
        "AI Notes Assistant (FAISS RAG)"
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

elif menu == "AI Interview Questions":
    st.header("🤖 AI Interview Question Generator")

    topic = st.text_input("Topic", placeholder="Example: Terraform State")
    difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])
    count = st.slider("Number of questions", min_value=3, max_value=10, value=5)

    if st.button("Generate AI Questions"):
        with st.spinner("Generating questions using Amazon Bedrock..."):
            try:
                questions = generate_ai_interview_questions(topic, difficulty, count)
                st.markdown(questions)
            except Exception as error:
                st.error("Failed to generate questions from Bedrock.")
                st.exception(error)

elif menu == "Bedrock Usage Dashboard":
    st.header("📈 Bedrock Usage Dashboard")

    summary = get_usage_summary()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Requests", summary["total_requests"])
    col2.metric("Estimated Input Tokens", summary["total_input_tokens"])
    col3.metric("Estimated Output Tokens", summary["total_output_tokens"])

    st.subheader("Usage Records")
    st.dataframe(summary["records"])

elif menu == "AI Answer Evaluation":
    st.header("🧠 AI Answer Evaluation")

    topic = st.text_input("Topic", placeholder="Example: Terraform State")
    difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])
    question = st.text_area("Interview Question")
    user_answer = st.text_area("Your Answer")

    if st.button("Evaluate with AI"):
        if not topic or not question or not user_answer:
            st.warning("Please provide topic, question, and your answer.")
        else:
            with st.spinner("Evaluating answer using Amazon Bedrock..."):
                try:
                    feedback = evaluate_answer_with_ai(
                        topic=topic,
                        question=question,
                        user_answer=user_answer,
                        difficulty=difficulty,
                    )

                    st.markdown(feedback)
                    save_ai_evaluation(topic, difficulty, question, user_answer, feedback)
                    st.success("AI evaluation saved.")

                    add_weak_topic(topic)
                    st.info(f"{topic} added to weak topics for revision tracking.")

                except Exception as error:
                    st.error("Failed to evaluate answer using Bedrock.")
                    st.exception(error)

elif menu == "Evaluation History":
    st.header("📚 Evaluation History")

    evaluations = get_evaluation_history()

    if not evaluations:
        st.info("No AI evaluations saved yet.")
    else:
        for item in reversed(evaluations):
            with st.expander(f"{item['date']} | {item['topic']} | {item['difficulty']}"):
                st.write("Question:")
                st.write(item["question"])

                st.write("Your Answer:")
                st.write(item["user_answer"])

                st.write("AI Feedback:")
                st.markdown(item["ai_feedback"])

elif menu == "AI Study Plan":
    st.header("📘 AI Study Plan Generator")

    recommended_topic = get_recommended_topic()
    st.info(f"Recommended topic from weak topics: {recommended_topic}")

    topic = st.text_input("Topic", value=recommended_topic)
    duration = st.number_input("Duration in minutes", min_value=15, max_value=180, value=45)
    difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])

    if st.button("Generate AI Study Plan"):
        with st.spinner("Generating personalized study plan using Amazon Bedrock..."):
            try:
                plan = generate_ai_study_plan(topic, int(duration), difficulty)
                st.markdown(plan)

                add_study_session(topic, int(duration), difficulty)
                st.success("AI study session saved.")

            except Exception as error:
                st.error("Failed to generate AI study plan.")
                st.exception(error)

# elif menu == "Notes Assistant":
#     question = st.text_input(
#         "Ask a question"
#     )

#     if st.button("Search Notes"):
#         answer = answer_from_notes(question)
#         st.markdown(answer)
elif menu == "AI Notes Assistant (FAISS RAG)":
    st.header("AI Notes Assistant (FAISS RAG)")

    question = st.text_input(
        "Ask a question",
        placeholder="Example: How should EC2 securely access S3?"
    )

    if st.button("Search Notes"):
        if not question:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching notes using FAISS semantic retrieval..."):
                try:
                    answer, results, context = answer_from_notes_semantic(question)

                    st.subheader("Answer")
                    st.markdown(answer)

                    with st.expander("Retrieved Chunks"):
                        for item in results:
                            st.markdown(f"### Source: {item['source']}")
                            st.write(f"Chunk ID: {item['chunk_id']}")
                            st.write(f"Similarity Score: {item['score']:.4f}")
                            st.write(item["content"])
                            st.divider()

                    with st.expander("Full Context Sent to Bedrock"):
                        st.code(context)

                except Exception as error:
                    st.error("Failed to answer using Semantic RAG.")
                    st.exception(error)