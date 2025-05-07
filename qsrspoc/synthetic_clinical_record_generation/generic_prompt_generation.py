import random
from typing import List, Tuple

generic_prompt_qa_dict = {}

generic_prompt_qa_dict[1] = {
    "Q1": "yes",
    "Q1a": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "Q4": "yes",
    "Q5": "yes"
}

generic_prompt_qa_dict[2] = {
    "Q1": "yes",
    "Q1a": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "Q4": "no",
    "Q5": "yes"
}

generic_prompt_qa_dict[3] = {
    "Q1": "yes",
    "Q1a": "yes",
    "Q2": "yes",
    "Q3": "no",
    "Q5": "yes"
}

generic_prompt_qa_dict[4] = {
    "Q1": "no",
    "Q1a": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "Q4": "yes",
    "Q5": "yes"
}

generic_prompt_qa_dict[5] = {
    "Q1": "no",
    "Q1a": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "Q4": "no",
    "Q5": "yes"
}

generic_prompt_qa_dict[6] = {
    "Q1": "no",
    "Q1a": "yes",
    "Q2": "yes",
    "Q3": "no",
    "Q5": "yes"
}

def build_Q1_prompt(answer):
    if answer == "yes":
        Q1_prompt = f"The patient had a central venous catheter inserted during their stay. "
    else:
        Q1_prompt = "The patient did not have a central venous catheter inserted during their stay."
    return Q1_prompt

def build_Q1a_prompt():
    prompt_list = [
        "The patient was transferred to an inpatient floor from the emergency department.",
        "The patient was admitted to the hospital directly from another hospital",
        "The patient was admitted to the hospital from a physicians office"
    ]
    Q1a_prompt = random.choice(prompt_list)
    return Q1a_prompt

def build_Q2_prompt():
    insert_list = [
        "did",
        "did not"
    ]
    rand_insert = random.choice(insert_list)
    Q2_prompt = f"The patient {rand_insert} have a urinary tract catheter inserted during their stay."
    return Q2_prompt

def build_Q3_prompt(answer):
    if answer == "yes":
        Q3_prompt = "The patient required ventilator support that was not intiailly present on admission."
    else:
        Q3_prompt = "The patient did not require ventilator support during their hospitalization."
    return Q3_prompt

def build_Q4_prompt(answer, dis_day):
    vent_day = random.randint(3,dis_day)
    hour = random.randint(1,23)
    prompt_list = [
        f"The patient was placed on a ventilator after the first 24 hours of admission. Ventilation ocurred on day {vent_day}.",
        f"The patient's ventilator was initiated {hour}(s) after admission of the patient."
    ]
    Q4_prompt = random.choice(prompt_list)
    return Q4_prompt

def build_Q5_prompt():
    prompt_list = [
        "The patient had an operating room procedure during their hospitalization in the operating room.",
        "The patient did not have an operating room procedure during their hospitalization."
    ]
    Q5_prompt = random.choice(prompt_list)
    return Q5_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(generic_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(generic_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    patient_age = random.randint(1, 99)

    # create placeholders for variables that might get set / passed around between functions

    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(generic_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "Q1" in question_keys:
        ans = generic_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q1a" in question_keys:
        q1a_prompt = build_Q1a_prompt()
        list_of_prompts.append(q1a_prompt)
    if "Q2" in question_keys:
        q2_prompt = build_Q2_prompt()
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        ans = generic_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = generic_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans, discharge_day_number)
        list_of_prompts.append(q4_prompt)
    if "Q5" in question_keys:
        q5_prompt = build_Q5_prompt()
        list_of_prompts.append(q5_prompt)
    #######


    # after all build prompt functions that should be called are, add general prompts about the stay that might
    # not have been stated yet (remove duplicates at the end)
    list_of_prompts.append(f"Patient is {patient_age} years old.")
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
        story_definition = generate_pdf_file_name(algo_str, num, prompt_run)  # Function to get filename
        story_prompt = story_prompts_dict.get(num, "")  # Retrieve prompt, default to empty if missing

        writer.writerow([story_definition, story_prompt])

import json
json_output_file = f"{algo_str}_prompts_{prompt_run}.json"
data = []
# Build JSON data
for num in story_numbers:
    story_definition = generate_pdf_file_name(algo_str, num, prompt_run)  # Function to get filename
    story_prompt = story_prompts_dict.get(num, "")  # Retrieve prompt, default to empty if missing

    data.append({
        "story_definition": story_definition,
        "story_prompt": story_prompt
    })
# Save to JSON file
with open(json_output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)