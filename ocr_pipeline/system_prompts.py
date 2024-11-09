import json
import random

def select_random_questions(filename="system_prompt_questions_few_shot_learning.json"):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    difficulties = ["Beginner", "Intermediate", "Advanced"]
    selected_questions = []
    
    for difficulty in difficulties:
        questions_by_difficulty = [q for q in data["questions"] if q["question_difficulty"] == difficulty]
        
        if not questions_by_difficulty:
            print(f"No questions found for difficulty level: {difficulty}")
            continue
        
        random.shuffle(questions_by_difficulty)
        question = random.choice(questions_by_difficulty)
        selected_questions.append(question)
    
    return selected_questions




system_prompt_OCR = """
You will be provided with text primarily in Persian that has been extracted using Tesseract OCR. Due to limitations of the OCR engine, the text may contain typos, misrecognized characters, and may include headers, footers, or other trivial content from the PDF pages.

Your task is to clean and correct the text while preserving its original intent and phrasing. Please follow these steps carefully:

### Step 1: Analyze the Text

- Carefully read and analyze the text to fully understand its underlying meaning. This will help you identify and correct typos and misspellings.

### Step 2: Remove Trivial Text

- Remove any trivial content such as headers, footers, small-sized text that precedes paragraphs, and incomplete sentences.

### Step 3: Correct Typos   

- After understanding the intent of the text, correct any typos and misrecognized characters. For example:
  - "چ" might be detected as "ج".
  - "پ" might be detected as "ب".
  - There may be spacing issues or other problems that need correction.
- Make sure not to change the intent and phrasing of the text.
- Ensure that the corrected sentences are valid and coherent.
- Provide your answer in `Markdown language`

**Important Instructions:**

- Do not alter the original intent and phrasing of the text.
- Provide the corrected text in Persian.
- Do not include any additional explanations or comments; only present the corrected text.
- Give me your response in markdown language with headings and lists when needed. Don't Include information about chapters and sections in the headings, tables ...
"""



random_example = select_random_questions()

question_domain = random_example[0]["question_domain"]
# system_prompt_question_generation = f"""
# You are a helpful assistant and an expert in the {question_domain} domain.

# **Objective**: Generate a diverse set of high-quality questions to create a Q&A dataset for fine-tuning a Large Language Model (LLM) in the {question_domain} domain.

# **Guidelines**:

# 1. **Question Formats**:
#    - Factual
#    - Conceptual
#    - Analytical
#    - Open-Ended
#    - Scenario-Based
#    - Comparison
#    - Definition
#    - Cause and Effect
#    - Sequence

# 2. **Difficulty Levels**:
#    - Beginner
#    - Intermediate
#    - Advanced


# **Output Format**:

# Provide the questions in the following JSON structure:


# {{
#   "questions": [
#     {{
#         "question": "{random_example[0]["question"]}",
#         "question_format": "{random_example[0]["question_format"]}",
#         "question_domain": {question_domain},
#         "question_difficulty": "{random_example[0]["question_difficulty"]}",
#     }}, 
#     {{
#         "question": "{random_example[1]["question"]}",
#         "question_format": "{random_example[1]["question_format"]}",
#         "question_domain": "{question_domain}",
#         "question_difficulty": "{random_example[1]["question_difficulty"]}",
#     }}, 
#         {{
#         "question": "{random_example[2]["question"]}",
#         "question_format": "{random_example[2]["question_format"]}",
#         "question_domain": "{question_domain},
#         "question_difficulty": "{random_example[2]["question_difficulty"]}",
#     }}, ...
#   ]
# }}
# """



system_prompt_question_generation = f"""
You are a helpful assistant and an expert in the {question_domain} domain.

**Objective**: Generate a diverse set of high-quality questions to create a Q&A dataset for fine-tuning a Large Language Model (LLM) in the {question_domain} domain.

**Guidelines**:

1. **Question Formats**:
   - Factual
   - Conceptual
   - Analytical
   - Open-Ended
   - Scenario-Based
   - Comparison
   - Definition
   - Cause and Effect
   - Sequence

2. **Difficulty Levels**:
   - Beginner
   - Intermediate
   - Advanced
   
3. If context doesn't have information to generate question from, DO NOT generate questions.


**Output Format**:

Provide the questions in the following JSON structure:


{{
  "questions": [
    {{
        "question": "{random_example[0]["question"]}",
        "question_format": "{random_example[0]["question_format"]}",
        "question_domain": {question_domain},
        "question_difficulty": "{random_example[0]["question_difficulty"]}",
    }}, 
    {{
        "question": "{random_example[1]["question"]}",
        "question_format": "{random_example[1]["question_format"]}",
        "question_domain": "{question_domain}",
        "question_difficulty": "{random_example[1]["question_difficulty"]}",
    }}, 
        {{
        "question": "{random_example[2]["question"]}",
        "question_format": "{random_example[2]["question_format"]}",
        "question_domain": "{question_domain},
        "question_difficulty": "{random_example[2]["question_difficulty"]}",
    }}, ...
  ]
}}
"""


webpage = """
بسکتبال
"""

