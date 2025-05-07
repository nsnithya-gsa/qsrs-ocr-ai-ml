import random
from typing import List, Tuple

# this is used for file naming
algo_str = "medication_part_4"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.

medication_prompt_qa_dict_part_4 = {}

medication_prompt_qa_dict_part_4[1] = {
    "Q76": "no",
    "Q8a": "no"
}

medication_prompt_qa_dict_part_4[2] = {
    "Q76": "no",
    "Q8a": "yes", # page 9 starts - yes / no answer
    "Q70": "yes", # non-branching text answer
    "Q71": "yes" # non-branching text answer
}

medication_prompt_qa_dict_part_4[3] = {
    "Q76": "yes",
    "Q77": "all", # run the program for a patient given all listed opioids (unrealistic, but fine for testing) - if this isn't none just answer 78-80 in function 77
    "Q78": "yes", # non-branching text answer
    "Q79": "yes", # non-branching numerical answer
    "Q80": "yes", # yes / no answer
}

# all listed opioids are: "Hydrocodone", "Oxycodone", "Oxymorphone", "Morphine", "Codeine", "Fentanyl", "Tramadol"

medication_prompt_qa_dict_part_4[4] = {
    "Q76": "yes",
    "Q77": "hc-morph-fent", # run the program 3 non-consecutive parts of the step function to test jumping
    "Q78": "yes", # non-branching text answer
    "Q79": "yes", # non-branching numerical answer
    "Q80": "yes", # yes / no answer
}

def build_Q76_prompt(answer):
    if answer == "yes":
        Q76_prompt = ""
    else:
        Q76_prompt = ""
    return Q76_prompt

# for current stories, answer is either hc-morph-fent or all (none isn't an option; if Q76 is yes, the specific med(s) must be listed in Q77)
# This function also answers 78, 79, and 80 for each med separately
def build_Q77_prompt(answer):
    if answer == "hc-morph-fent":
        hc_morph_fent_prompts = [
            "At discharge the patient was prescribed hydrocodone at a dose of 5 mg; the prescription was for 10 pills with 1 refill.",
            "At discharge the patient was prescribed morphine at a dose of 5 mg; the prescription was for 2 pills with no refills.",
            "At discharge the patient was prescribed fentanyl at a dose of 5 mg; the prescription was for 2 pills with no refills.",
        ]
        Q77_prompt = " ".join(hc_morph_fent_prompts)
    elif answer == "all":
        all_meds_prompts = [
            "At discharge the patient was prescribed hydrocodone at a dose of 5 mg; the prescription was for 10 pills with 1 refill.",
            "At discharge the patient was prescribed oxycodone at a dose of 5 mg; the prescription was for 2 pills with no refills.",
            "At discharge the patient was prescribed oxymorphone at a dose of 5 mg; the prescription was for 2 pills with no refills.",
            "At discharge the patient was prescribed morphine at a dose of 5 mg; the prescription was for 2 pills with no refills.",
            "At discharge the patient was prescribed codeine at a dose of 5 mg; the prescription was for 2 pills with no refills.",
            "At discharge the patient was prescribed fentanyl at a dose of 5 mg; the prescription was for 2 pills with no refills.",
            "At discharge the patient was prescribed tramadol at a dose of 5 mg; the prescription was for 20 pills with 2 refills.",
        ]
        Q77_prompt = " ".join(all_meds_prompts)
    else:
        Q77_prompt = ""
    return Q77_prompt

# was there a medication event in the patient record about which there have been no prior questions?
def build_Q8a_prompt(answer):
    if answer == "yes":
        Q8a_prompt = "The record should note that there was an adverse event involving the medication Carprofen (canine painkiller) during the stay."
    else:
        Q8a_prompt = "The record should not list any other medications."
    return Q8a_prompt

# "identy the medication involved in the event noted in the chart - currently handled with Q8a's yes prompt"
def build_Q70_prompt():
    Q70_prompt = ""
    return Q70_prompt

# briefly describe what happened
def build_Q71_prompt():
    Q71_prompt = "The patient accidentally swallowed a Carprofen tablet from their personal belongings during their stay."
    return Q71_prompt


# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(medication_prompt_qa_dict_part_4[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(medication_prompt_qa_dict_part_4.keys())
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
    question_keys = list(medication_prompt_qa_dict_part_4[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "Q76" in question_keys:
        ans = medication_prompt_qa_dict_part_4[num]["Q76"]
        q76_prompt = build_Q76_prompt(ans)
        list_of_prompts.append(q76_prompt)
    if "Q77" in question_keys:
        ans = medication_prompt_qa_dict_part_4[num]["Q77"]
        q77_prompt = build_Q77_prompt(ans)
        list_of_prompts.append(q77_prompt)
    if "Q8a" in question_keys:
        ans = medication_prompt_qa_dict_part_4[num]["Q8a"]
        q8a_prompt = build_Q8a_prompt(ans)
        list_of_prompts.append(q8a_prompt)
    if "Q70" in question_keys:
        q70_prompt = build_Q70_prompt()
        list_of_prompts.append(q70_prompt)
    if "Q71" in question_keys:
        q71_prompt = build_Q71_prompt()
        list_of_prompts.append(q71_prompt)
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