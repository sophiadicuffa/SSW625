 # prompt_pattern_issues

import json
import csv
from datetime import datetime

with open('raw/issues.json', 'r') as file:
    data = json.load(file)

def analyze_prompt_structure(data):
    detected_patterns = []

    persona_keywords = ["you are", "act as", "pretend to be", "pretend you are"]
    recipe_keywords = ["step-by-step", "recipe", "guide"]
    template_keywords = ["template", "formatting"]
    automator_keywords = ["script", "code", "executable"]
    simple_instruction_keywords = ["explain", "describe", "list", "tell me", "give me"]
    context_instruction_keywords = ["based on", "with this information"]
    question_keywords = ["what", "where", "when", "who", "why"]

    def contains_keywords(text, keywords):
        return any(keyword in text.lower() for keyword in keywords)

    for source in data.get("Sources", []):
        body = source.get("Body", "")
        created_at = source.get("CreatedAt")
        closed_at = source.get("ClosedAt")
        state = "Closed" if closed_at is not None else "Open"

        time_lapsed = None
        if created_at and closed_at:
            created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            closed_at_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
            time_lapsed = closed_at_dt - created_at_dt

        body_patterns = []

        if contains_keywords(body, persona_keywords):
            body_patterns.append("Persona Pattern")
        if contains_keywords(body, recipe_keywords):
            body_patterns.append("Recipe Pattern")
        if contains_keywords(body, template_keywords):
            body_patterns.append("Template Pattern")
        if contains_keywords(body, automator_keywords):
            body_patterns.append("Output Automator Pattern")
        if contains_keywords(body, simple_instruction_keywords):
            body_patterns.append("Simple Instruction Pattern")
        if contains_keywords(body, context_instruction_keywords):
            body_patterns.append("Context and Instruction Pattern")
        if contains_keywords(body, question_keywords):
            body_patterns.append("Question Pattern")

        conversations = source.get("ChatgptSharing", [])
        for item in conversations:
            number_of_prompts = item.get("NumberOfPrompts", "N/A")
            conversation_url = item.get("URL", "N/A")

            for pattern in body_patterns:
                detected_patterns.append((
                    source['Number'],
                    pattern,
                    state,
                    time_lapsed,
                    number_of_prompts,
                    conversation_url
                ))

    return detected_patterns

patterns = analyze_prompt_structure(data)

with open("detected_patterns_issues.csv", "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Issue Number", "Detected Pattern", "State", "Time Lapsed", "Number of Prompts", "Conversation"])
    for number, pattern, state, time_lapsed, number_of_prompts, conversation_url in patterns:
        csv_writer.writerow([number, pattern, state, time_lapsed, number_of_prompts, conversation_url])

print("detected_patterns_issues.csv.")
