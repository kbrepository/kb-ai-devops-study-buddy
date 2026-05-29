from agent.planner import generate_study_plan


def main():
    print("Welcome to KB AI DevOps Study Buddy")

    topic = input("Which topic do you want to study today? ")
    duration = int(input("How many minutes do you have? "))
    difficulty = input("Difficulty level? beginner/intermediate/advanced: ")

    plan = generate_study_plan(topic, duration, difficulty)
    print(plan)


if __name__ == "__main__":
    main()