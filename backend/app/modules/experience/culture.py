# Get cultural experiences
cultural_experiences = get_cultural_experiences(user_info)
if cultural_experiences:
    experience_names = ", ".join(exp["name"] for exp in cultural_experiences)
    ai_response += f"\n\nBased on your interests and location, I recommend checking out the following cultural experiences: {experience_names}."