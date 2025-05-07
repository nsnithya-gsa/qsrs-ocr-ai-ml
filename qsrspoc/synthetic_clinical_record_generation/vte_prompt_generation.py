import random
from typing import List, Tuple

# this is used for file naming
algo_str = "vte"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.

vte_prompt_qa_dict = {}

vte_prompt_qa_dict[1] = {
    "EQ1": "yes"
}

vte_prompt_qa_dict[2] = {
    "EQ1": "no",
    "EQ2": "yes"
}

vte_prompt_qa_dict[3] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "no",
    "EQ4": "no",
    "EQ6": "no",
    "EQ7": "neither" # pe, dvt, or both - wait, no counts as neither/can't tell and exits - make it "neither"
}

vte_prompt_qa_dict[4] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "no",
    "EQ4": "yes",
    "EQ5": "yes",
    "EQ7": "neither" # pe, dvt, or both
}

vte_prompt_qa_dict[5] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "no",
    "EQ4": "no",
    "EQ6": "yes",
    "EQ7": "neither" # pe, dvt, or both
}

"""
shortest route through page 1 is (it's purposely not implemented above):
{
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes"
    "EQ7": ___
}
"""

# EQ7 = both is only needed for one dict: with Q2 = yes, Q3 = yes, Q3a = no, Q4 = yes, so that R3 can be yes, hitting Q5b. 
vte_prompt_qa_dict[6] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "both",
    "Q2": "yes",
    "Q3": "yes",
    "Q3a": "no",
    "Q4": "yes",
    "Q5b": "yes"
}

vte_prompt_qa_dict[7] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "both",
    "Q2": "yes",
    "Q3": "yes",
    "Q3a": "no",
    "Q4": "yes",
    "Q5b": "none"
}

# EQ7 = dvt covers all branches in page 2
vte_prompt_qa_dict[8] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "dvt",
    "Q2": "yes",
    "Q3": "yes",
    "Q3a": "yes"
}

vte_prompt_qa_dict[9] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "dvt",
    "Q2": "yes",
    "Q3": "none"
}

vte_prompt_qa_dict[10] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "dvt",
    "Q2": "none"
}

# EQ7 = pe jumps to Q5a, then covers all of page 3 and 4 except Q5b
# Q5a = none jumps to page 4, then exits through R4a & b (no prompts for those). 
vte_prompt_qa_dict[11] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "pe",
    "Q5a": "none"
}

# The step function uses a pass state with flags to handle R4a & b; to get through that we need conf.pe to be true.
# conf.pe is only true if Q6a = no (the last q on p3). So there's no need to handle page 4 except for that case.

vte_prompt_qa_dict[12] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "pe",
    "Q5a": "none"
}

vte_prompt_qa_dict[13] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "pe",
    "Q5a": "yes",
    "Q6": "none"
}

vte_prompt_qa_dict[14] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "pe",
    "Q5a": "yes",
    "Q6": "yes",
    "Q6a": "yes"
}

# cover page 4 with shortest route through 1-3
vte_prompt_qa_dict[15] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "pe",
    "Q5a": "yes",
    "Q6": "yes",
    "Q6a": "no",
    "R5": "yes",
    "Q7": "yes",
    "R6": "yes",
    "Q8": "yes",
    "Q9": "yes"
}

vte_prompt_qa_dict[16] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "pe",
    "Q5a": "yes",
    "Q6": "yes",
    "Q6a": "no",
    "R5": "yes",
    "Q7": "yes",
    "R6": "no"
}

vte_prompt_qa_dict[17] = {
    "EQ1": "no",
    "EQ2": "no",
    "EQR1": "yes",
    "EQ7": "pe",
    "Q5a": "yes",
    "Q6": "yes",
    "Q6a": "no",
    "R5": "no"
}

def build_EQ1_prompt(answer):
    eq1_list = [
            "deep vein thrombosis",
            "pulmonary embolism"
        ]
    if answer == "yes":
        rand_vte = random.choice(eq1_list)
        EQ1_prompt = f"On admission, the patient had {rand_vte}"
    else:
        vte_str = ", ".join(eq1_list)
        EQ1_prompt = f"On admission, the patient had none of the following: {vte_str}."
    return EQ1_prompt

def build_EQ2_prompt(answer):
    if answer == "yes":
        EQ2_prompt = "On admission, the patient DID have unilateral leg swelling."
    else:
        EQ2_prompt = "On admission, the patient DID NOT have unilateral leg swelling."
    return EQ2_prompt

def build_EQR1_prompt(answer, patient_age):
    if answer == "yes":
        if patient_age >= 18:
            patient_age = random.randint(1,17)
        EQR1_prompt = "The patient is pediatric (under 18 years old)."
    else:
        if patient_age < 18:
            patient_age = random.randint(18, 99)
        EQR1_prompt = "The patient is not pediatric (18 years old or older)."
    return EQR1_prompt, patient_age

def build_EQ4_prompt(answer):
    if answer == "yes":
        EQ4_prompt = "On admission, venous thromboembolism (VTE) prophylaxis WAS ordered."
    else:
        EQ4_prompt = "On admission, venous thromboembolism (VTE) prophylaxis WAS NOT ordered."
    return EQ4_prompt

def build_EQ5_prompt():
    eq5_list = [
        "anticoagulants",
        "physical / mechanical vte prophylaxis"
    ]
    num_to_choose = random.randint(1, len(eq5_list))
    rand_type = random.sample(eq5_list, num_to_choose)
    EQ5_prompt = f"The following type(s) of prophylaxis was ordered on admission: {rand_type}."
    return EQ5_prompt

def build_EQ6_prompt(answer):
    if answer == "yes":
        EQ6_prompt = "The clinical record MUST state that venous thromboembolism (VTE) prophylaxis was contraindicated."
    else:
        EQ6_prompt = "The clinical record MUST NOT state that venous thromboembolism (VTE) prophylaxis was contraindicated."
    return EQ6_prompt

# The answer (pe, dvt, both, [neither/can't tell -> end]) determines flow of control for this algorithm, requiring dict customization
def build_EQ7_prompt(answer):
    if answer == "neither":
        EQ7_prompt = "The record should make no mention of pulmonary embolism or deep vein thrombosis occurring during the stay."
    elif answer == "pe":
        EQ7_prompt = "The record must note that during the stay, a pulmonary embolism occurred but it should make no mention of deep vein thrombosis."
    elif answer == "dvt":
        EQ7_prompt = "The record must note that during the stay, a deep vein thrombosis occurred but it should make no mention of pulmonary embolism."
    else: # both
        EQ7_prompt = "The record must note that during the stay, both a pulmonary embolism and a deep vein thrombosis occurred."
    return EQ7_prompt

def build_Q2_prompt(answer):
    q2_list = [
        "venous compression ultrasound or duplex ultrasound",
        "magnetic resonance imaging (mri)",
        "computed tomography (ct) with contrast medium",
        "venography"
    ]
    if answer == "yes":
        num_to_select = random.randint(1, len(q2_list))
        rand_test_list = random.sample(q2_list, num_to_select)
        rand_test_str = ", ".join(rand_test_list)
        Q2_prompt = f"The record should note that the following diagnostic test(s) confirmed the deep vein thrombosis: {rand_test_str}."
    else:
        all_test_str = ", ".join(q2_list)
        Q2_prompt = f"The record should NOT mention any of the following diagnostic tests for deep vein thrombosis: {all_test_str}."
    return Q2_prompt

def build_Q3_prompt(answer):
    q3_list = [
        "pain",
        "tenderness",
        "swelling",
        "redness"
    ]
    if answer == "yes":
        num_to_select = random.randint(1, len(q3_list))
        rand_symptom_list = random.sample(q3_list, num_to_select)
        rand_symptom_str = ", ".join(rand_symptom_list)
        Q3_prompt = f"The following symptoms must be documented more than 48 hours after admission: {rand_symptom_str}."
    else:
        all_symptom_str = ", ".join(q3_list)
        Q3_prompt = f"The record should make no mention of the following symptoms: {all_symptom_str}."
    return Q3_prompt

def build_Q3a_prompt(answer):
    if answer == "yes":
        Q3a_prompt = "The record should state that comfort care HAD been ordered for the patient during the stay, BEFORE the occurrence of deep vein thrombosis."
    else:
        Q3a_prompt = "The record should NOT mention anything about comfort care"
    return Q3a_prompt

def build_Q4_prompt(answer):
    location_list = [
        "lower extremity, proximal",
        "lower extremity, distal",
        "upper extremity",
        "upper thorax"
    ]
    if answer == "yes":
        num_to_select = random.randint(1, len(location_list))
        rand_location_list = random.sample(location_list, num_to_select)
        rand_location_str = ", ".join(rand_location_list)
        Q4_prompt = f"Deep vein thrombosis was noted at the following location(s): {rand_location_str}."
    else:
        Q4_prompt = "The medical record should NOT discuss or describe the location of the deep vein thrombosis."
    return Q4_prompt

def build_Q5a_prompt(answer):
    q5a_list = [
        "computed tomography angiography of pulmonary arteries with contrast",
        "high probability nuclear medicine V/Q scan",
        "Magnetic Resonsance Imaging (MRI) of pulmonary arteries",
        "pulmonary angiography",
        "post-mortem exam finding that PE likely contributed to death"
    ]
    if answer == "yes":
        num_to_select = random.randint(1, len(q5a_list))
        test_list = random.sample(q5a_list, num_to_select)
        test_list_str = ", ".join(test_list)
        Q5a_prompt = f"The diagnostic test(s) that confirmed the pulmonary embolism are: {test_list_str}"
    else:
        q5a_list_str = ", ".join(q5a_list)
        Q5a_prompt = f"The record should state that none of the following diagnostic tests were run to confirm the pulmonary embolism: {q5a_list_str}"
    return Q5a_prompt

def build_Q5b_prompt(answer):
    q5b_list = [
        "computed tomography angiography of pulmonary arteries with contrast",
        "high probability nuclear medicine V/Q scan",
        "Magnetic Resonsance Imaging (MRI) of pulmonary arteries",
        "pulmonary angiography",
        "post-mortem exam finding that PE likely contributed to death",
        "moderate probability V/Q scan"
    ]
    if answer == "yes":
        num_to_select = random.randint(1, len(q5b_list))
        test_list = random.sample(q5b_list, num_to_select)
        test_list_str = ", ".join(test_list)
        Q5b_prompt = f"The diagnostic test(s) that confirmed the pulmonary embolism are: {test_list_str}"
    else:
        q5b_list_str = ", ".join(q5b_list)
        Q5b_prompt = f"The record should state that none of the following diagnostic tests were run to confirm the pulmonary embolism: {q5b_list_str}"
    return Q5b_prompt

def build_Q6_prompt(answer):
    q6_list = [
        "shortness of breath",
        "pleuritic chest pain",
        "hemoptysis",
        "oxygen desaturation",
        "death"
    ]
    if answer == "yes":
        num_to_select = random.randint(1, len(q6_list))
        symptom_list = random.sample(q6_list, num_to_select)
        symptom_list_str = ", ".join(symptom_list)
        Q6_prompt = f"The following symptoms should be noted in the medical record as appearing more than 48 hours after admission: {symptom_list_str}."
    else:
        all_symptom_list_str = ", ".join(q6_list)
        Q6_prompt = f"The medical record should not note any of the following symptoms: {all_symptom_list_str}."
    return Q6_prompt

def build_Q6a_prompt(answer):
    if answer == "yes":
        Q6a_prompt = "The record should note that comfort care HAD been ordered for the patient during the stay, BEFORE the pulmonary embolism occurred."
    else:
        Q6a_prompt = "The record should note that comfort care HAD NOT been ordered for the patient during the stay, BEFORE the pulmonary embolism occurred."
    return Q6a_prompt

def build_R5_prompt(answer):
    if answer == "yes":
        R5_prompt = "The record should note that the patient underwent an operating room procedure during the stay (and provide details about the type of procedure)."
    else:
        R5_prompt = "The record should make no mention of any operating room procedures occurring during the stay."
    return R5_prompt

# Q7 is non-branching; "yes" answer in dict is a placeholder only
def build_Q7_prompt():
    q7_list = [
        "before any operating room procedures",
        "after an operating room procedure",
    ]
    rand_insert = random.choice(q7_list)
    Q7_prompt = f"The record should state that the patient developed the venous thromboembolism {rand_insert}."
    return Q7_prompt

def build_R6_prompt(answer):
    if answer == "yes":
        R6_prompt = "The record should note that the patient had a central venous catheter."
    else:
        R6_prompt = "Ther record should make no mention of a central venous catheter."
    return R6_prompt

# Q8 is non-branching; yes answer in dicts is a placeholder only.
def build_Q8_prompt():
    q8_list = [
        "WAS",
        "WAS NOT"
    ]
    rand_insert = random.choice(q8_list)
    Q8_prompt = f"The central venous catheter {rand_insert} in place at the time of the venous thromboembolism."
    return Q8_prompt

def build_Q9_prompt():
    q9_list = [
        "SHOULD",
        "SHOULD NOT"
    ]
    rand_insert = random.choice(q9_list)
    Q9_prompt = f"The record {rand_insert} say that deep vein thromboembolism is clearly associated with the central venous catheter."
    return Q9_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(story_number, algo_str):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(vte_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(vte_prompt_qa_dict.keys())
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
    question_keys = list(vte_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQ1" in question_keys:
        ans = vte_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = vte_prompt_qa_dict[num]["EQ2"]
        eq2_prompt = build_EQ2_prompt(ans)
        list_of_prompts.append(eq2_prompt)
    # might update patient age
    if "EQR1" in question_keys:
        ans = vte_prompt_qa_dict[num]["EQR1"]
        eqr1_prompt, patient_age = build_EQR1_prompt(ans, patient_age)
        list_of_prompts.append(eqr1_prompt)
    if "EQ4" in question_keys:
        ans = vte_prompt_qa_dict[num]["EQ4"]
        eq4_prompt = build_EQ4_prompt(ans)
        list_of_prompts.append(eq4_prompt)
    if "EQ5" in question_keys:
        eq5_prompt = build_EQ5_prompt()
        list_of_prompts.append(eq5_prompt)
    if "EQ6" in question_keys:
        ans = vte_prompt_qa_dict[num]["EQ6"]
        eq6_prompt = build_EQ6_prompt(ans)
        list_of_prompts.append(eq6_prompt)
    if "EQ7" in question_keys:
        ans = vte_prompt_qa_dict[num]["EQ7"]
        eq7_prompt = build_EQ7_prompt(ans)
        list_of_prompts.append(eq7_prompt)
    if "Q2" in question_keys:
        ans = vte_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        ans = vte_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q3a" in question_keys:
        ans = vte_prompt_qa_dict[num]["Q3a"]
        q3a_prompt = build_Q3a_prompt(ans)
        list_of_prompts.append(q3a_prompt)
    if "Q4" in question_keys:
        ans = vte_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "Q5a" in question_keys:
        ans = vte_prompt_qa_dict[num]["Q5a"]
        q5a_prompt = build_Q5a_prompt(ans)
        list_of_prompts.append(q5a_prompt)
    if "Q5b" in question_keys:
        ans = vte_prompt_qa_dict[num]["Q5b"]
        q5b_prompt = build_Q5b_prompt(ans)
        list_of_prompts.append(q5b_prompt)
    if "Q6" in question_keys:
        ans = vte_prompt_qa_dict[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans)
        list_of_prompts.append(q6_prompt)
    if "Q6a" in question_keys:
        ans = vte_prompt_qa_dict[num]["Q6a"]
        q6a_prompt = build_Q6a_prompt(ans)
        list_of_prompts.append(q6a_prompt)
    if "R5" in question_keys:
        ans = vte_prompt_qa_dict[num]["R5"]
        r5_prompt = build_R5_prompt(ans)
        list_of_prompts.append(r5_prompt)
    if "Q7" in question_keys:
        q7_prompt = build_Q7_prompt()
        list_of_prompts.append(q7_prompt)
    if "R6" in question_keys:
        ans = vte_prompt_qa_dict[num]["R6"]
        r6_prompt = build_R6_prompt(ans)
        list_of_prompts.append(r6_prompt)
    if "Q8" in question_keys:
        q8_prompt = build_Q8_prompt()
        list_of_prompts.append(q8_prompt)
    if "Q9" in question_keys:
        q9_prompt = build_Q9_prompt()
        list_of_prompts.append(q9_prompt)
    
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