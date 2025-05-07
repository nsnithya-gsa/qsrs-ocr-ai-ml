import random
from typing import List, Tuple

# this is used for file naming
algo_str = "medication_part_3"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.

medication_prompt_qa_dict_part_3 = {}

medication_prompt_qa_dict_part_3[1] = {
    "Q7": "no",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[2] = {
    "Q7": "yes",
    "Q62": "no",
    "Q63a": "no",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[3] = {
    "Q7": "yes",
    "Q62": "yes",
    "Q63": "yes",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[4] = {
    "Q7": "yes",
    "Q62": "no",
    "Q63a": "yes",
    "Q63b": "yes",
    "Q63c": "yes",
    "Q63d": "yes",
    "Q8": "no"
}

# value isn't in logical order; this was a dupe of 2
# so I moved the very last value up here
medication_prompt_qa_dict_part_3[5] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "yes",
    "Q74": "yes"
}

medication_prompt_qa_dict_part_3[6] = {
    "Q7": "yes",
    "Q62": "no",
    "Q63a": "yes",
    "Q63b": "no",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[7] = {
    "Q7": "yes",
    "Q62": "no",
    "Q63a": "yes",
    "Q63b": "yes",
    "Q63c": "yes",
    "Q63d": "none",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[8] = {
	"Q7": "no",
    "Q8": "yes",
    "Q64a": "yes",
    "Q64b": "yes",
    "Q64c": "yes",
    "Q64d": "yes",
    "Q64": "no",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[9] = {
	"Q7": "no",
    "Q8": "yes",
    "Q64a": "yes",
    "Q64b": "yes",
    "Q64c": "yes",
    "Q64d": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[10] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "yes",
    "Q64b": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[11] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[12] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "yes",
    "Q65": "no",
    "Q66": "no",
    "Q67": "no"
}

medication_prompt_qa_dict_part_3[13] = {
	"Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "yes",
    "Q65": "no",
    "Q66": "no",
    "Q67": "yes",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[14] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "yes",
    "Q65": "no",
    "Q66": "yes",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[15] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "yes",
    "Q65": "yes",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[16] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "yes",
    "Q69": "no",
    "Q72": "no"
}

medication_prompt_qa_dict_part_3[17] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "yes",
    "Q69": "no",
    "Q72": "yes",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[18] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "yes",
    "Q69": "yes",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[19] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "yes",
    "Q74": "no",
    "Q75": "no"
}

medication_prompt_qa_dict_part_3[20] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "yes",
    "Q74": "no",
    "Q75": "yes"
}

def build_Q7_prompt(answer):
    if answer == "yes":
        Q7_prompt = "During the stay, the patient received a hypoglycemic agent on day 4."
    else:
        Q7_prompt = "The record must not mention any hypoglycemic agents such as glucagon, D50, D10, etc."
    return Q7_prompt

def build_Q62_prompt(answer):
    if answer == "yes":
        Q62_prompt = "On day 3 of the stay, the patient's blood glucose was documented as being 45 mg/dL."
    else:
        Q62_prompt = "On no days during the stay was the patient's blood glucose documented as being at or below 50 mg/dL."
    return Q62_prompt

def build_Q63_prompt(answer):
    symptom_list = [
        "profuse sweating",
        "confusion",
        "seizure",
        "coma or loss of consiousness",
        "cardiac arrest or emergency measures to sustain life or call for rapid response team",
        "death"
    ]
    if answer == "yes":
        rand_symptom = random.choice(symptom_list)
        Q63_prompt = f"On day 3, the patient's blood glucose was documented as being 45 mg/dL, and the following was reported: {rand_symptom}."
    else:
        all_symptoms = ", ".join(symptom_list)
        Q63_prompt = f"The record must not mention any of the following as being associated with or occurring on a day when the patient's blood glucose was 50 or below: {all_symptoms}."
    return Q63_prompt

def build_Q63a_prompt(answer):
    if answer == "yes":
        Q63a_prompt = "The patient's blood glucose was only measured once during the stay, on day 3. On that day, it was documented as being 65 mg/dL."
    else:
        Q63a_prompt = "The patient's blood glucose was not measured during the stay."
    return Q63a_prompt

def build_Q63b_prompt(answer):
    if answer == "yes":
        Q63b_prompt = "The patient was administered glucagon on day 3, the same day blood glucose was measured to be 65 mg/dL."
    else:
        Q63b_prompt = "The record must not mention the patient receiving glucagon, D50, or D10 on day 3."
    return Q63b_prompt

# This data is part of Q63b's yes prompt
def build_Q63c_prompt():
    Q63c_prompt = ""
    return Q63c_prompt

def build_Q63d_prompt(answer):
    symptom_list = [
        "profuse sweating",
        "confusion",
        "seizure",
        "coma or loss of consiousness",
        "cardiac arrest or emergency measures to sustain life or call for rapid response team",
        "death"
    ]
    if answer == "yes":
        rand_symptom = random.choice(symptom_list)
        Q63d_prompt = f"On day 3, the record must note the following: {rand_symptom}."
    else:
        all_symptoms = ", ".join(symptom_list)
        Q63d_prompt = f"The record must not note any of the following happening on day 3: {all_symptoms}."
    return Q63d_prompt

def build_Q8_prompt(answer):
    if answer == "yes":
        Q8_prompt = "During the stay, the patient received an opioid."
    else:
        Q8_prompt = "The record must not mention the administration of any opioids during the patient's stay."
    return Q8_prompt

def build_Q64a_prompt(answer):
    if answer == "yes":
        Q64a_prompt = "The record must note that the patient was taking opioids prior to admission."
    else:
        Q64a_prompt = "The record must note that the patient was NOT taking opioids prior to admission."
    return Q64a_prompt

def build_Q64b_prompt(answer):
    if answer == "yes":
        Q64b_prompt = "The record must note that the opioid the patient was taking prior to admission was from a prescription."
    else:
        Q64b_prompt = "The record must note that the opioid the patient was taking prior to admission was NOT from a prescription."
    return Q64b_prompt

def build_Q64c_prompt(answer):
    if answer == "yes":
        Q64c_prompt = "The record must note that the opioid the patient was taking prior to admission had been prescribed to the patient, specifically."
    else:
        Q64c_prompt = "The record must note that although the opioid the patient was taking prior to admission was from a prescription, the prescription was written for someone else - not for the patient who was taking it."
    return Q64c_prompt

def build_Q64d_prompt(answer):
    if answer == "yes":
        Q64d_prompt = "The opioid the patient was taking prior to admission was dolophine (Methadone), for medication assisted treatment."
    else:
        Q64d_prompt = "The opioid the patient was taking prior to admission was hydrocodone and was NOT for medication assisted treatment."
    return Q64d_prompt

def build_Q64_prompt(answer):
    if answer == "yes":
        Q64_prompt = "The patient was administered naloxone later on the same day they were first administered an opioid in the hospital as an inpatient."
    else:
        Q64_prompt = "The patient was not administered naloxone during their stay."
    return Q64_prompt

def build_Q65_prompt(answer):
    if answer == "yes":
        Q65_prompt = "The record must note that the naloxone was administered during a procedure."
    else:
        Q65_prompt = "The record must not mention any procedures being performed on the patient."
    return Q65_prompt

def build_Q66_prompt(answer):
    if answer == "yes":
        Q66_prompt = "The record must note that the naloxone was administered for constipation."
    else:
        Q66_prompt = "The record must not mention pruritis, urinary retention, or constipation."
    return Q66_prompt

def build_Q67_prompt(answer):
    if answer == "yes":
        Q67_prompt = "The record must specify that the naloxone was only administered at the exact same time as the opioid."
    else:
        Q67_prompt = "The record must describe that the naloxone was administered 6 hours after the opiod on the same day as opiod administration."
    return Q67_prompt

def build_Q68_prompt(answer):
    if answer == "yes":
        Q68_prompt = "The record must specify that the patient experienced respiratory arrest 8 hours after the initial administration of the opioid during the stay."
    else:
        Q68_prompt = "The record must make no mention of respiratory arrest."
    return Q68_prompt

def build_Q69_prompt(answer):
    if answer == "yes":
        Q69_prompt = "The record must specify that this respiratory arrest is due to the patient's underlying condition or diagnosis."
    else:
        Q69_prompt = "The record must specify that this respiratory arrest is NOT due to the patient's underlying condition or diagnosis."
    return Q69_prompt

def build_Q72_prompt(answer):
    if answer == "yes":
        Q72_prompt = "The record must describe that the respiratory arrest was anticipated by clincal personanel based on the opioid dosage."
    else:
        Q72_prompt = "The record must note that the respiratory arrest was unexpected / unanticipated."
    return Q72_prompt

def build_Q73_prompt(answer):
    if answer == "yes":
        Q73_prompt = "The record must note that the patient became unresponsive to all but noxious stimulation 14 hours after the initial administration of the opioid."
    else:
        Q73_prompt = "The record must make no note of the patient becoming unresponsive during their stay."
    return Q73_prompt

def build_Q74_prompt(answer):
    if answer == "yes":
        Q74_prompt = "The record must specify that this unresponsiveness is attributed to the patient's underlying condition or diagnosis."
    else:
        Q74_prompt = "The record must specify that this unresponsiveness is NOT attributed to the patient's underlying condition or diagnosis."
    return Q74_prompt

def build_Q75_prompt(answer):
    if answer == "yes":
        Q75_prompt = "The record must specify that this unresponsiveness was anticipated by clincal personanel based on the opioid dosage."
    else:
        Q75_prompt = "The record must specify that this unresponsiveness was unexpected / unanticipated."
    return Q75_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(medication_prompt_qa_dict_part_3[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(medication_prompt_qa_dict_part_3.keys())
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
    question_keys = list(medication_prompt_qa_dict_part_3[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "Q7" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q7"]
        q7_prompt = build_Q7_prompt(ans)
        list_of_prompts.append(q7_prompt)
    if "Q62" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q62"]
        q62_prompt = build_Q62_prompt(ans)
        list_of_prompts.append(q62_prompt)
    if "Q63" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q63"]
        q63_prompt = build_Q63_prompt(ans)
        list_of_prompts.append(q63_prompt)
    if "Q63a" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q63a"]
        q63a_prompt = build_Q63a_prompt(ans)
        list_of_prompts.append(q63a_prompt)
    if "Q63b" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q63b"]
        q63b_prompt = build_Q63b_prompt(ans)
        list_of_prompts.append(q63b_prompt)
    if "Q63c" in question_keys:
        q63c_prompt = build_Q63c_prompt()
        list_of_prompts.append(q63c_prompt)
    if "Q63d" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q63d"]
        q63d_prompt = build_Q63d_prompt(ans)
        list_of_prompts.append(q63d_prompt)
    if "Q8" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q8"]
        q8_prompt = build_Q8_prompt(ans)
        list_of_prompts.append(q8_prompt)
    if "Q64a" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q64a"]
        q64a_prompt = build_Q64a_prompt(ans)
        list_of_prompts.append(q64a_prompt)
    if "Q64b" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q64b"]
        q64b_prompt = build_Q64b_prompt(ans)
        list_of_prompts.append(q64b_prompt)
    if "Q64c" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q64c"]
        q64c_prompt = build_Q64c_prompt(ans)
        list_of_prompts.append(q64c_prompt)
    if "Q64d" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q64d"]
        q64d_prompt = build_Q64d_prompt(ans)
        list_of_prompts.append(q64d_prompt)
    if "Q64" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q64"]
        q64_prompt = build_Q64_prompt(ans)
        list_of_prompts.append(q64_prompt)
    if "Q65" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q65"]
        q65_prompt = build_Q65_prompt(ans)
        list_of_prompts.append(q65_prompt)
    if "Q66" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q66"]
        q66_prompt = build_Q66_prompt(ans)
        list_of_prompts.append(q66_prompt)
    if "Q67" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q67"]
        q67_prompt = build_Q67_prompt(ans)
        list_of_prompts.append(q67_prompt)
    if "Q68" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q68"]
        q68_prompt = build_Q68_prompt(ans)
        list_of_prompts.append(q68_prompt)
    if "Q69" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q69"]
        q69_prompt = build_Q69_prompt(ans)
        list_of_prompts.append(q69_prompt)
    if "Q72" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q72"]
        q72_prompt = build_Q72_prompt(ans)
        list_of_prompts.append(q72_prompt)
    if "Q73" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q73"]
        q73_prompt = build_Q73_prompt(ans)
        list_of_prompts.append(q73_prompt)
    if "Q74" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q74"]
        q74_prompt = build_Q74_prompt(ans)
        list_of_prompts.append(q74_prompt)
    if "Q75" in question_keys:
        ans = medication_prompt_qa_dict_part_3[num]["Q75"]
        q75_prompt = build_Q75_prompt(ans)
        list_of_prompts.append(q75_prompt)
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