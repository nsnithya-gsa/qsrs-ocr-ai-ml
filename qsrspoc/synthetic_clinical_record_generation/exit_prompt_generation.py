import random
from typing import List, Tuple


# this is used for file naming
algo_str = "exit"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.


exit_prompt_qa_dict = {}

exit_prompt_qa_dict[1] = {
    "Q1": "no",
    "L1": "no",
    "L2": "no"
}

exit_prompt_qa_dict[2] = {
    "Q1": "yes",
    "Q2": "yes",
    "L1": "yes",
    "Q3": "no"
}

exit_prompt_qa_dict[3] = {
    "Q1": "yes",
    "Q2": "yes",
    "L1": "no",
    "L2": "no"
}

exit_prompt_qa_dict[4] = {
    "Q1": "yes",
    "Q2": "yes",
    "L1": "no",
    "L2": "yes",
    "Q4": "no",
    "Q5": "yes"
}

exit_prompt_qa_dict[5] = {
    "Q1": "yes",
    "Q2": "yes",
    "L1": "yes",
    "Q3": "yes"
}

def build_Q1_prompt(answer):
    if answer == "yes":
        Q1_prompt = "The patient experienced an adverse event not mentioned elsewhere in this prompt. The following sentence describes it."
    else:
        Q1_prompt = "The clinical record should not note any adverse event not already specified in this prompt."
    return Q1_prompt

# Q2 is non-branching and free-text; no answer is needed. "yes" is used in dicts as a placeholder value only.
def build_Q2_prompt():
    q2_list = [
        "accidental paralysis due to a nerve block",
        "ICU delirium",
        "in-hospital malnutrition"
    ]
    rand_event = random.choice(q2_list)
    Q2_prompt = f"The adverse event was {rand_event}."
    return Q2_prompt

def build_L1_prompt(answer):
    if answer == "yes":
        L1_prompt = "The patient's discharge status is Died. They passed away during their stay. They were not an infant born during the visit nor a person who gave birth during the stay."
    else:
        L1_prompt = "The record should not state that the patient died during the stay and provide a discharge status that isn't Died."
    return L1_prompt

def build_L2_prompt(answer):
    if answer == "yes":
        adverse_event_list = [
            "hospital-acquired infection",
            "a non-operating-room invasive procedure at an incorrect site",
            "an allergic response to a drug, with anaphylaxis documented within 2 hours of the medication administration. The record should indicate they had no known allergies"
        ]
        rand_adverse_event = random.choice(adverse_event_list)
        L2_prompt = f"The record should note that the patient's stay involved the following adverse event: {rand_adverse_event}"
    else:
        L2_prompt = "The record should state that no adverse event occurred during the patient's stay."
    return L2_prompt

def build_Q3_prompt(answer):
    if answer == "yes":
        Q3_prompt = "The record should state that the patient's death WAS related to an adverse event mentioned in this prompt."
    else:
        Q3_prompt = "The record should state that the patient's death WAS NOT related to an adverse event mentioned in this prompt."
    return Q3_prompt

# prompting gets complicated if Q1 is "no" and Q4 is "yes". Q4 doesn't branch, so we set the answer always to "no" in the dicts.
# if prompt-generation is combined between algorithms, this should be updated
def build_Q4_prompt(answer):
    if answer == "yes":
        Q4_prompt = "The record should indicate that the patient DID experience harm because of an adverse event mentioned in this prompt."
    else:
        Q4_prompt = "The record should indicate that the patient DID NOT experience harm related to ANY adverse event mentioned in this prompt."
    return Q4_prompt

def build_Q5_prompt(answer):
    if answer == "yes":
        Q5_prompt = "The record should indicate that the patients family WAS notified of an adverse event mentioned in this prompt."
    else:
        Q5_prompt = "The record should indicate that the patients family WAS NOT notified of ANY adverse event mentioned in this prompt."
    return Q5_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(story_number):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(exit_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(exit_prompt_qa_dict.keys())
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
    question_keys = list(exit_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "Q1" in question_keys:
        ans = exit_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q2" in question_keys:
        q2_prompt = build_Q2_prompt()
        list_of_prompts.append(q2_prompt)
    if "L1" in question_keys:
        ans = exit_prompt_qa_dict[num]["L1"]
        l1_prompt = build_L1_prompt(ans)
        list_of_prompts.append(l1_prompt)
    if "L2" in question_keys:
        ans = exit_prompt_qa_dict[num]["L2"]
        l2_prompt = build_L2_prompt(ans)
        list_of_prompts.append(l2_prompt)
    if "Q3" in question_keys:
        ans = exit_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = exit_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "Q5" in question_keys:
        ans = exit_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
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
csv_output_file = f"{algo_str}_prompts.csv"
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
json_output_file = f"{algo_str}_prompts.json"
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