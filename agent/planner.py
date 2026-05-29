def generate_study_plan(topic, duration, difficulty):
    concept_time = int(duration * 0.25)
    hands_on_time = int(duration * 0.35)
    interview_time = int(duration * 0.25)
    notes_time = duration - concept_time - hands_on_time - interview_time

    return f"""
Today's DevOps Study Plan

Topic: {topic}
Difficulty: {difficulty}
Duration: {duration} minutes

Plan:
1. {concept_time} min - Understand/revise core concept
2. {hands_on_time} min - Practice hands-on commands or scenario
3. {interview_time} min - Answer interview-style questions
4. {notes_time} min - Write short notes for revision

Mock Question:
Explain {topic} in a real-world DevOps project.
"""