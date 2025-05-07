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
algo_str = "device"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.


device_prompt_qa_dict = {}

device_prompt_qa_dict[1] = {
    "EQ1": "no"
}

device_prompt_qa_dict[2] = {
    "EQ1": "yes",
    "EQ2": "yes"
}

device_prompt_qa_dict[3] = {
    "EQ1": "yes",
    "EQ2": "no",
    "Q1": "hit",
    "Q2": "yes",
    "Q3": "yes",
    "Q4": "no",
    "Q5": "yes",
    "Q6": "yes"
}

device_prompt_qa_dict[4] = {
    "EQ1": "yes",
    "EQ2": "no",
    "Q1": "hit",
    "Q2": "yes",
    "Q3": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "Q6": "yes"
}

device_prompt_qa_dict[5] = {
    "EQ1": "yes",
    "EQ2": "no",
    "Q1": "yes",
    "Q3": "yes",
    "Q4": "no",
    "Q5": "yes",
    "Q6": "yes"
}

device_prompt_qa_dict[6] = {
    "EQ1": "yes",
    "EQ2": "no",
    "Q1": "yes",
    "Q3": "yes",
    "Q4": "yes",
    "Q5": "yes",
    "Q6": "yes"
}

def build_EQ1_prompt(answer):
    if answer == "yes":
        EQ1_prompt = f"Use of a device WAS associated with an adverse outcome noted in the clinical record."
    else:
        EQ1_prompt = "Use of a device WAS NOT noted in the clinical record as associated with any adverse outcome."
    return EQ1_prompt

def build_EQ2_prompt(answer):
    if answer == "yes":
        EQ2_prompt = "The device related adverse outcome is noted in the clinical record as being present on admission (POA)."
    else:
        EQ2_prompt = "The device related adverse outcome is noted in the clinical record as NOT being present on admission (POA)."
    return EQ2_prompt

def build_Q1_prompt(answer):
    if answer == "hit":
        Q1_prompt = "The type of device involved in the adverse reaction is a HIT device."
    else:
        device_types = [
            "implantable device",
            "non-implantable device, such as endoscope, patient lift, monitor, pump, protective equipment",
            "medical / surgical supplies, such as bandages, flushes, dressings, cleaning solutions"
        ]
        device_type = random.choice(device_types)
        Q1_prompt = f"The type of device involved in the adverse reaction is a {device_type}."
    return Q1_prompt

def build_Q2_prompt(answer):
    hit_types = [
        "EHR or component of EHR",
        "Human interface device",
        "Radiology/diagnostic imaging system, including PACS"
    ]
    hit_type = random.choice(hit_types)
    Q2_prompt = f"The type of HIT device involved in the adverse reaction is a {hit_type}."
    return Q2_prompt

def build_Q3_prompt(answer):
    involvement_types = [
        "device defect or failure",
        "use error",
        "combination or interaction of device defect or failure and use error"
    ]
    involvement_type = random.choice(involvement_types)
    Q3_prompt = f"The record should note that the way the device was involved in the adverse reaction was {involvement_type}."
    return Q3_prompt

def build_Q4_prompt(answer):
    if answer == "yes":
        Q4_prompt = "A medication WAS involved in the device-related adverse event."
    else:
        Q4_prompt = "A medication WAS NOT involved in the device-related adverse_event."
    return Q4_prompt

def build_Q5_prompt():
    Q5_prompt = "Provide information about the device, including, as available, the type of the device, brand name, model, manufacturer, age, condition."
    return Q5_prompt

def build_Q6_prompt():
    Q6_prompt = "Describe how the device malfunction or improper use harmed the patient or note clearly that no harm was caused to the patient."
    return Q6_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(story_number):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(device_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(device_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] 

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    patient_age = f"{random.randint(1, 99)} years old"

    # create placeholders for variables that might get set / passed around between functions

    question_keys = list(device_prompt_qa_dict[num].keys())

    if "EQ1" in question_keys:
        ans = device_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = device_prompt_qa_dict[num]["EQ2"]
        eq2_prompt = build_EQ2_prompt(ans)
        list_of_prompts.append(eq2_prompt)
    if "Q1" in question_keys:
        ans = device_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q2" in question_keys:
        ans = device_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        ans = device_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = device_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "Q5" in question_keys:
        q5_prompt = build_Q5_prompt()
        list_of_prompts.append(q5_prompt)
    if "Q6" in question_keys:
        q6_prompt = build_Q6_prompt()
        list_of_prompts.append(q6_prompt)
    

    # after all build prompt functions that should be called are, add general prompts about the stay that might
    # not have been stated yet (remove duplicates at the end)
    list_of_prompts.append(f"Patient is {patient_age} old.")
    list_of_prompts.append(f"Patient was discharged on day number {discharge_day_number}.")

    # Device is odd in that from Q3 there's no branching; Q3 -> Q4 -> Q5 -> Q6 AND Q5, Q6 are free text. 
    # Redundant tails are kept in the dicts to create more diverse and full PDFs, using information from
    # the QSRS tool to help fill out data. The build prompt functions for Q5, Q6 have no if/else structure,
    # so their dict values of "yes" is just a placeholder.


    # join all the prompts into one big string and save it to the full-prompt dict
    prompt_string = " ".join(list_of_prompts)
    story_prompts_dict[num] = prompt_string

# when the loop is done running (prompts are generated for all stories)
# print to screen to be sure everything looks right
for num in story_numbers:
    print(f"full prompt to generate story number {num}:")
    print(story_prompts_dict[num])
    print()

import csv
csv_output_file = "device_prompts.csv"
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
json_output_file = "device_prompts.json"
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
