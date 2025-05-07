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
algo_str = "hai_hap"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.

hap_prompt_qa_dict = {}

hap_prompt_qa_dict[1] = {
	"EQ1": "yes"
}
hap_prompt_qa_dict[2] = {
	"EQ1": "no",
	"EQ2": "no"
}

# case 1: force age as < 1
hap_prompt_qa_dict[3] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "yes",
    "Q2": "none"
}

hap_prompt_qa_dict[4] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "yes",
    "Q2": "yes"
}

# case 2: force age as 1 < age < 70
hap_prompt_qa_dict[5] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "none"
}

hap_prompt_qa_dict[6] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "no",
    "Q6": "none"
}

hap_prompt_qa_dict[7] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "no",
    "Q6": "yes"
}

# case 3: force age as > 70
hap_prompt_qa_dict[8] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "none"
}

hap_prompt_qa_dict[9] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "yes",
    "Q6a": "none"
}

hap_prompt_qa_dict[10] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "yes",
    "Q6a": "yes",
    "Q8": "none"
}

hap_prompt_qa_dict[11] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "yes",
    "Q6a": "yes",
    "Q8": "yes",
    "Q7": "no"
}

hap_prompt_qa_dict[12] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "yes",
    "Q6a": "yes",
    "Q8": "yes",
    "Q7": "yes",
    "Q7a": "yes"
}

hap_prompt_qa_dict[13] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "yes",
    "Q6a": "yes",
    "Q8": "yes",
    "Q7": "yes",
    "Q7a": "no",
    "Q9": "yes", # non-branching
    "R9a": "yes",
    "Q10": "yes", # non-branching
    "R9b": "yes",
    "Q11": "yes" # non-branching
}

hap_prompt_qa_dict[14] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "yes",
    "Q6a": "yes",
    "Q8": "yes",
    "Q7": "yes",
    "Q7a": "no",
    "Q9": "yes", # non-branching
    "R9a": "yes",
    "Q10": "yes", # non-branching
    "R9b": "no",
    "Q11": "yes" # non-branching
}

hap_prompt_qa_dict[15] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "yes",
    "Q6a": "yes",
    "Q8": "yes",
    "Q7": "yes",
    "Q7a": "no",
    "Q9": "yes", # non-branching
    "R9a": "yes",
    "Q10": "no", # non-branching
    "R9b": "no"
}

hap_prompt_qa_dict[16] = {
	"EQ1": "no",
	"EQ2": "yes",
	"R1": "no",
    "Q1": "yes",
    "R2": "yes",
    "Q5": "yes",
    "Q6a": "yes",
    "Q8": "yes",
    "Q7": "yes",
    "Q7a": "no",
    "Q9": "yes", # non-branching
    "R9a": "no",
    "R9b": "no"
}

# new dicts are done and guarantee no age contradictions within a story.

def build_EQ1_prompt(answer, diagnosis_day_number):
	if answer == "yes":
		diagnosis_day_number = random.choice([1, 2])
		EQ1_prompt = f"Pneumonia WAS documented as POA indicated by physician diagnosis of pneumonia on day number {diagnosis_day_number}."
	else:
		EQ1_prompt = f"Pneumonia WAS NOT documented as POA."
	return EQ1_prompt, diagnosis_day_number

def build_EQ2_prompt(answer, discharge_day_number):
	if answer == "yes":
		radiograph_day_number = random.randint(3, discharge_day_number)
		diagnosis_day_number = radiograph_day_number
		EQ2_prompt = f"A chest radiograph was done on day number {radiograph_day_number}."
	else:
		EQ2_prompt = f"A chest radiograph was not done."
		diagnosis_day_number = random.randint(3, discharge_day_number)
		radiograph_day_number = -1 # no radiograph performed, -> end

	return EQ2_prompt, radiograph_day_number, diagnosis_day_number

def build_R1_prompt(answer):
	if answer == "yes":
		age_str = f"{random.randint(1, 11)} months"
	else:
		age_str = f"{random.randint(1,100)} years"

	R1_prompt = "" # stating the age at this point is redundant at best, creating a contradiction at worst
	return R1_prompt, age_str

def build_Q1_prompt(answer):
	list_for_Q1 = ["Infiltrate", "Consolidation", "Cavitation"]

	Q1_prompt = multiple_choice_question(answer, "chest radiograph findings", list_for_Q1)

	return Q1_prompt

def build_Q2_prompt(answer):
	list_for_Q2 = ["Infiltrate", "Consolidation", "Cavitation", "Pneumatocele"]

	Q2_prompt = multiple_choice_question(answer, "chest radiograph findings", list_for_Q2)

	return Q2_prompt

def build_R2_prompt(answer):
	if answer == "yes":
		insertion = random.randint(71, 100) # 75
	else:
		insertion = random.randint(1,70)

	R2_prompt = "" # stating the age at this point is redundant at best, creating a contradiction at worst
	age_str = f"{insertion} years"

	return R2_prompt, age_str

def build_Q5_prompt(answer):
	list_for_Q5 = [
		"Fever (> 38 degrees C)",
		"Leukopenia (<4000 WBC/mm3) or Leukocytosis (>12,000 WBC/mm3)",
		"Decline in mental status"
	]
	Q5_prompt = multiple_choice_question(answer, "systemic findings", list_for_Q5)
	return Q5_prompt


def build_Q6_prompt(answer):
	list_for_Q6 = [
		"Fever (> 38 degrees C)",
		"Leukopenia (<4000 WBC/mm3) or Leukocytosis (>12,000 WBC/mm3)"
	]
	Q6_prompt = multiple_choice_question(answer, "systemic findings", list_for_Q6)
	return Q6_prompt

def build_Q6a_prompt(answer, radiograph_day_number, discharge_day_number):
	findings_day = 0

	# yes means findings happened INSIDE 3 day window around radiograph_day_number
	if answer == "yes":
		# choose a random day number in the 3 day window, within the scope of the stay
		possible_findings_days = return_days_inside_3_day_window(radiograph_day_number, discharge_day_number)
		findings_day = random.choice(possible_findings_days)
	
	# no means findings happened OUTSIDE 3 day window
	else:
		possible_findings_days, discharge_day_number = get_days_outside_3_day_window(radiograph_day_number, discharge_day_number)
		findings_day = random.choice(possible_findings_days)

	Q6a_prompt = f"The systemic findings appeared on day number {findings_day}."
	return Q6a_prompt, discharge_day_number

def build_Q7_prompt(answer, radiograph_day_number, discharge_day_number):
	findings_day = 0

	# yes means findings happened INSIDE 3 day window around radiograph_day_number
	if answer == "yes":
		# choose a random day number in the 3 day window, within the scope of the stay
		possible_findings_days = return_days_inside_3_day_window(radiograph_day_number, discharge_day_number)
		findings_day = random.choice(possible_findings_days)
	
	# no means findings happened OUTSIDE 3 day window
	else:
		possible_findings_days, discharge_day_number = get_days_outside_3_day_window(radiograph_day_number, discharge_day_number)
		findings_day = random.choice(possible_findings_days)

	Q7_prompt = f"The pulmonary findings are noted as appearing on day number {findings_day}"
	return Q7_prompt, discharge_day_number

def build_Q7a_prompt(answer, age):
	pulmonary_findings_list = [
            "New onset of purulent sputum, change in character or quantity of sputum, or increased respiratory secretions",
            "New onset or worsening cough, or dyspnea, or tachypnea",
            "Rales (or crackles) or bronchial breath sounds",
            "Oxygen saturation that decreases following admission and reaches less than 94 percent"
        ]
	systemic_findings_list = [
            "Fever (> 38 degrees C)",
            "Leukopenia (<4000 WBC/mm3) or Leukocytosis (>12,000 WBC/mm3)"
        ]
	if " years" in age:
		age_parts = age.split()
		age_number = int(age_parts[0])
		if age_number > 70:
			systemic_findings_list.append("Decline in mental status")

	combined_findings_list = pulmonary_findings_list + systemic_findings_list

	if answer == "yes":
		day_num = random.choice([1, 2])
		num_to_select = random.randint(1, len(combined_findings_list))

		# choose some random findings
		selected_findings = random.sample(combined_findings_list, num_to_select)
		findings_together = ", ".join(selected_findings)
		Q7a_prompt = f"Pneumonia is documented as POA indicated by the presence of a finding from a chest radiograph and the following associated findings: {findings_together} on day number {day_num}."
	else:
		findings_together = ", ".join(combined_findings_list)
		Q7a_prompt = f"The record MUST NOT mention any of the following on day number 1 or day number 2: a chest radiograph, {findings_together}."

	return Q7a_prompt

def build_Q8_prompt(answer):
	pulmonary_findings_list = [
            "New onset of purulent sputum, change in character or quantity of sputum, or increased respiratory secretions",
            "New onset or worsening cough, or dyspnea, or tachypnea",
            "Rales (or crackles) or bronchial breath sounds",
            "Oxygen saturation that decreases following admission and reaches less than 94 percent"
        ]
	Q8_prompt = multiple_choice_question(answer, "pulmonary findings", pulmonary_findings_list)
	return Q8_prompt

# R9a covers whether or not major surgical procedure should be in record
# R9b covers whether or not ventilation should be in record
# if Q9 is yes, just randomly select whether or not to include aspiration too.
def build_Q9_prompt(answer):
	if answer == "yes":
		Q9_prompt = "The medical record MUST mention the occurrence of aspiration after admission but prior to the onset of pneumonia."
	if answer == "none":
		Q9_prompt = f"The medical record MUST NOT mention aspiration happening after admission but prior to the onset of pneumonia."

	return Q9_prompt

def build_R9a_prompt(answer):
	if answer == "yes":
		Q9a_prompt = "The medical record must mention the occurrence of a major surgical procedure prior to the onset of pneumonia."
	else:
		Q9a_prompt = "The medical record must not mention the occurrence of a major surgical procedure prior to the onset of pneumonia."
	return Q9a_prompt

def build_R9b_prompt(answer):
	if answer == "yes":
		Q9b_prompt = "The medical record must mention the occurrence of ventilation with tracheostomy or endotracheal tube prior to the onset of pneumonia."
	else:
		Q9b_prompt = "The medical record must not mention the occurrence of ventilation with tracheostomy or endotracheal tube prior to the onset of pneumonia."
	return Q9b_prompt

def build_Q10_prompt(answer):
	if answer == "yes":
		Q10_prompt = "The major surgical procedure WAS done with general endotracheal anasthesia."
	else:
		Q10_prompt = "The major surgical procedure WAS NOT done with general endotracheal anasthesia."
	return Q10_prompt

def build_Q11_prompt(answer):
	if answer == "yes":
		Q11_prompt = "The ventilation with tracheostomy or endotracheal tube occurred more than 2 days prior to the onset of pneumonia."
	else:
		Q11_prompt = "The ventilation with tracheostomy or endotracheal tube occured exactly 1 day before the onset of pneumonia."
	return Q11_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(hap_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(hap_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    patient_age = f"{str(random.randint(1, 99))} years"

    # create placeholders for variables that might get set / passed around between functions
    diagnosis_day_number = -1 # will be determined by functions
    radiograph_day_number = -1 # will be determined by functions; don't use for prompts (redundancy), only to pass between functions.

    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(hap_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQ1" in question_keys:
        ans = hap_prompt_qa_dict[num]["EQ1"]
        eq1_prompt, diagnosis_day_number = build_EQ1_prompt(ans, diagnosis_day_number)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = hap_prompt_qa_dict[num]["EQ2"]
        eq2_prompt, radiograph_day_number, diagnosis_day_number = build_EQ2_prompt(ans, discharge_day_number)
        list_of_prompts.append(eq2_prompt)
    if "R1" in question_keys:
        ans = hap_prompt_qa_dict[num]["R1"]
        r1_prompt, patient_age = build_R1_prompt(ans)
        list_of_prompts.append(r1_prompt)
    if "Q1" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q2" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "R2" in question_keys:
        ans = hap_prompt_qa_dict[num]["R2"]
        r2_prompt, patient_age = build_R2_prompt(ans)
        list_of_prompts.append(r2_prompt)
    if "Q5" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
    if "Q6" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans)
        list_of_prompts.append(q6_prompt)
    if "Q6a" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q6a"]
        q6a_prompt, discharge_day_number = build_Q6a_prompt(ans, radiograph_day_number, discharge_day_number)
        list_of_prompts.append(q6a_prompt)
    if "Q7" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q7"]
        q7_prompt, discharge_day_number = build_Q7_prompt(ans, radiograph_day_number, discharge_day_number)
        list_of_prompts.append(q7_prompt)
    if "Q7a" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q7a"]
        q7a_prompt = build_Q7a_prompt(ans, patient_age)
        list_of_prompts.append(q7a_prompt)
    if "Q8" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q8"]
        q8_prompt = build_Q8_prompt(ans)
        list_of_prompts.append(q8_prompt)
    if "Q9" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q9"]
        q9_prompt = build_Q9_prompt(ans)
        list_of_prompts.append(q9_prompt)
    if "R9a" in question_keys:
        ans = hap_prompt_qa_dict[num]["R9a"]
        r9a_prompt = build_R9a_prompt(ans)
        list_of_prompts.append(r9a_prompt)
    if "R9b" in question_keys:
        ans = hap_prompt_qa_dict[num]["R9b"]
        r9b_prompt = build_R9b_prompt(ans)
        list_of_prompts.append(r9b_prompt)
    if "Q10" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q10"]
        q10_prompt = build_Q10_prompt(ans)
        list_of_prompts.append(q10_prompt)
    if "Q11" in question_keys:
        ans = hap_prompt_qa_dict[num]["Q11"]
        q11_prompt = build_Q11_prompt(ans)
        list_of_prompts.append(q11_prompt)
    
    #######


    # after all build prompt functions that should be called are, add general prompts about the stay that might
    # not have been stated yet (remove duplicates at the end)
    list_of_prompts.append(f"The record should note that the patient was diagnosed with pneumonia on day number {diagnosis_day_number}.")
    list_of_prompts.append(f"Patient is {patient_age} old.")
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
        story_definition = generate_pdf_file_name(algo_str, num)  # Function to get filename
        story_prompt = story_prompts_dict.get(num, "")  # Retrieve prompt, default to empty if missing

        writer.writerow([story_definition, story_prompt])

import json
json_output_file = f"{algo_str}_prompts_{prompt_run}.json"
data = []
# Build JSON data
for num in story_numbers:
    story_definition = generate_pdf_file_name(algo_str, num)  # Function to get filename
    story_prompt = story_prompts_dict.get(num, "")  # Retrieve prompt, default to empty if missing

    data.append({
        "story_definition": story_definition,
        "story_prompt": story_prompt
    })
# Save to JSON file
with open(json_output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
