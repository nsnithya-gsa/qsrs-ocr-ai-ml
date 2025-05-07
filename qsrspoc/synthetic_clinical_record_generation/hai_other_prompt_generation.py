import random
from typing import List, Tuple


# this is used for file naming
algo_str = "hai_other"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.

hai_other_prompt_qa_dict = {}

hai_other_prompt_qa_dict[1] = {
    "EQ1": "no"
}

hai_other_prompt_qa_dict[2] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "EQ3": "no"
}

hai_other_prompt_qa_dict[3] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "EQ3": "yes"
}

def build_EQ1_prompt(answer):
    if answer == "yes":
        EQ1_prompt = "The record should indicate that the patient acquired an infection in the hospital."
    else:
        EQ1_prompt = "The record should not mention any hospital-acquired infections not explicitly described in this prompt." # allows for combining with other algos
    return EQ1_prompt

# EQ2 has no branching; it's a follow-up to EQ1 being yes to collect / add more details - so the dict value is always yes, and answer isn't needed here
def build_EQ2_prompt():
    eq2_list = [
        "gastrointestinal infection caused by something other than C. Difficile",
        "eye, ear, nose, throat or mouth infection",
        "skin or soft tissue infection that was not related to a surgical site",
        "cardiovascular infection",
        "device-related infection (colonoscope, duodenoscope, bronchoscope)"
    ]
    rand_infection = random.choice(eq2_list)
    EQ2_prompt = f"The hospital acquired infection is of the following type: {rand_infection}."
    return EQ2_prompt

def build_EQ3_prompt(answer):
    if answer == "yes":
        mdro_list = [
            "methicillin-resistant Staphylococcus aureus (MRSA)",
            "vancomycin-resistant Enterobacter (VRE)",
            "carbepenem-resistant Enterobacteriacea (CRE)",
        ]
        rand_mdro = random.choice(mdro_list)
        EQ3_prompt = f"A multi drug resistant organism of type {rand_mdro} was associated with the hospital-acquired infection just described."
    else:
       EQ3_prompt = "The record should state that no multi-drug resistant organism was found to be associated with the hospital-acquired infection just described." 
    return EQ3_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(story_number):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(hai_other_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

# for clabsi this will be numbers 1 through 19
story_numbers = list(hai_other_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    # If R1 / R2 answer = "no" this changes to months old, from 1 to 11 (this avoids umbilical catheter complexity)
    patient_age = f"{random.randint(1, 99)} years old" # R1 and R2 both check if >= 365 days

    # create placeholders for variables that might get set / passed around between functions

    question_keys = list(hai_other_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQ1" in question_keys:
        ans = hai_other_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        eq2_prompt = build_EQ2_prompt()
        list_of_prompts.append(eq2_prompt)
    if "EQ3" in question_keys:
        ans = hai_other_prompt_qa_dict[num]["EQ3"]
        eq3_prompt = build_EQ3_prompt(ans)
        list_of_prompts.append(eq3_prompt)
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
csv_output_file = "hai_other_prompts.csv"
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
json_output_file = "hai_other_prompts.json"
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
