from agent.planner import generate_study_plan
from agent.interviewer import get_interview_questions
from agent.memory import add_study_session, add_weak_topic, view_progress
from agent.memory import add_study_session, add_weak_topic, view_progress, get_recommended_topic

def main():
    print("Welcome to KB AI DevOps Study Buddy")
    print("1. Generate Study Plan")
    print("2. Interview Mode")
    print("3. Add Weak Topic")
    print("4. View Progress")
    print("5. Recommend Topic")
    print("6. Generate Daily Plan from Weak Topic")

    choice = input("Choose an option: ")

    if choice == "1":
        topic = input("Which topic do you want to study today? ")
        duration = int(input("How many minutes do you have? "))
        difficulty = input("Difficulty level? beginner/intermediate/advanced: ")

        plan = generate_study_plan(topic, duration, difficulty)
        print(plan)

        add_study_session(topic, duration, difficulty)
        print("Study session saved.")

    elif choice == "2":
        topic = input("Which topic do you want interview questions for? ")
        questions = get_interview_questions(topic)

        print("\nInterview Questions:\n")
        for index, question in enumerate(questions, start=1):
            print(f"{index}. {question}")
    
    elif choice == "3":
        topic = input("Which topic do you want to mark as weak? ")
        add_weak_topic(topic)
        print(f"{topic} added to weak topics.")

    elif choice == "4":
        progress = view_progress()

        print("\nYour Progress:\n")
        print("Completed Topics:")
        for topic in progress["completed_topics"]:
            print(f"- {topic}")

        print("\nWeak Topics:")
        for topic in progress["weak_topics"]:
            print(f"- {topic}")

        print("\nStudy Sessions:")
        for session in progress["study_sessions"]:
            print(
                f"- {session['date']} | {session['topic']} | "
                f"{session['duration']} mins | {session['difficulty']}"
            )

    elif choice == "5":
        topic = get_recommended_topic()
        print(f"\nRecommended topic for today: {topic}")

    elif choice == "6":
        topic = get_recommended_topic()
        duration = int(input("How many minutes do you have today? "))
        difficulty = input("Difficulty level? beginner/intermediate/advanced: ")

        print(f"\nUsing recommended weak topic: {topic}")

        plan = generate_study_plan(topic, duration, difficulty)
        print(plan)

        add_study_session(topic, duration, difficulty)
        print("Daily plan saved.")

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    main()