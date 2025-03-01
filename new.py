learners_data = [
    {
        "id": 1,
        "name": "Alice",
        "capability": 80,
        "gender": "female",
        "style": "visual"
    },
    {
        "id": 2,
        "name": "Bob",
        "capability": 75,
        "gender": "male",
        "style": "auditory"
    }
]
learners_map = {}
for learner in learners_data:
    learners_map[learner["id"]]=learner


print(learners_map[1])
