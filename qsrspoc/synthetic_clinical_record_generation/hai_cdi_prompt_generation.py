import random
from typing import List, Tuple
from datetime import datetime, timedelta

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
algo_str = "cdi"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.

cdi_prompt_qa_dict = {}

cdi_prompt_qa_dict[1] = {
    "EQR1": "yes"
}

cdi_prompt_qa_dict[2] = {
    "EQR1": "no",
    "EQR2": "a_047",
    "EL3": "yes"
}

cdi_prompt_qa_dict[3] = {
    "EQR1": "no",
    "EQR2": "a_047",
    "EL3": "no"
}

cdi_prompt_qa_dict[4] = {
    "EQR1": "no",
    "EQR2": "other",
    "EQ1": "no",
    "EQ2": "no"
}

cdi_prompt_qa_dict[5] = {
    "EQR1": "no",
    "EQR2": "other",
    "EQ1": "no",
    "EQ2": "yes"
}

cdi_prompt_qa_dict[6] = {
    "EQR1": "no",
    "EQR2": "other",
    "EQ1": "yes", # to page 2
    "Q1": "timeline_a",
    "R3": "timeline_a"
}

cdi_prompt_qa_dict[7] = {
    "EQR1": "no",
    "EQR2": "other",
    "EQ1": "yes", # to page 2
    "Q1": "none"
}

cdi_prompt_qa_dict[8] = {
    "EQR1": "no",
    "EQR2": "other",
    "EQ1": "yes", # to page 2
    "Q1": "timeline_b",
    "R3": "timeline_b",
    "Q2": "no",
    "Q3": "no"
}

cdi_prompt_qa_dict[9] = {
    "EQR1": "no",
    "EQR2": "other",
    "EQ1": "yes", # to page 2
    "Q1": "timeline_b",
    "R3": "timeline_b",
    "Q2": "no",
    "Q3": "yes"
}

cdi_prompt_qa_dict[10] = {
    "EQR1": "no",
    "EQR2": "other",
    "EQ1": "yes", # to page 2
    "Q1": "timeline_b",
    "R3": "timeline_b",
    "Q2": "yes",
    "Q4": "timeline_b",
    "R4": "timeline_b"
}

cdi_prompt_qa_dict[11] = {
    "EQR1": "no",
    "EQR2": "other",
    "EQ1": "yes", # to page 2
    "Q1": "timeline_c",
    "R3": "timeline_c",
    "Q2": "yes",
    "Q4": "timeline_c",
    "R4": "timeline_c"
}


def build_EQR1_prompt(answer):
    if answer == "yes":
        age_type = "months"
        patient_age = random.randint(2,23)
        EQ1_prompt = f"The patient is {patient_age} {age_type} old."
    else:
        age_type = "years"
        patient_age = random.randint(2,99)
        EQ1_prompt = f"The patient is {patient_age} {age_type} old."
    return EQ1_prompt, patient_age, age_type

def build_EQR2_prompt(answer):
    if answer == "a_047":
         EQR2_prompt = f"Patient has ICD-10 Code: A04.7 – Enterocolitis due to Clostridium difficile."
    
    else:
        list_for_EQR2 = [
            "J45.909 – Unspecified asthma, uncomplicated",
            "S93.401A – Sprain of unspecified ligament of right ankle, initial encounter",
            "E11.9 – Type 2 diabetes mellitus without complications"
        ]
        # Randomly select between 1 to 3 items from the list
        num_choices = random.randint(1, 3)  # Randomly pick 1, 2, or 3 choices
        ICD_10_random = random.sample(list_for_EQR2, num_choices)  # Pick unique items
        ICD_10_text = ", ".join(ICD_10_random)  # Convert list to a readable string
        EQR2_prompt = f"Patient has ICD-10 Codes: {ICD_10_text}."

    return EQR2_prompt

#check to see if c-dif code was present on admission! assuming yes to last q
def build_EL3_prompt(answer):
    if answer =="yes":
        EL3_prompt = f"ICD-10 code was present on admission."
    else:
        EL3_prompt = f"ICD-10 code was NOT present on admission."
    return EL3_prompt

# was there a positive CDI toxin A and-or Toxin B found in the stool sample?
def build_EQ1_prompt(answer):
    if answer == "yes":
        list_for_EQ1 = [
              "CDI Toxin A",
              "CDI Toxin B",
              "CDI Toxin A and B"
        ]
        toxin_type = random.choice(list_for_EQ1)
        EQ1_prompt = f"Patient's stool sample tested positive for {toxin_type}."
    else:
        EQ1_prompt = "No positive CDI Toxin A or Toxin B was found in the patient's stool sample."
    return EQ1_prompt

#Was there a toxin producing CDI organism detected in the patient’s stool sample?
def build_EQ2_prompt(answer):
    if answer == "yes":
        EQ2_prompt = f"There was a toxin producing CDI organism detected in the patient's stool sample."
    else:
         EQ2_prompt = f"There was not a toxin producing CDI organism detected in the patient's stool sample."
    return EQ2_prompt

# answer is timeline_a, timeline_b, timeline_c, or none
def build_Q1_prompt(answer, timelines_dict):
    if answer == "timeline_a":
        pos_cdi_date = timelines_dict["timeline_a"]["pos_cdi_date"]
        Q1_prompt = f"The date the first specimen was collected that tested postive for CDI was {pos_cdi_date}."
    if answer == "timeline_b":
        pos_cdi_date = timelines_dict["timeline_b"]["pos_cdi_date"]
        Q1_prompt = f"The date the first specimen was collected that tested postive for CDI was {pos_cdi_date}."
    if answer == "timeline_c":
        pos_cdi_date = timelines_dict["timeline_c"]["pos_cdi_date"]
        Q1_prompt = f"The date the first specimen was collected that tested postive for CDI was {pos_cdi_date}."
    else: # answer is none
        Q1_prompt = "The record MUST NOT note the day or date on which the first specimen was collected that tested postive for CDI."
        pos_cdi_date = ""
    return Q1_prompt

def build_R3_prompt(answer, timelines_dict):
    if answer == "timeline_a":
        admission_date = timelines_dict["timeline_a"]["admission_date"]
        R3_prompt = f"The date the patient was admitted was {admission_date}."
    if answer == "timeline_b":
        admission_date = timelines_dict["timeline_b"]["admission_date"]
        R3_prompt = f"The date the patient was admitted was {admission_date}."
    if answer == "timeline_c":
        admission_date = timelines_dict["timeline_c"]["admission_date"]
        R3_prompt = f"The date the patient was admitted was {admission_date}."
    return R3_prompt

def build_Q2_prompt(answer):
    if answer == "yes":
        Q2_prompt = "The medical record MUST note that the patient had loose stool during the stay."
    else:
        Q2_prompt = "The medical record MUST NOT note that the patient had loose stool or diarrhea during the stay."
    return Q2_prompt

def build_Q3_prompt(answer):
    if answer == "yes":
        Q3_prompt = "The medical record MUST document that the patient had pseudomembranous colitis during their stay."
    else:
        Q3_prompt = "The medical record MUST NOT document that the patient had pseudomembranous colitis during their stay."
    return Q3_prompt

def build_Q4_prompt(answer, timelines_dict):
    if answer == "timeline_a":
        cdi_doc_date = timelines_dict["timeline_a"]["cdi_doc_date"]
        Q4_prompt = f"The medical record MUST note that the first episode of loose stool during the stay occurred on {cdi_doc_date}."
    if answer == "timeline_b":
        cdi_doc_date = timelines_dict["timeline_b"]["cdi_doc_date"]
        Q4_prompt = f"The medical record MUST note that the first episode of loose stool during the stay occurred on {cdi_doc_date}."
    if answer == "timeline_c":
        cdi_doc_date = timelines_dict["timeline_c"]["cdi_doc_date"]
        Q4_prompt = f"The medical record MUST note that the first episode of loose stool during the stay occurred on {cdi_doc_date}."
    return Q4_prompt

# R4 is an extension of Q4 but provides a good place to specify discharge date, which only matters if we reach Q4/R4
def build_R4_prompt(answer, timelines_dict):
    if answer == "timeline_a":
        discharge_date = timelines_dict["timeline_a"]["discharge_date"]
        R4_prompt = f"The patient was discharged on {discharge_date}."
    if answer == "timeline_b":
        discharge_date = timelines_dict["timeline_b"]["discharge_date"]
        R4_prompt = f"The patient was discharged on {discharge_date}."
    if answer == "timeline_c":
        discharge_date = timelines_dict["timeline_c"]["discharge_date"]
        R4_prompt = f"The patient was discharged on {discharge_date}."
    return R4_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(cdi_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(cdi_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    #discharge_day_number = random.randint(4, 8)
    patient_age = random.randint(1, 99)
    age_type = ""

    # timelines needed (the prompts require dates in MM/DD/YYYY format, not day numbers): 
    # a: Q1=yes, R3=no: pos_cdi_day = x, x-admission_day <= 2 (except convert all to dates starting with x)
    # b: Q1=yes, R3=yes,(Q2=yes), Q4/R4=yes: pos_cdi_day = x, pos_cdi_day - admission_day > 2, pos_cdi_day - cdi_doc_day >= 0
    # c: Q1=yes, R3=yes,(Q2=yes), Q4/R4=no: pos_cdi_day = x, pos_cdi_day - admission_day > 2, pos_cdi_day - cdi_doc_day < 0
    timeline_a = {
        "pos_cdi_date" : "09/15/2022",
        "admission_date": "09/14/2022",
        "cdi_doc_date": "",
        "discharge_date": "09/18/2022"
    }
    timeline_b = {
        "pos_cdi_date" : "07/20/2023",
        "admission_date": "07/15/2023",
        "cdi_doc_date": "07/18/2023",
        "discharge_date": "07/24/2023",
    }
    timeline_c = {
        "pos_cdi_date" : "11/10/2021",
        "admission_date": "11/05/2021",
        "cdi_doc_date": "11/12/2021",
        "discharge_date": "11/14/2021"
    }

    timelines_dict = {
        "timeline_a": timeline_a,
        "timeline_b": timeline_b,
        "timeline_c": timeline_c
    }

    # create placeholders for variables that might get set / passed around between functions

    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(cdi_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQR1" in question_keys:
        ans = cdi_prompt_qa_dict[num]["EQR1"]
        eqr1_prompt, patient_age, age_type = build_EQR1_prompt(ans)
        list_of_prompts.append(eqr1_prompt)
    if "EQR2" in question_keys:
        ans = cdi_prompt_qa_dict[num]["EQR2"]
        eqr2_prompt = build_EQR2_prompt(ans)
        list_of_prompts.append(eqr2_prompt)
    if "EL3" in question_keys:
        ans = cdi_prompt_qa_dict[num]["EL3"]
        el3_prompt = build_EL3_prompt(ans)
        list_of_prompts.append(el3_prompt)
    if "EQ1" in question_keys:
        ans = cdi_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = cdi_prompt_qa_dict[num]["EQ2"]
        eq2_prompt = build_EQ2_prompt(ans)
        list_of_prompts.append(eq2_prompt)
    if "Q1" in question_keys:
        ans = cdi_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans, timelines_dict)
        list_of_prompts.append(q1_prompt)
    if "R3" in question_keys:
        ans = cdi_prompt_qa_dict[num]["R3"]
        r3_prompt = build_R3_prompt(ans, timelines_dict)
        list_of_prompts.append(r3_prompt)
    if "Q2" in question_keys:
        ans = cdi_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        ans = cdi_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = cdi_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans, timelines_dict)
        list_of_prompts.append(q4_prompt)
    if "R4" in question_keys:
        ans = cdi_prompt_qa_dict[num]["R4"]
        r4_prompt = build_R4_prompt(ans, timelines_dict)
        list_of_prompts.append(r4_prompt)
    
    #######


    # after all build prompt functions that should be called are, add general prompts about the stay that might
    # not have been stated yet (remove duplicates at the end)
    #list_of_prompts.append(f"Patient is {patient_age} {age_type} old.")
    #list_of_prompts.append(f"Patient was discharged on day number {discharge_day_number}.")

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


