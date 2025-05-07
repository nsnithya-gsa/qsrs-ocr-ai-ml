import random
from typing import List, Tuple

def return_days_inside_3_day_window(window_center_day: int, discharge_day: int) -> List[int]:
    """Given the day number at the center of a 3-day window and the current discharge day,
    returns all possible days within that 3-day window that still fit within the patient stay

    Args:
        window_center_day (int): day number of event at the center of the window
        discharge_day (int): current discharge day before the function is called

    Returns:
        List[int]: list of all day numbers that can be chosen bc they're within the 3 day 
        window and the patient's stay
    """
    # first day in window is 3 days before event OR admission day, whichever comes last
    earliest_possible_day = max(1, window_center_day - 3)

    # last day in window is 3 days after event OR discharge day, whichever comes first
    latest_possible_day = min(window_center_day + 3, discharge_day)

    # range collects consecutive numbers from first number to last number-1 
    possible_findings_days = list(range(earliest_possible_day, latest_possible_day + 1))
    return possible_findings_days



def get_days_outside_3_day_window(window_center_day: int, discharge_day: int) -> Tuple[List[int], int]:
    """Given the day number at the center of a 3-day window and the current discharge day,
    returns all possible days outside that 3-day window that still fit within the patient stay
    AND ALSO the discharge day, which might be increased -
    If the patient stay is too short (so all patient stay days are inside the 3-day window), 
    the discharge day will be increased (with some randomization of up to 5 extra days) to 
    ensure that there's at least one day outside the 3-day window

    Args:
        window_center_day (int): day number of event at the center of the window
        discharge_day (int): current discharge day before the function is called

    Returns:
        Tuple[List[int], int]: first return variable is a list of all day numbers that can be 
        chosen bc they're outside the 3 day window, second return variable is the (possibly larger)
        discharge day. After calling this function, we must check to see if externally-stored value of
        discharge day needs to be updated to match.
    """
    dis_day = discharge_day

    # if event is very early in stay, the window includes admission (day 1)
    if window_center_day < 5:
        # findings must happen after window but before discharge
        last_window_day = window_center_day + 3
        
        # make sure there are days in stay after window
        if last_window_day >= discharge_day:
            min_extra_days_needed = last_window_day - discharge_day + 1
            # lengthen stay by increasing discharge day number
            dis_day = discharge_day + random.randint(min_extra_days_needed, min_extra_days_needed + 5)

        possible_findings_days = list(range(last_window_day + 1, dis_day + 1))

    else:
        # collect day numbers in stay before the 3-day window
        left_of_window_days = list(range(1, window_center_day - 3))

        # collect day numbers in stay after the 3-day window
        right_of_window_days = list(range(window_center_day + 4, (dis_day + 1)))

        # choose a random day from the combined list of possible outside-of-window days in stay
        possible_findings_days = left_of_window_days + right_of_window_days

    return possible_findings_days, dis_day

def multiple_choice_question(answer: str, choice_type: str, choice_list: List[str]) -> str:
    """Given the answer to a multiple choice question (which may be "none", a phrase to make 
    the generic prompt fit the specific situation, and the list of possible choices (phrases),
    returns an appropriate, randomized prompt. Example: given answer = "none", choice_type is = "infection symptoms",
    choice_list = ["fever", "redness", "swelling"], returned value will be "The medical record should not mention 
    any of the following infection symptoms: fever, redness, swelling." If the answer is not "none",
    the function will choose a random NON-ZERO number of items from the list and build a prompt like this: 
    "The medical record should note the following infection symptoms: redness, swelling"

    Args:
        answer (str): "none" or "yes", the desired answer to an algorithm question
        choice_type (str): short phrase as described above
        choice_list (List[str]): list of all possible multiple choice answers

    Returns:
        str: the complete prompt based on the parameters as described above
    """
    if answer == "none":
        choices_together = ", ".join(choice_list)
        prompt = f"The medical record should not mention any of the following {choice_type}: {choices_together}."
    else:
        num_to_select = random.randint(1, len(choice_list))
        selected_elements = random.sample(choice_list, num_to_select)
        elements_together = ", ".join(selected_elements)
        prompt = f"The medical record should note the following {choice_type}: {elements_together}."
    return prompt

# this is used for file naming
algo_str = "birth_neonatal"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.

birth_neonatal_prompt_qa_dict = {}

birth_neonatal_prompt_qa_dict[1] = {
    "EQR1": "no"
}

birth_neonatal_prompt_qa_dict[2] = {
    "EQR1": "yes",
    "EQ1": "no"
}

birth_neonatal_prompt_qa_dict[3] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "Q3": "none",
    "R2": "yes"
}

birth_neonatal_prompt_qa_dict[4] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "R2": "no",
    "R2a": "no"
}

birth_neonatal_prompt_qa_dict[5] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "R2": "yes",
    "Q4": "no",
    "R2a": "no"
}

birth_neonatal_prompt_qa_dict[6] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "R2": "yes",
    "Q4": "yes",
    "R2a": "yes",
    "Q5": "no"
}

birth_neonatal_prompt_qa_dict[7] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "R2": "yes",
    "Q4": "yes",
    "R2a": "yes",
    "Q5": "yes",
    "R3": "no"
}

birth_neonatal_prompt_qa_dict[8] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "R2": "yes",
    "Q4": "yes",
    "R2a": "yes",
    "Q5": "yes",
    "R3": "yes",
    "Q6": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "Q9": "no",
    "R4": "none"
}

birth_neonatal_prompt_qa_dict[9] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "R2": "yes",
    "Q4": "yes",
    "R2a": "yes",
    "Q5": "yes",
    "R3": "yes",
    "Q6": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "Q9": "yes",
    "Q10": "none",
    "R4": "none"
}

birth_neonatal_prompt_qa_dict[10] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "Q3": "yes",
    "R2": "yes",
    "Q4": "yes",
    "R2a": "yes",
    "Q5": "yes",
    "R3": "yes",
    "Q6": "yes",
    "Q7": "yes",
    "Q8": "yes",
    "Q9": "yes",
    "Q10": "yes",
    "R4": "none"
}

def build_EQR1_prompt(answer, patient_age, age_type):
    if answer == "yes":
        patient_age = random.randint(1,28)
        age_type = "days"
        EQR1_prompt = f"The patient is a neonate, {patient_age} days old."
    else:
        EQR1_prompt = "The patient is not a neonatal age."
    return EQR1_prompt, patient_age, age_type

def build_EQ1_prompt(answer):
    if answer == "yes":
        EQ1_prompt = f"The patient was born during this hospital stay."
    else:
        EQ1_prompt = f"The patient was not born inside the hospital. "
    return EQ1_prompt

def build_Q1_prompt():
    apgar = random.randint(1, 10)  # Random APGAR score
    return apgar

def build_Q2_prompt():
  birthweight_kgs = round(random.uniform(1.0, 4.5), 2)
  return birthweight_kgs

def build_Q3_prompt(answer):
    neonate_diagnoses = [
        "Seizure",
        "Anoxic or Hypoxic-Ischemic Encephalopathy",
        "Infection",
        "Subdural or cerebral hemorrhage",
        "Injury to brachial plexus, Erb's paralysis or Klumpke's paralysis",
        "Abduction of a neonate",
        "Massive aspiration syndrome or meconium aspiration syndrome",
        "Severe hyperbilirubinemia (bilirubin > 30 mg/dl)",
        "Other birth injury",
    ]

    Q3_prompt = multiple_choice_question(answer, "neonate outcomes", neonate_diagnoses)
    
    return Q3_prompt


def build_R2_prompt(answer):
    if answer == "yes":
        R2_prompt = f"The neonate suffered from a seizure."
    else:
        R2_prompt = f"There is no mention of a seizure episode ocurring with the patient."
    return R2_prompt

def build_Q4_prompt(answer):
    if answer == "yes":
        reasons_list = [
            "withdrawal symptoms",
            "drug reactions",
            "diagnosis of fetal alcohol syndrome"
        ]
        reason_choice = random.choice(reasons_list)
        Q4_prompt = f"The seizure episode was related to {reason_choice}."
    else:
        Q4_prompt = f"The seizure had no relation to withdrawal symptoms, drug reactions, or diagnosis of fetal alcohol syndrome. There is no mention of these causes in the chart."
    return Q4_prompt

def build_R2a_prompt(answer):
    if answer == "yes":
        R2a_prompt = f"The patient's discharge status was death, or died."
    else:
        R2a_prompt = f"The patient's discharge status was living."
    return R2a_prompt

def build_Q5_prompt(answer):
    if answer == "yes":
        death_reason = [
            "neonate extreme encephaly with no expectation of survival", 
            "neonate had terminal Hypoplastic Left Heart Syndrome (HLHS) incompatible with life hence comfort care measure initiated"]
        death_reasons = random.choice(death_reason)
        Q5_prompt = f"The death was expected as determined by a physician's note explicitly noted in the medical record. The death reason was noted as: {death_reasons}. "
    else:
        Q5_prompt = f"The death was unrelated to labor, and instead happened after labor and delivery had already been completed."
    return Q5_prompt

def build_R3_prompt(answer, apgar, birthweight_kgs):
    """ If answer is 'yes', force APGAR <7 and weight >2.5kg.
        If 'no', do the opposite: APGAR >=7 and weight ≤2.5kg.
    """
    if answer == "yes":
        apgar = random.randint(1, 6)  # Force APGAR < 7
        birthweight_kgs = round(random.uniform(2.6, 4.5), 2)  # Force weight > 2.5kg
        R3_prompt = (f"For this scenario, the APGAR score is {apgar}, "
                     f"and the neonate's birthweight is {birthweight_kgs} kg.")
    else:
        apgar = random.randint(7, 10)  # Force APGAR >= 7
        birthweight_kgs = round(random.uniform(1.0, 2.5), 2)  # Force weight ≤ 2.5kg
        R3_prompt = (f"For this scenario, the APGAR score is {apgar}, "
                     f"and the neonate's birthweight is {birthweight_kgs} kg.")
    
    return R3_prompt, apgar, birthweight_kgs  # Return updated values


def build_Q6_prompt():
    est_gest = random.randint(34,41)
    Q6_prompt = f"The patient's estimated gestational age in weeks at time of delivery was {est_gest} weeks."
    return Q6_prompt

def build_Q7_prompt():
    fetuses = random.randint(1,3)
    Q7_prompt = f"There were {fetuses} fetuses in the pregnancy."
    return Q7_prompt

def build_Q8_prompt():
    previous_births = random.randint(1,4)
    prompt_list = [
        f"This neonate was the mother's first delivery.",
        f"The mother had {previous_births} live births before this neonate was delivered."
    ]
    Q8_prompt = random.choice(prompt_list)
    return Q8_prompt

def build_Q9_prompt(answer):
    list_for_Q9 = [
        "vaginal delivery",
        "attempted vaginal delivery followed by Cesarean section"
    ]
    if answer == "yes":
        delivery = random.choice(list_for_Q9)
        Q9_prompt = f"The neonate was delivered via {delivery}."
    else:
        Q9_prompt = f"The neonate was delivered by scheduled cesarean section without attempted vaginal delivery."
    return Q9_prompt

def build_Q10_prompt(answer):
    if answer == "yes":
        list_for_Q10 = [
            "vacuum",
            "forceps",
            "vacuum followed by forceps"
        ]
        instruments = random.choice(list_for_Q10)
        Q10_prompt = f"The patient was delivered with the instrument: {instruments}."
    else:
        Q10_prompt = f"There is no mention of instruments utilized during delivery."
    return Q10_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(birth_neonatal_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(birth_neonatal_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    patient_age = random.randint(1, 99)
    age_type = "years"
    apgar = -1
    birthweight_kgs = -1

    # create placeholders for variables that might get set / passed around between functions

    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(birth_neonatal_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQR1" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["EQR1"]
        eqr1_prompt, patient_age, age_type = build_EQR1_prompt(ans, patient_age, age_type)
        list_of_prompts.append(eqr1_prompt)
    if "EQ1" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "Q1" in question_keys:
        apgar = build_Q1_prompt()
    if "Q2" in question_keys:
        birthweight_kgs = build_Q2_prompt()
    if "Q3" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "R2" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["R2"]
        r2_prompt = build_R2_prompt(ans)
        list_of_prompts.append(r2_prompt)
    if "Q4" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "R2a" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["R2a"]
        r2a_prompt = build_R2a_prompt(ans)
        list_of_prompts.append(r2a_prompt)
    if "Q5" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
    if "R3" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["R3"]
        r3_prompt, apgar, birthweight_kgs = build_R3_prompt(ans, apgar, birthweight_kgs)
        list_of_prompts.append(r3_prompt)
    if "Q6" in question_keys:
        q6_prompt = build_Q6_prompt()
        list_of_prompts.append(q6_prompt)
    if "Q7" in question_keys:
        q7_prompt = build_Q7_prompt()
        list_of_prompts.append(q7_prompt)
    if "Q8" in question_keys:
        q8_prompt = build_Q8_prompt()
        list_of_prompts.append(q8_prompt)
    if "Q9" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["Q9"]
        q9_prompt = build_Q9_prompt(ans)
        list_of_prompts.append(q9_prompt)
    if "Q10" in question_keys:
        ans = birth_neonatal_prompt_qa_dict[num]["Q10"]
        q10_prompt = build_Q10_prompt(ans)
        list_of_prompts.append(q10_prompt)
    #######


    # after all build prompt functions that should be called are, add general prompts about the stay that might
    # not have been stated yet (remove duplicates at the end)
    if apgar > -1:
        list_of_prompts.append(f"The patient's apgar score was {apgar}.")
    if birthweight_kgs > -1:
        list_of_prompts.append(f"The patient's birthweight was {birthweight_kgs} kilograms.")
    list_of_prompts.append(f"Patient is {patient_age} {age_type} old.")
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