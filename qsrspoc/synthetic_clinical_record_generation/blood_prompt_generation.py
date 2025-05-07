
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

##############################################################

# this is used for file naming
algo_str = "blood"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.

blood_prompt_qa_dict = {}
blood_prompt_qa_dict[1] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "no",
    "Q1": "yes",
    "Q2": "no",
    "Q3": "none",
    "Q4": "no",
    "Q5": "no"
}
blood_prompt_qa_dict[2] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "no",
    "Q1": "yes",
    "Q2": "no",
    "Q3": "none",
    "Q4": "no",
    "Q5": "yes"
}
blood_prompt_qa_dict[3] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "no",
    "Q1": "yes",
    "Q2": "no",
    "Q3": "none",
    "Q4": "yes",
    "R0": "no"
}
blood_prompt_qa_dict[4] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "no",
    "Q1": "yes",
    "Q2": "no",
    "Q3": "none",
    "Q4": "yes",
    "R0": "yes",
    "Q4a": "no"
}
blood_prompt_qa_dict[5] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "no",
    "Q1": "yes",
    "Q2": "no",
    "Q3": "none",
    "Q4": "yes",
    "R0": "yes",
    "Q4a": "yes"
}
blood_prompt_qa_dict[6] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "no",
    "Q1": "yes",
    "Q2": "no",
    "Q3": "yes"
}
blood_prompt_qa_dict[7] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "no",
    "Q1": "yes",
    "Q2": "yes"
}
blood_prompt_qa_dict[8] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "yes",
    "EQ1": "no"
}
blood_prompt_qa_dict[9] = {
    "EQR1": "yes",
    "EL1a": "no",
    "EL2": "yes",
    "EQ1": "yes"
}
blood_prompt_qa_dict[10] = {
    "EQR1": "yes",
    "EL1a": "yes"
}
blood_prompt_qa_dict[11] = {
    "EQR1": "no"
}

def build_EQR1_prompt(answer):
    # List of ICD-10 codes related to transfusion reactions (first 5 codes)
    transfusion_reaction_code = [
        "T80.51XA", "T80.311A", "T80.410A", "T80.319A", "T80.30XA"
    ]
    # List of unrelated ICD-10 codes
    unrelated_codes = [
        "Z00.00", "M54.5", "E11.9"  # Generic unrelated codes (example: checkup, back pain, diabetes)
    ]
    selected_code = ""

    if answer == "yes":
        selected_code = random.sample(transfusion_reaction_code, 1)
        EQR1_prompt = (
            f"There is a secondary diagnosis of a transfusion reaction: {selected_code}."
        )
    else:
        selected_code = random.sample(unrelated_codes, 1)
        EQR1_prompt = (
            f"There is a secondary diagnosis of a transfusion reaction: {selected_code}."
        )
    return EQR1_prompt, selected_code

#check to see if POA is null (if there is anything listed for context)
def build_EL1a_prompt(answer, transfusion_related_code):
    if answer == "yes":
        EL1a_prompt = f"The ICD-10 code: {transfusion_related_code} has a POA status that is null or not recorded."
    else:
        EL1a_prompt = f"The ICD-10 code: {transfusion_related_code} has a recorded POA status."
    
    return EL1a_prompt



def build_EL2_prompt(answer, transfusion_related_code):
    if answer == "no":
        EL2_prompt =f"{transfusion_related_code} was NOT present on admission (POA)."
    else:
        EL2_prompt = f"{transfusion_related_code} ICD-10 code was present on admission"
    return EL2_prompt


def build_EQ1_prompt(answer):
    if answer == "yes":
        EQ1_prompt = "Patient received a transfusion of blood or a blood product during the stay."
    else:
        EQ1_prompt = "Patient did not receive a transfusion of blood or a blood product during the stay."
    return EQ1_prompt

#multiple choice
def build_Q1_prompt(answer):
    list_for_Q1 = [
            "Red blood cells",
            "Platelets",
            "Plasma",
            "Cryoprecipitate",
            "Hematopoietic stem cells",
            "Whole blood",
            "Lymphocytes",
            "Granulocytes"
    ]
    Q1_prompt = multiple_choice_question(answer, "blood products used in the transfusion", list_for_Q1)

    return Q1_prompt

def build_Q2_prompt(answer):
    if answer == "yes":
        epi_cortico = [
            "epinepherine was",
            "a corticosteroid was",
            "epinepherine and corticosteroids were"
        ]
        Q2_prompt = f"Within 2 hours of completion of the administration of a blood product, {epi_cortico} administered."
    else:
        Q2_prompt = "The record must not make any mention of epinephrine or corticosteroids being adminsitered within 2 hours of completion of the administration of a blood product."
    return Q2_prompt

def build_Q3_prompt(answer):
    list_for_Q3 = [
        "Oxygen administration initiated after transfusion",
        "Ventilator support initiated after transfusion"
    ]
    Q3_prompt = multiple_choice_question(answer, "treatments for respiratory distress", list_for_Q3)
    return Q3_prompt

def build_Q4_prompt(answer):
    if answer == "yes":
        Q4_prompt = "There was documentation in the medical record of a transfusion reaction."
    else:
        Q4_prompt = "The medical record MUST NOT include any mention of a transfusion reaction."
    return Q4_prompt

#we get here if there is not documentation related to a transfusion reaction
#Did the patient receive a product notes as an incompapitble ABO type?
def build_Q5_prompt(answer):
    if answer == "yes":
        Q5_prompt = "The patient received a product noted as an incompatible ABO type."
    else:
        Q5_prompt = "The patient did not receive a product noted as an incompatible ABO type."
    return Q5_prompt

def build_R0_prompt(answer, dis_day):
    died_day = -1
    if answer == "yes":
        died_day = random.randint(1, dis_day)
        R0_prompt = f"The patient died on day {died_day} of their stay, reulting in a died discharge status. "
    else:
        R0_prompt = f"The patient did not die during their hospital admission stay."
    return R0_prompt

def build_Q4a_prompt(answer):
    list_for_Q4a = [
        "sepsis",
        "cardiac arrest",
        "stroke"
    ]
    if answer == "yes":
        Q4a_prompt = f"The patient's death is notated to be attributed to the blood transfusion reaction. "
    else:
        cause_of_death = random.sample(list_for_Q4a, 1)
        Q4a_prompt = f"The patient's death was not attributed to the blood transfusion reaction, but instead due to {cause_of_death}. "
    return Q4a_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(blood_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(blood_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    patient_age = random.randint(1, 99)
    transfusion_related_code = ""

    # create placeholders for variables that might get set / passed around between functions

    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(blood_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQR1" in question_keys:
        ans = blood_prompt_qa_dict[num]["EQR1"]
        eqr1_prompt, transfusion_related_code = build_EQR1_prompt(ans)
        list_of_prompts.append(eqr1_prompt)
    if "EL1a" in question_keys:
        ans = blood_prompt_qa_dict[num]["EL1a"]
        el1a_prompt = build_EL1a_prompt(ans, transfusion_related_code)
        list_of_prompts.append(el1a_prompt)
    if "EL2" in question_keys:
        ans = blood_prompt_qa_dict[num]["EL2"]
        el2_prompt = build_EL2_prompt(ans, transfusion_related_code)
        list_of_prompts.append(el2_prompt)
    if "EQ1" in question_keys:
        ans = blood_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "Q1" in question_keys:
        ans = blood_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q2" in question_keys:
        ans = blood_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        ans = blood_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = blood_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "Q5" in question_keys:
        ans = blood_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
    if "R0" in question_keys:
        ans = blood_prompt_qa_dict[num]["R0"]
        r0_prompt = build_R0_prompt(ans, discharge_day_number)
        list_of_prompts.append(r0_prompt)
    if "Q4a" in question_keys:
        ans = blood_prompt_qa_dict[num]["Q4a"]
        q4a_prompt = build_Q4a_prompt(ans)
        list_of_prompts.append(q4a_prompt)
    

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
