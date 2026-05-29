from agent.planner import generate_study_plan
from agent.interviewer import get_interview_questions


def main():
    print("Welcome to KB AI DevOps Study Buddy")
    print("1. Generate Study Plan")
    print("2. Interview Mode")

    choice = input("Choose an option: ")

    if choice == "1":
        topic = input("Which topic do you want to study today? ")
        duration = int(input("How many minutes do you have? "))
        difficulty = input("Difficulty level? beginner/intermediate/advanced: ")

        plan = generate_study_plan(topic, duration, difficulty)
        print(plan)

    elif choice == "2":
        topic = input("Which topic do you want interview questions for? ")
        questions = get_interview_questions(topic)

        print("\nInterview Questions:\n")
        for index, question in enumerate(questions, start=1):
            print(f"{index}. {question}")

    else:
        print("Invalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    main()