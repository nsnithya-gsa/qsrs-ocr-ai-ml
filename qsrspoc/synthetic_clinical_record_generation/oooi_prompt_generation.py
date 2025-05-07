import random
from typing import List, Tuple

oooi_prompt_qa_dict = {}

oooi_prompt_qa_dict[1] = {
    "Q1": "no",
    "Q7": "none"
}

oooi_prompt_qa_dict[2] = {
    "Q1": "yes",
    "Q2": "incorrect",
    "Q3": "yes",
    "Q4": "yes",
    "Q5": "no",
    "RL1": "yes",
    "Q6": "yes",
    "Q6a": "yes",
    "L2a": "yes",
    "Q6b": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "RL2": "above-2-under-5",
    "Q9": "yes",
    "RL3": "yes",
    "RL5": "less-than-five",
    "Q10": "yes",
    "RL4": "yes",
    "RL6": "yes",
    "Q11": "yes",
    "Q12": "yes",
    "Q13": "yes",
    "Q13a": "yes",
    "RL7": "yes", # RL6 is duplicated in flowchart: RL7 is key for 2nd question (ventilator)
    "RL8": "yes",
    "Q14": "yes",
    "Q15": "yes",
    "Q15a": "yes",
    "RL11": "yes",
    "Q15b": "yes",
    "RL15": "yes",
    "Q16": "yes",
    "Q17a": "yes",
    "RL9": "yes",
    "Q18": "yes",
    "Q19": "yes",
    "Q20": "yes",
    "RL16": "yes",
    "Q21": "yes",
    "Q17b": "yes",
    "Q23a": "yes",
    "Q24": "yes",
    "Q24a": "yes",
    "RL12": "yes",
    "Q24b": "yes",
    "Q25": "yes",
    "RL13": "yes",
    "Q26": "yes",
    "Q27": "yes",
    "RL14": "yes",
    "Q28": "yes",
    "Q29": "yes"
}

oooi_prompt_qa_dict[3] = {
    "Q1": "yes",
    "Q2": "incorrect",
    "Q3": "yes",
    "Q4": "no",
    "RL1": "no",
    "Q6": "yes",
    "Q6a": "no",
    "Q7": "no"
}

oooi_prompt_qa_dict[4] = {
    "Q1": "yes",
    "Q2": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "RL1": "yes",
    "Q6": "yes",
    "Q6a": "yes",
    "L2a": "no",
    "Q7": "no"
}

oooi_prompt_qa_dict[5] = {
    "Q1": "yes",
    "Q2": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "RL1": "yes",
    "Q6": "yes",
    "Q6a": "yes",
    "L2a": "yes",
    "Q6b": "no",
    "Q7": "no"
}

oooi_prompt_qa_dict[6] = {
    "Q1": "yes",
    "Q2": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "RL1": "yes",
    "Q6": "yes",
    "Q6a": "yes",
    "L2a": "yes",
    "Q6b": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "RL2": "no",
    "RL6": "no"
}

oooi_prompt_qa_dict[7] = {
    "Q1": "yes",
    "Q2": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "RL1": "yes",
    "Q6": "yes",
    "Q6a": "yes",
    "L2a": "yes",
    "Q6b": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "RL2": "yes",
    "Q9": "yes",
    "RL3": "no",
    "RL6": "no"
}

oooi_prompt_qa_dict[8] = {
    "Q1": "yes",
    "Q2": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "RL1": "yes",
    "Q6": "yes",
    "Q6a": "yes",
    "L2a": "yes",
    "Q6b": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "RL2": "above-2-above-5",
    "Q9": "yes",
    "RL3": "yes",
    "RL5": "above-5",
    "RL6": "no"
}

oooi_prompt_qa_dict[9] = {
    "Q1": "yes",
    "Q2": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "RL1": "yes",
    "Q6": "yes",
    "Q6a": "yes",
    "L2a": "yes",
    "Q6b": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "RL2": "above-2-under-5",
    "Q9": "yes",
    "RL3": "yes",
    "RL5": "above-5",
    "Q10": "yes",
    "RL4": "no",
    "RL6": "no"
}

oooi_prompt_qa_dict[10] = {
    "Q1": "yes",
    "Q2": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "RL1": "yes",
    "Q6": "yes",
    "Q6a": "yes",
    "L2a": "yes",
    "Q6b": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "RL2": "above-2-under-5",
    "Q9": "yes",
    "RL3": "yes",
    "RL5": "above-5",
    "Q10": "yes",
    "RL4": "yes",
    "RL6": "no",
    "Q11": "no",
    "Q13": "no",
    "RL7": "no",
    "Q15": "yes",
    "Q15a": "yes",
    "RL11": "yes",
    "Q15b": "no",
    "RL15": "yes",
    "Q16": "no",
    "Q19": "no",
    "Q20": "no",
    "RL16": "yes",
    "Q21": "no",
    "Q24": "no",
    "Q25": "no",
    "Q27": "no",
    "Q29": "no"
}

def build_Q1_prompt(answer):
    if answer == "yes":
        Q1_prompt = "The patient underwent a non-operating room invasive procedure (not a caesarean section)."
    else:
        Q1_prompt = "The record should make no mention of non-operating room invasive procedures as part of the patient's stay."
    return Q1_prompt

def build_Q2_prompt(answer):
    yes_list = [
        "an unintended iatrogenic pneumothorax",
        "a laceration",
        "an unintended puncture"
    ]
    if answer == "incorrect":
        Q2_prompt = "The record must note that the patient underwent an incorrect non-operating room procedure."
    if answer == "yes":
        rand_unintended = random.choice(yes_list)
        Q2_prompt = f"The record must note that the patient experienced {rand_unintended} as part of their stay."
    else: # none
        yes_list.append("an incorrect non-operating room procedure")
        none_str = ", ".join(yes_list)
        Q2_prompt = f"The record must not mention any of the following happening during the patient's stay: {none_str}."
    return Q2_prompt

def build_Q3_prompt():
    wrong_proc_list = [
            "an incorrect procedure (includes procedure done when none ordered)",
            "an incorrect side",
            "an incorrect site"
        ]
    rand_wrong = random.choice(wrong_proc_list)
    Q3_prompt = f"The patient's incorrect non-operating room procedure involved {rand_wrong}."
    return Q3_prompt

def build_Q4_prompt(answer):
    if answer == "yes":
        Q4_prompt = "During the stay, the patient underwent an arterial puncture."
    else:
        Q4_prompt = "The record must not mention an arterial puncture as part of the patient's stay."
    return Q4_prompt

def build_Q5_prompt(answer):
    if answer == "yes":
        Q5_prompt = "The patient DID experience an adverse event as the result of the arterial puncture."
    else:
        Q5_prompt = "The patient DID NOT experience an adverse event as the result of the arterial puncture."
    return Q5_prompt

def build_RL1_prompt(answer):
    if answer == "yes":
        RL1_prompt = "The record must note that the patient had a central venous catheter (CVC) inserted during their stay."
    else:
        RL1_prompt = "The record must not mention a central venous catheter (CVC) as part of the stay."
    return RL1_prompt

def build_Q6_prompt(answer):
    if answer == "yes":
        Q6_prompt = "The record must note that the patient experienced a mechanical adverse event during their stay as the result of the central venous catheter."
    else:
        Q6_prompt = "The record must not mention the patient experiencing any mechanical adverse event as the result of the central venous catheter during their stay."
    return Q6_prompt

def build_Q6a_prompt(answer):
    if answer == "yes":
        Q6a_prompt = "The record must note that during the stay, the patient sustained an intravascular air embolism."
    else:
        Q6a_prompt = "The record must NOT note that during the stay, the patient sustained an intravascular air embolism."
    return Q6a_prompt

def build_L2a_prompt(answer):
    if answer == "yes":
        L2a_prompt = "The record must list the patient's discharge status as death. The patient died during the stay."
    else:
        L2a_prompt = "The record must NOT list the patient's discharge status as death. The patient did not die during the stay."
    return L2a_prompt

def build_Q6b_prompt(answer):
    if answer == "yes":
        Q6b_prompt = "The record must note that the patient's death is attributed to intravascular air embolism."
    else:
        Q6b_prompt = "The record MUST NOT note that the patient's death is attributed to intravascular air embolism."
    return Q6b_prompt

def build_Q7_prompt(answer):
    if answer == "yes":
        Q7_prompt = "The record must note that a serum creatinine was performed during the stay."
    else:
        Q7_prompt = "The record must not mention any serum creatinine being measured as part of the stay."
    return Q7_prompt

# in the current dict, Q8 is always followed by RL2, which currently determines the answer to Q8
def build_Q8_prompt():
    Q8_prompt = ""
    return Q8_prompt

# This has complex possible answers in story dict to account for RL5 requirements
def build_RL2_prompt(answer):
    if answer == "above-2-under-5":
        rand_level = round(random.uniform(2.1, 4.9), 1)
    if answer == "above-2-above-5":
        rand_level = round(random.uniform(5.0, 10.0), 1)
    if answer == "yes": # above 2, no ceiling
        rand_level = round(random.uniform(2.1, 3.0), 1)
    else: # <= 2.0
        rand_level = round(random.uniform(0.4, 2.0), 1)
    RL2_prompt = f"The record must state that after the first 24 hours of admission, the highest serum creatinine was {rand_level}."
    return RL2_prompt

# currently a placeholder; RL3's answer determines this value
def build_Q9_prompt():
    Q9_prompt = ""
    return Q9_prompt

def build_RL3_prompt(answer):
    if answer == "yes": # <= 2.0
        rand_level = round(random.uniform(0.4, 2.0), 1)
    else: # >2.0
        rand_level = round(random.uniform(2.1, 10.0), 1)
    RL3_prompt = f"The record must state that during the first 24 hours of admission, the highest serum creatinine was {rand_level}."
    return RL3_prompt

# This is already covered by RL2's fancy answers based on the current story definitions
def build_RL5_prompt():
    RL5_prompt = ""
    return RL5_prompt

# currently a placeholder; the answer for RL4 determines this
def build_Q10_prompt():
    Q10_prompt = ""
    return Q10_prompt

# Was the last reported serum creatinine (mg/dL) prior to discharge greater than 2.0?
def build_RL4_prompt(answer):
    if answer == "yes":
        rand_level = round(random.uniform(2.1, 10.0), 1)
    else:
        rand_level = round(random.uniform(0.4, 2.0), 1)
    RL4_prompt = f"The record must clearly state that the last reported serum creatinine (mg/dL) prior to discharge was {rand_level}."
    return RL4_prompt

# Is the patient less than 18 years old? NOTE: RL15 checks if patient is at least 5 yo, RL16 CHECKS IF PATIENT > 2
# No current stories have conflicting answer combinations to these 3 age checks.
# story 2: < 18, over 5, over 2 
# story 10: >18, over 5, over 2
def build_RL6_prompt(answer):
    if answer == "yes":
        age = random.randint(6, 17)
    else:
        age = random.randint(19, 99)
    RL6_prompt = f"The patient is {age} years old."
    return RL6_prompt, age

def build_Q11_prompt(answer):
    if answer == "yes":
        Q11_prompt = "The record must note that the patient had a seizure during the stay."
    else:
         Q11_prompt = "The record must not mention the patient having any seizures."
    return Q11_prompt

def build_Q12_prompt():
    insert_list = [
        "did",
        "did not"
    ]
    rand_insert = random.choice(insert_list)
    Q12_prompt = f"The record must note that the patient {rand_insert} have a prior history of seizure disorder."
    return Q12_prompt

def build_Q13_prompt(answer):
    if answer == "yes":
        Q13_prompt = "The record must note that the patient underwent an unplanned transfer to a higher level care area."
    else:
        Q13_prompt = "The record must not mention the patient being transferred at all."
    return Q13_prompt

def build_Q13a_prompt():
    transfer_list = [
        "within the facility",
        "to another facility"
    ]
    transfer_type = random.choice(transfer_list)
    Q13a_prompt = f"The record must note that the unplanned transfer for a higher level of care was {transfer_type}."
    return Q13a_prompt

# Was ventilator support initiated after the first 24 hours?
def build_RL7_prompt(answer):
    if answer == "yes":
        RL7_prompt = "The record must note that ventilator support was initiated after the first 24 hours."
    else:
        RL7_prompt = "The record must not mention any use of ventilator support."
    return RL7_prompt

def build_RL8_prompt(answer):
    if answer == "yes":
        RL8_prompt = "The patient had an operating room procedure during their stay."
    else:
        RL8_prompt = "The record must not mention any operating room procedures during the patient's stay."
    return RL8_prompt

def build_Q14_prompt(answer):
    if answer == "yes":
        Q14_prompt = "The record must specify that the ventilator support was initiated prior to the operating room procedure."
    else:
        Q14_prompt = "The record must specify that the ventilator support was initiated after the operating room procedure."
    return Q14_prompt

# currently a placeholder; Q15a covers the information for this question fully
def build_Q15_prompt():
    Q15_prompt = ""
    return Q15_prompt

def build_Q15a_prompt():
    q15_list = [
        "a burn injury",
        "an electric shock"
    ]
    rand_insert = random.choice(q15_list)
    Q15a_prompt = f"The record must note that the patient experienced {rand_insert} during their stay, outside of the operating room."
    return Q15a_prompt

# L2a, RL11, RL9, RL12, RL13, RL14 all ask if discharge status is death; no current stories hold contradictory answers
def build_RL11_prompt(answer):
    if answer == "yes":
        RL11_prompt = "The record must list the patient's discharge status as death. The patient died during the stay."
    else:
        RL11_prompt = "The record must NOT list the patient's discharge status as death. The patient did not die during the stay."
    return RL11_prompt

def build_Q15b_prompt(answer):
    if answer == "yes":
        Q15b_prompt = "The record must state that the patient's death is attributed to the burn injury or electric shock just described."
    else:
        Q15b_prompt = "The record must not attribute the patient's death to burns or electric shock sustained during the styay."
    return Q15b_prompt

# is the patient at least 5 years old?
# placeholder; age is handled by RL6 before this prompt is ever reached
def build_RL15_prompt():
    RL15_prompt = ""
    return RL15_prompt

def build_Q16_prompt(answer):
    if answer == "yes":
        Q16_prompt = "The record must note that the patient had an attempted suicide during their stay."
    else:
        Q16_prompt = "The record must make no mention of the patient having any suicide attempts."
    return Q16_prompt

def build_Q17a_prompt():
    insert_list = [
        "did",
        "did not"
    ]
    rand_insert = random.choice(insert_list)
    Q17a_prompt = f"The record must state that the patient {rand_insert} have a documented mental health condition on admission."
    return Q17a_prompt

def build_RL9_prompt(answer):
    if answer == "yes":
        RL9_prompt = "The record must list the patient's discharge status as death. The patient died during the stay."
    else:
        RL9_prompt = "The record must NOT list the patient's discharge status as death. The patient did not die during the stay."
    return RL9_prompt

def build_Q18_prompt():
    insert_list = [
        "did",
        "did not"
    ]
    rand_insert = random.choice(insert_list)
    Q18_prompt = f"The record must state that the patient {rand_insert} die from the suicide attempt."
    return Q18_prompt

def build_Q19_prompt(answer):
    if answer == "yes":
        Q19_prompt = "The patient sustained an injury during their stay associated with the use of physical restraints during their stay."
    else:
        Q19_prompt = "The record should not mention use of restraints on the patient during their stay."
    return Q19_prompt

def build_Q20_prompt(answer):
    if answer == "yes":
        Q20_prompt = "The patient sustained an injury during the stay associated with the use of bed rails."
    else:
        Q20_prompt = "The record should not mention bed rails at all."
    return Q20_prompt

# is the patient greater than 2 years old?
# placeholder; patient's age is always already established by this point in a non-contradictory way
def build_RL16_prompt():
    RL16_prompt = ""
    return RL16_prompt

def build_Q21_prompt(answer):
    if answer == "yes":
        Q21_prompt = f"The patient did elope during their stay."
    else:
        Q21_prompt = f"The patient did not elope during their stay."
    return Q21_prompt

# This is a repeat of Q17a, which is currently part of all stories that include Q17b
def build_Q17b_prompt():
    Q17b_prompt = ""
    return Q17b_prompt

def build_Q23a_prompt():
    prompt_list = [
        "The patient's documented elopement was from a locked mental health facility they were in during their stay.",
        "The record should not include information that the patient's stay was inside a locked mental health facility or space of any kind."
    ]
    Q23a_prompt = random.choice(prompt_list)
    return Q23a_prompt

def build_Q24_prompt(answer):
    if answer == "yes":
        Q24_prompt = "The record must note that the patient sustained harm due to radiology or imaging study during their stay."
    else:
        Q24_prompt = "There should be no mention in the record of harm sustained by the patient due to radiology or imaging during their stay."
    return Q24_prompt

def build_Q24a_prompt():
    event_list = [
        "radiation overdose",
        "radiological procedure on wrong person or wrong body region",
        "incident related to introduction of an inappropriate metallic object in MRI room"
    ]
    rand_event = random.choice(event_list)
    Q24a_prompt = f"The harm sustained by the patient due to this radiology or imaging study during ther stay was {rand_event}."
    return Q24a_prompt

def build_RL12_prompt(answer):
    if answer == "yes":
        RL12_prompt = "The record must list the patient's discharge status as death. The patient died during the stay."
    else:
        RL12_prompt = "The record must NOT list the patient's discharge status as death. The patient did not die during the stay."
    return RL12_prompt

def build_Q24b_prompt():
    insert_list = [
        "must",
        "must not"
    ]
    rand_insert = random.choice(insert_list)
    Q24b_prompt = f"The record {rand_insert} state that the patient's death is attributed to the adverse event from this radiology or imaging study."
    return Q24b_prompt

def build_Q25_prompt(answer):
    if answer == "yes":
        Q25_prompt = "The record must note that the patient sustained harm related to an irretrievable loss of an irreplacable biological specimen."
    else:
        Q25_prompt = "The record must not mention anything about loss of a biological specimen of any kind."
    return Q25_prompt

def build_RL13_prompt(answer):
    if answer == "yes":
        RL13_prompt = "The record must list the patient's discharge status as death. The patient died during the stay."
    else:
        RL13_prompt = "The record must NOT list the patient's discharge status as death. The patient did not die during the stay."
    return RL13_prompt

def build_Q26_prompt():
    insert_list = [
        "must be",
        "must not be"
    ]
    rand_insert = random.choice(insert_list)
    Q26_prompt = f"In the record, the patient's death {rand_insert} attributed to the loss of the irreplaceable biological specimen."
    return Q26_prompt

def build_Q27_prompt(answer):
    if answer == "yes":
        Q27_prompt = "The patient sustained harm attributed in the record to failure to communicate laboratory, pathology, imaging or phsiologic test results."
    else:
        Q27_prompt = "The record should make no mention of any failure to communicate laboratory, pathology, imaging or phsiologic test results."
    return Q27_prompt

def build_RL14_prompt(answer):
    if answer == "yes":
        RL14_prompt = "The record must list the patient's discharge status as death. The patient died during the stay."
    else:
        RL14_prompt = "The record must NOT list the patient's discharge status as death. The patient did not die during the stay."
    return RL14_prompt

def build_Q28_prompt():
    insert_list = [
        "must be",
        "must not be"
    ]
    rand_insert = random.choice(insert_list)
    Q28_prompt = f"In the record, the patient's death {rand_insert} attributed to the failure to communicate laboratory, pathology, imaging or phsiologic test results."
    return Q28_prompt

def build_Q29_prompt(answer):
    insert_list = [
            "the wrong gas",
            "no gas",
            "contaminated gas"
        ]
    if answer == "yes":
        rand_insert = random.choice(insert_list)
        Q29_prompt = f"The record must note that the patient sustained harm related to the delivery of {rand_insert} during their stay."
    else:
        all_options_str = ", ".join(insert_list)
        Q29_prompt = f"The record must not make any mention of the delivery of {all_options_str} happening during the patient's stay."
    return Q29_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(oooi_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(oooi_prompt_qa_dict.keys())
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
    question_keys = list(oooi_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "Q1" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q2" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        q3_prompt = build_Q3_prompt()
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "Q5" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
    if "RL1" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL1"]
        rl1_prompt = build_RL1_prompt(ans)
        list_of_prompts.append(rl1_prompt)
    if "Q6" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans)
        list_of_prompts.append(q6_prompt)
    if "Q6a" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q6a"]
        q6a_prompt = build_Q6a_prompt(ans)
        list_of_prompts.append(q6a_prompt)
    if "L2a" in question_keys:
        ans = oooi_prompt_qa_dict[num]["L2a"]
        l2a_prompt = build_L2a_prompt(ans)
        list_of_prompts.append(l2a_prompt)
    if "Q6b" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q6b"]
        q6b_prompt = build_Q6b_prompt(ans)
        list_of_prompts.append(q6b_prompt)
    if "Q7" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q7"]
        q7_prompt = build_Q7_prompt(ans)
        list_of_prompts.append(q7_prompt)
    if "Q8" in question_keys:
        q8_prompt = build_Q8_prompt()
        list_of_prompts.append(q8_prompt)
    if "RL2" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL2"]
        rl2_prompt = build_RL2_prompt(ans)
        list_of_prompts.append(rl2_prompt)
    if "Q9" in question_keys:
        q9_prompt = build_Q9_prompt()
        list_of_prompts.append(q9_prompt)
    if "RL3" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL3"]
        rl3_prompt = build_RL3_prompt(ans)
        list_of_prompts.append(rl3_prompt)
    if "RL5" in question_keys:
        rl5_prompt = build_RL5_prompt()
        list_of_prompts.append(rl5_prompt)
    if "Q10" in question_keys:
        q10_prompt = build_Q10_prompt()
        list_of_prompts.append(q10_prompt)
    if "RL4" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL4"]
        rl4_prompt = build_RL4_prompt(ans)
        list_of_prompts.append(rl4_prompt)
    if "RL6" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL6"]
        rl6_prompt, patient_age = build_RL6_prompt(ans)
        list_of_prompts.append(rl6_prompt)
    if "Q11" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q11"]
        q11_prompt = build_Q11_prompt(ans)
        list_of_prompts.append(q11_prompt)
    if "Q12" in question_keys:
        q12_prompt = build_Q12_prompt()
        list_of_prompts.append(q12_prompt)
    if "Q13" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q13"]
        q13_prompt = build_Q13_prompt(ans)
        list_of_prompts.append(q13_prompt)
    if "Q13a" in question_keys:
        q13a_prompt = build_Q13a_prompt()
        list_of_prompts.append(q13a_prompt)
    if "RL7" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL7"]
        rl7_prompt = build_RL7_prompt(ans)
        list_of_prompts.append(rl7_prompt)
    if "RL8" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL8"]
        rl8_prompt = build_RL8_prompt(ans)
        list_of_prompts.append(rl8_prompt)
    if "Q14" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q14"]
        q14_prompt = build_Q14_prompt(ans)
        list_of_prompts.append(q14_prompt)
    if "Q15" in question_keys:
        q15_prompt = build_Q15_prompt()
        list_of_prompts.append(q15_prompt)
    if "Q15a" in question_keys:
        q15a_prompt = build_Q15a_prompt()
        list_of_prompts.append(q15a_prompt)
    if "RL11" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL11"]
        rl11_prompt = build_RL11_prompt(ans)
        list_of_prompts.append(rl11_prompt)
    if "Q15b" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q15b"]
        q15b_prompt = build_Q15b_prompt(ans)
        list_of_prompts.append(q15b_prompt)
    if "RL15" in question_keys:
        rl15_prompt = build_RL15_prompt()
        list_of_prompts.append(rl15_prompt)
    if "Q16" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q16"]
        q16_prompt = build_Q16_prompt(ans)
        list_of_prompts.append(q16_prompt)
    if "Q17a" in question_keys:
        q17a_prompt = build_Q17a_prompt()
        list_of_prompts.append(q17a_prompt)
    if "RL9" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL9"]
        rl9_prompt = build_RL9_prompt(ans)
        list_of_prompts.append(rl9_prompt)
    if "Q18" in question_keys:
        q18_prompt = build_Q18_prompt()
        list_of_prompts.append(q18_prompt)
    if "Q19" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q19"]
        q19_prompt = build_Q19_prompt(ans)
        list_of_prompts.append(q19_prompt)
    if "Q20" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q20"]
        q20_prompt = build_Q20_prompt(ans)
        list_of_prompts.append(q20_prompt)
    if "RL16" in question_keys:
        rl16_prompt = build_RL16_prompt()
        list_of_prompts.append(rl16_prompt)
    if "Q21" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q21"]
        q21_prompt = build_Q21_prompt(ans)
        list_of_prompts.append(q21_prompt)
    if "Q17b" in question_keys:
        q17b_prompt = build_Q17b_prompt()
        list_of_prompts.append(q17b_prompt)
    if "Q23a" in question_keys:
        q23a_prompt = build_Q23a_prompt()
        list_of_prompts.append(q23a_prompt)
    if "Q24" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q24"]
        q24_prompt = build_Q24_prompt(ans)
        list_of_prompts.append(q24_prompt)
    if "Q24a" in question_keys:
        q24a_prompt = build_Q24a_prompt()
        list_of_prompts.append(q24a_prompt)
    if "RL12" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL12"]
        rl12_prompt = build_RL12_prompt(ans)
        list_of_prompts.append(rl12_prompt)
    if "Q24b" in question_keys:
        q24b_prompt = build_Q24b_prompt()
        list_of_prompts.append(q24b_prompt)
    if "Q25" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q25"]
        q25_prompt = build_Q25_prompt(ans)
        list_of_prompts.append(q25_prompt)
    if "Q26" in question_keys:
        q26_prompt = build_Q26_prompt()
        list_of_prompts.append(q26_prompt)
    if "Q27" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q27"]
        q27_prompt = build_Q27_prompt(ans)
        list_of_prompts.append(q27_prompt)
    if "RL14" in question_keys:
        ans = oooi_prompt_qa_dict[num]["RL14"]
        rl14_prompt = build_RL14_prompt(ans)
        list_of_prompts.append(rl14_prompt)
    if "Q28" in question_keys:
        q28_prompt = build_Q28_prompt()
        list_of_prompts.append(q28_prompt)
    if "Q29" in question_keys:
        ans = oooi_prompt_qa_dict[num]["Q29"]
        q29_prompt = build_Q29_prompt(ans)
        list_of_prompts.append(q29_prompt)
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