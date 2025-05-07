
import random
from typing import List, Tuple

# this is used for file naming
algo_str = "pressure_injury"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.


pressure_injury_prompt_qa_dict = {}

pressure_injury_prompt_qa_dict[1] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "EQ3a": "none"
}

pressure_injury_prompt_qa_dict[2] = {
    "EQ1": "yes",
    "EQ2": "no",
    "EQ3a": "ha",
    "Q5": "no",
    "Q5a": "yes"
}

pressure_injury_prompt_qa_dict[3] = {
    "EQ1": "no",
    "EQ2": "yes",
    "EQ3a": "ha",
    "Q5": "yes",
    "Q6": "yes"
}

pressure_injury_prompt_qa_dict[4] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "EQ3a": "ha",
    "Q5": "yes",
    "Q6": "no"
}

pressure_injury_prompt_qa_dict[5] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "EQ3a": "poa",
    "Q2": "no",
    "Q3": "no"
}

pressure_injury_prompt_qa_dict[6] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "EQ3a": "poa",
    "Q2": "no",
    "Q3": "yes"
}

def build_EQ1_prompt(answer):
    if answer == "yes":
        EQ1_prompt = "The record should note that a skin inspection WAS done within the first 24 hours of admission."
    else:
        EQ1_prompt = "The record should note that a skin inspection WAS NOT done within the first 24 hours of admission."
    return EQ1_prompt

def build_EQ2_prompt(answer):
    if answer == "yes":
        EQ2_prompt = "The record should note that a pressure injury risk assessment WAS documented within the first 24 hours of admission."
    else:
        EQ2_prompt = "The record should note that a pressure injury risk assessment WAS NOT documented within the first 24 hours of admission."
    return EQ2_prompt

# answer is "ha", "poa", or "none" 
def build_EQ3a_prompt(answer):
    if answer == "ha":
        EQ3a_prompt = f"The record should note that the patient had a hospital-acquired pressure injury ONLY."
    elif answer == "poa":
        EQ3a_prompt = f"The record should note that the patient had a present on admission pressure injury ONLY."
    else:
        EQ3a_prompt = "The record should note that the patient had no pressure injuries during their stay."
    return EQ3a_prompt

def build_Q2_prompt(answer):
    pi_type_list = [
            "stage 3",
            "stage 4",
            "unstageable",
            "deep tissue pressure injury"
        ]
    if answer == "yes":
        rand_pi_type = random.choice(pi_type_list)
        Q2_prompt = f"The pressure injury was noted as being {rand_pi_type} on admission."
    else:
        pi_types_str = ", ".join(pi_type_list)
        Q2_prompt = f"The records should note that no pressure injuries were any of the following on admission: {pi_types_str}."
    return Q2_prompt

def build_Q3_prompt(answer):
    pi_type_list = [
            "stage 3",
            "stage 4",
            "unstageable",
            "deep tissue pressure injury"
        ]
    if answer == "yes":
        rand_pi_type = random.choice(pi_type_list)
        Q3_prompt = f"The record should note that during the stay, a pressure injury that had been present on admission advanced to {rand_pi_type}."
    else:
        pi_types_str = ", ".join(pi_type_list)
        Q3_prompt = f"The record should state that no pressure injuries that were present on admission advanced to any of the following during the stay: {pi_types_str}."
    return Q3_prompt

def build_Q5_prompt(answer):
    pi_type_list = [
            "stage 3",
            "stage 4",
            "unstageable",
            "deep tissue pressure injury"
        ]
    if answer == "yes":
        rand_pi_type = random.choice(pi_type_list)
        Q5_prompt = f"During the stay, a new pressure injury that wasn't present on admission advanced to {rand_pi_type}."
    else:
        pi_types_str = ", ".join(pi_type_list)
        Q5_prompt = f"During the stay, no new pressure injury (not present on admission) advanced to any of the following: {pi_types_str}."
    return Q5_prompt

# The Q5a answer in dictionaries is always yes as a placeholder. This is a non-branching question with options.
def build_Q5a_prompt():
    stage_list = [
        "stage 1",
        "stage 2"
    ]
    rand_stage = random.choice(stage_list)
    Q5a_prompt = f"The record should note the most advanced stage of any new pressure injury (not present on admission) was {rand_stage}."
    return Q5a_prompt

# Q6 and Q7 are both handled with this one function, so Q7 is left out of the dictionaries, as it's non-branching and goes only to end.
def build_Q6_prompt(answer):
    secondary_morbidities = [
        "osteomyelitis",
        "tunneling",
        "fissure"
    ]
    if answer == "yes":
        rand_morbidity = random.choice(secondary_morbidities)
        Q6_prompt = f"The patient developed {rand_morbidity} as a secondary morbidity contiguous to pressure injury."
    else:
        morbidity_str = ", ".join(secondary_morbidities)
        Q6_prompt = f"The record should state that the patient developed none of the following as secondary morbidity contiguous to pressure injury: {morbidity_str}."
    return Q6_prompt


# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(story_number):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(pressure_injury_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(pressure_injury_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    patient_age = f"{random.randint(1, 99)} years old" # R1 and R2 both check if >= 365 days

    # create placeholders for variables that might get set / passed around between functions


    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(pressure_injury_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQ1" in question_keys:
        ans = pressure_injury_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = pressure_injury_prompt_qa_dict[num]["EQ2"]
        eq2_prompt = build_EQ2_prompt(ans)
        list_of_prompts.append(eq2_prompt)
    if "EQ3a" in question_keys:
        ans = pressure_injury_prompt_qa_dict[num]["EQ3a"]
        eq3a_prompt = build_EQ3a_prompt(ans)
        list_of_prompts.append(eq3a_prompt)
    if "Q2" in question_keys:
        ans = pressure_injury_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        ans = pressure_injury_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q5"in question_keys:
        ans = pressure_injury_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
    if "Q5a"in question_keys:
        q5a_prompt = build_Q5a_prompt()
        list_of_prompts.append(q5a_prompt)
    if "Q6" in question_keys:
        ans = pressure_injury_prompt_qa_dict[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans)
        list_of_prompts.append(q6_prompt)
    #######


    # after all build prompt functions that should be called are, add general prompts about the stay that might
    # not have been stated yet (remove duplicates at the end)
    list_of_prompts.append(f"Patient is {patient_age} old.")
    list_of_prompts.append(f"Patient was discharged on day number {discharge_day_number}.")

    prompt_string = " ".join(list_of_prompts)
    story_prompts_dict[num] = prompt_string

# when the loop is done running (prompts are generated for all stories)
# print to screen to be sure everything looks right
for num in story_numbers:
    print(f"full prompt to generate story number {num}:")
    print(story_prompts_dict[num])
    print()

import csv
csv_output_file = f"{algo_str}_prompts_{prompt_run}.csv"
with open(csv_output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write header
    writer.writerow(["story_definition", "story_prompt"])

    # Write each row
    for num in story_numbers:
        story_definition = generate_pdf_file_name(num)  # Function to get filename
        story_prompt = story_prompts_dict.get(num, "")  # Retrieve prompt, default to empty if missing

        writer.writerow([story_definition, story_prompt])

import json
json_output_file = f"{algo_str}_prompts_{prompt_run}.json"
data = []
# Build JSON data
for num in story_numbers:
    story_definition = generate_pdf_file_name(num)  # Function to get filename
    story_prompt = story_prompts_dict.get(num, "")  # Retrieve prompt, default to empty if missing

    data.append({
        "story_definition": story_definition,
        "story_prompt": story_prompt
    })
# Save to JSON file
with open(json_output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

