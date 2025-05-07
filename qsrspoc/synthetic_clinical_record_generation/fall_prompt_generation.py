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

fall_prompt_qa_dict = {}

fall_prompt_qa_dict[1] = {
    "EQ1": "yes",
    "EQ2": "no"
}

fall_prompt_qa_dict[2] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "Q1": "no",
    "Q4": "yes"
}

fall_prompt_qa_dict[3] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "RL1": "no",
    "Q4": "yes"
}

fall_prompt_qa_dict[4] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "Q1": "yes",
    "Q2": "yes",
    "RL1": "yes",
    "Q3": "yes",
    "Q4": "yes"
}

fall_prompt_qa_dict[5] = {
    "EQ1": "yes",
    "EQ2": "yes",
    "Q1": "yes",
    "Q2": "no",
    "Q4": "yes"
}

def build_EQ1_prompt(answer):
    if answer == "yes":
        assessment_hours = random.randint(1,24)
        EQ1_prompt = f"Within {assessment_hours} hours of admission, a fall risk assessment was documented."
    else:
        EQ1_prompt = f"There was no fall risk assessment documented."
    return EQ1_prompt


def build_EQ2_prompt(answer):
    if answer == "yes":
        number_falls = random.randint(1,4)
        EQ2_prompt = f"The patient fell {number_falls} times during their hospitalization."
    else:
        EQ2_prompt = f"The patient did not fall during their hospital stay."
    return EQ2_prompt


def build_Q1_prompt(answer):
    if answer == "yes":
        Q1_prompt = f"There was an injury as a result of the fall."
    else:
        Q1_prompt = f"There was no injury as a result of the fall."
    return Q1_prompt


def build_Q2_prompt(answer):
    fall_injuries = [
        "Intracranial Injury (e.g. subdural hematoma)",
        "Fracture",
        "Dislocation",
        "Laceration requiring sutures",
        "Other injury (e.g.,skin tear, avulsion,"
        "hematoma, bruising)",
    ]
    if answer == "yes":
        serious_injury = random.choice(fall_injuries)
        Q2_prompt = f"The patient suffered from {serious_injury}."
    else:
        joined_injury = " ".join(fall_injuries)
        Q2_prompt = f"There is no mention of these injuries in the chart: {joined_injury}."
    
    return Q2_prompt

def build_RL1_prompt(answer):
    if answer == "yes":
        RL1_prompt = f"Patient died during hospitalization. Their discharge status is death."
    else:
        RL1_prompt = f"The patient did not die during their stay, nor is there death mentioned at all in their chart or stay."
    return RL1_prompt

def build_Q3_prompt(answer):
    if answer == "yes":
        Q3_prompt = f"The patient's death was attributed to this fall."
    else:
        death_reasons = [
        "unrelated respiratory failure",
        "unrelated sepsis.",
        "unrelated cardiac arrest."
        ]
        rand_death = random.choice(death_reasons)
    
        Q3_prompt = f"The patient's death was NOT attributed to the fall, but rather to {rand_death} "
    return Q3_prompt

def build_Q4_prompt(answer):
    if answer == "yes":
        fall_type = [
            "assisted",
            "unassisted"
        ]
        fall = random.choice(fall_type)
        Q4_prompt = f"The patient's fall was {fall}."
    else:
        Q4_prompt = f"The patient's fall was not stated to be assisted nor unassisted."
    return Q4_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(fall_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(fall_prompt_qa_dict.keys())
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
    question_keys = list(fall_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQ1" in question_keys:
        ans = fall_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = fall_prompt_qa_dict[num]["EQ2"]
        eq2_prompt = build_EQ2_prompt(ans)
        list_of_prompts.append(eq2_prompt)
    if "Q1" in question_keys:
        ans = fall_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q2" in question_keys:
        ans = fall_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "RL1" in question_keys:
        ans = fall_prompt_qa_dict[num]["RL1"]
        rl1_prompt = build_RL1_prompt(ans)
        list_of_prompts.append(rl1_prompt)
    if "Q3" in question_keys:
        ans = fall_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = fall_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
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

