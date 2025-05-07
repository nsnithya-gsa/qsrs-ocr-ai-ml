
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
		right_of_window_days = list(range(window_center_day + (dis_day + 1)))

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



##############################################################

ssi_prompt_qa_dict = {}
ssi_prompt_qa_dict[1] = {
    "EQR1": "no"
}
ssi_prompt_qa_dict[2] = {
	"EQR1": "yes",
    "EQ1": "no"
}
ssi_prompt_qa_dict[3] = {
	"EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "no"
}
ssi_prompt_qa_dict[4] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "SKIN_SUBCUTANEOUS_ONLY",
    "Q1": "none"
}
ssi_prompt_qa_dict[5] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "SKIN_SUBCUTANEOUS_ONLY",
    "Q1": "non_incision_list",
}
ssi_prompt_qa_dict[6] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "SKIN_SUBCUTANEOUS_ONLY",
    "Q1": "incision_drained",
    "Q5": "yes",
    "Q6": "no"
}
ssi_prompt_qa_dict[7] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "SKIN_SUBCUTANEOUS_ONLY",
    "Q1": "incision_drained",
    "Q5": "yes",
    "Q6": "yes",
    "Q7": "none"
}
ssi_prompt_qa_dict[8] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "SKIN_SUBCUTANEOUS_ONLY",
    "Q1": "incision_drained",
    "Q5": "yes",
    "Q6": "yes",
    "Q7": "yes"
}
ssi_prompt_qa_dict[9] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "SKIN_SUBCUTANEOUS_ONLY",
    "Q1": "incision_drained",
    "Q5": "no"
}
ssi_prompt_qa_dict[10] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "DEEP_SOFT_TISSUE",
    "Q2": "deep_incision_open",
    "Q8": "yes",
    "Q9": "no"
}
ssi_prompt_qa_dict[11] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "DEEP_SOFT_TISSUE",
    "Q2": "deep_incision_open",
    "Q8": "yes",
    "Q9": "yes",
    "Q10": "none"
}
ssi_prompt_qa_dict[12] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "DEEP_SOFT_TISSUE",
    "Q2": "deep_incision_open",
    "Q8": "yes",
    "Q9": "yes",
    "Q10": "yes"
}

ssi_prompt_qa_dict[13] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "DEEP_SOFT_TISSUE",
    "Q2": "deep_incision_open",
    "Q8": "no"
}

ssi_prompt_qa_dict[14] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "DEEP_SOFT_TISSUE",
    "Q2": "deep_incision_list",
}
ssi_prompt_qa_dict[15] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "DEEP_SOFT_TISSUE",
    "Q2": "none"
}
ssi_prompt_qa_dict[16] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "UNSPECIFIED_DEPTH",
    "Q3": "unsp_inc_open",
    "Q11" :"yes",
    "Q12": "no" 
}
ssi_prompt_qa_dict[17] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "UNSPECIFIED_DEPTH",
    "Q3": "unsp_inc_open",
    "Q11" :"yes",
    "Q12": "yes",
    "Q13": "none"
}
ssi_prompt_qa_dict[18] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "UNSPECIFIED_DEPTH",
    "Q3": "unsp_inc_open",
    "Q11" :"yes",
    "Q12": "yes",
    "Q13": "yes"
}
ssi_prompt_qa_dict[19] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "UNSPECIFIED_DEPTH",
    "Q3": "unsp_inc_open",
    "Q11": "no"
}
ssi_prompt_qa_dict[20] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "UNSPECIFIED_DEPTH",
    "Q3": "uns_inc_list",
}
ssi_prompt_qa_dict[21] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "UNSPECIFIED_DEPTH",
    "Q3": "none"
}
ssi_prompt_qa_dict[22] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "ORGAN_SPACE",
    "Q4": "yes"
}
ssi_prompt_qa_dict[23] = { 
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "ORGAN_SPACE",
    "Q4": "none"
}

# SSI.EQR1: Check to see if GEN.Q5 = ‘Yes’ (Did the patient have an operating room procedure?)
def build_EQR1_prompt(answer):
    if answer == "yes":
        EQR1_prompt = "The patient had an operating room procedure during this stay."
    else:
        EQR1_prompt = "The patient did not have an operating room procedure during this stay."
    return EQR1_prompt


# SSI.EQ1: Did the patient develop a surgical site infection that was not present or diagnosed prior to the first Operating Room (OR) procedure performed during this stay?
def build_EQ1_prompt(answer):
    if answer == "yes":
        EQ1_prompt = f"The patient developed a surgical site infection during the stay that was not present or diagnosed prior to the first operating room procedure during the stay."
    else:
        EQ1_prompt = f"The patient did not develop a surgical site infection (SSI) during the stay after the first Operating Room (OR) procedure performed during this stay."
    return EQ1_prompt


# answers are SKIN_SUBCUTANEOUS_ONLY, DEEP_SOFT_TISSUE, UNSPECIFIED_DEPTH, ORGAN_SPACE
def build_EQ2_prompt(answer):
    if answer == "SKIN_SUBCUTANEOUS_ONLY":
        EQ2_prompt = "The patient's SSI was a skin and subcutaneous tissue infection without deeper involvement."
    elif answer == "DEEP_SOFT_TISSUE":
        EQ2_prompt = "The patient's SSI was an infection of deep soft tissue."
    elif answer == "UNSPECIFIED_DEPTH":
        EQ2_prompt = "The patient's SSI was an infection without mention of superficiality."
    else: # ORGAN_SPACE
        EQ2_prompt = "The patient's SSI was an infection within organ space."
    return EQ2_prompt

# answers are incision_drained, non_incision_list, none
def build_Q1_prompt(answer):
    if answer == "incision_drained":
        Q1_prompt = f"The record must note that an incision was opened or drained."
    elif answer == "non_incision_list"
        non_incision_list = [
                "Superficial incisional SSI (surgical site infection)",
                "Purulent drainage from a superficial incision",
                "Organisms isolated from a culture of fluid or tissue from a superficial incision and / or subcutaneous tissue around operative site"
        ]
        rand_symptom = random.choice(non_incision_list)
        Q1_prompt = f"The record must note {rand_symptom}."
    else: # none
        non_incision_list.append("An incision was opened or drained")
        all_symptom_str = ", ".join(non_incision_list)
        Q1_prompt = f"The record must not mention any of the following: {all_symptom_str}."
    return Q1_prompt

def build_Q5_prompt(answer):
    if answer == "yes":
        Q5_prompt = f"A culture was collected from the wound."
    else:
        Q5_prompt = "No culture was performed from the wound"
    return Q5_prompt


def build_Q6_prompt(answer):
    if answer == "yes":
        Q6_prompt = f"This culture  was positive for infection."
    else:
        Q6_prompt = f"This culture did not indicate infection."
    return Q6_prompt


def build_Q7_prompt(answer):
    list_for_Q7 = [
        "Pain or tenderness",
        "Localized swelling",
        "Redness or heat"
    ]
    Q7_prompt = multiple_choice_question (answer, "skin and subcutaneous tissue infection symptoms", list_for_Q7)
    return Q7_prompt

# answers are deep_incision_open, deep_incision_list, none
def build_Q2_prompt(answer):
    if answer == "deep_incision_open":
        Q2_prompt = f"The medical record must note A deep incision that dehisces, is opened, or is percutaneously aspirated."
    elif answer == "deep_incision_list":
        list_for_Q2 = [
                "a deep incisional SSI (surgical site infection)",
                "purulent drainage from a deep infection",
                "an abscess or other evidence of infection found on physical exam, during an invasive procedure, pathology report, or imaging test"
        ]
        rand_symptom = random.choice(list_for_Q2)
        Q2_prompt = f"The medical record must note {rand_symptom}."
    else: # none
        list_for_Q2.append("A deep incision that dehisces, is opened, or is percutaneously aspirated")
        all_symptom_str = ", ".join(list_for_Q2)
        Q2_prompt = f"The record must not note any of the following: {all_symptom_str}."
    return Q2_prompt

def build_Q8_prompt(answer):
    if answer == "yes":
        Q8_prompt = f"A culture was collected from the deep incision."
    else:
        Q8_prompt = "No culture was performed from the deep incision."
    return Q8_prompt

def build_Q9_prompt(answer):
    if answer == "yes":
        Q9_prompt = f"This culture collected from the deep incision was positive for infection."
    else:
        Q9_prompt = f"This culture collected from the deep incision tested negative for infection."
    return Q9_prompt

def build_Q10_prompt(answer):
    list_for_Q10 = [
        "Fever (> 38 degrees C)",
        "Localized pain or tenderness"
    ]
    Q10_prompt = multiple_choice_question (answer, "deep soft tissue infection symptoms", list_for_Q10)
    return Q10_prompt

# answers are unsp_inc_open, uns_inc_list, none
def build_Q3_prompt(answer):
    if answer == "unsp_inc_open":
        Q3_prompt = "The record must note an incision, without mention of superficial or deep, that is opened."
    elif answer == "uns_inc_list"
        list_for_Q3 = [
            "an SSI (surgical site infection), without mention of superficial or deep",
            "purulent drainage from the incision without mention of superficial or deep",
            "organisms isolated from a culture of fluid or tissue from an incision without mention of superficial or deep"
        ]
        rand_symptom = random.choice(list_for_Q3)
        Q3_prompt = f"The record must note {rand_symptom}."
    else: # none
        list_for_Q3.append("an incision, without mention of superficial or deep, that is opened")
        all_symptom_str = ", ".join(list_for_Q3)
        Q3_prompt = f"The record must not note any of the following: {all_symptom_str}."
    return Q3_prompt

def build_Q11_prompt(answer):
    if answer == "yes":
        Q11_prompt = f"A culture was collected from the unspecified incision."
    else:
        Q11_prompt = "No culture was performed from the unspecified incision."
    return Q11_prompt

def build_Q12_prompt(answer):
    if answer == "yes":
        Q12_prompt = f"This culture collected from the unspecified incision was positive for infection."
    else:
        Q12_prompt = f"This culture collected from the unspecified incision was negative for infection."
    return Q12_prompt

def build_Q13_prompt(answer):
    list_for_Q13 = [
        "Fever (> 38 degrees C)",
        "Pain or tenderness",
        "Localized swelling",
        "Redness or heat"
    ]
    Q13_prompt = multiple_choice_question (answer, "infection without mention of superficiality symptoms", list_for_Q13)
    return Q13_prompt

def build_Q4_prompt(answer):
    list_for_Q4 = [
        "Organ or organ space SSI (surgical site infection)",
        "Purulent drainage from a drain that is placed into an organ or organ space",
        "Abscess or other evidence of infection found on physical exam, during an invasive procedure, pathology report, or imaging test",
        "Organisms isolated from a culture of fluid or tissue in an organ space"
    ]
    Q4_prompt = multiple_choice_question (answer, "SSI symptoms", list_for_Q4)
    return Q4_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(hai_ssi_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(hai_ssi_prompt_qa_dict.keys())
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
    question_keys = list(hai_ssi_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQR1" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["EQR1"]
        eqr1_prompt = build_EQR1_prompt(ans)
        list_of_prompts.append(eqr1_prompt)
    if "EQ1" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["EQ2"]
        eq2_prompt = build_EQ2_prompt(ans)
        list_of_prompts.append(eq2_prompt)
    if "Q1" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q5" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
    if "Q6" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans)
        list_of_prompts.append(q6_prompt)
    if "Q7" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q7"]
        q7_prompt = build_Q7_prompt(ans)
        list_of_prompts.append(q7_prompt)
    if "Q2" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "Q8" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q8"]
        q8_prompt = build_Q8_prompt(ans)
        list_of_prompts.append(q8_prompt)
    if "Q9" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q9"]
        q9_prompt = build_Q9_prompt(ans)
        list_of_prompts.append(q9_prompt)
    if "Q10" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q10"]
        q10_prompt = build_Q10_prompt(ans)
        list_of_prompts.append(q10_prompt)
    if "Q3" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q11" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q11"]
        q11_prompt = build_Q11_prompt(ans)
        list_of_prompts.append(q11_prompt)
    if "Q12" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q12"]
        q12_prompt = build_Q12_prompt(ans)
        list_of_prompts.append(q12_prompt)
    if "Q13" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q13"]
        q13_prompt = build_Q13_prompt(ans)
        list_of_prompts.append(q13_prompt)
    if "Q4" in question_keys:
        ans = hai_ssi_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q3_prompt(ans)
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







