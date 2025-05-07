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


############################################################## prompt dictionary


cauti_prompt_qa_dict = {}
cauti_prompt_qa_dict[1] = {
    "EQR1": "no"
}
cauti_prompt_qa_dict[2] = {
    "EQR1": "yes",
    "EQ1": "no"
}
cauti_prompt_qa_dict[3] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "EQ2": "no"
}

cauti_prompt_qa_dict[4] = {
    "EQR1": "yes", 
    "EQ1": "yes",
    "EQ2": "yes",
    "Q1": "yes",
    "Q2a": "yes"
}

cauti_prompt_qa_dict[5] = {
    "EQR1": "yes", 
    "EQ1": "yes",
    "EQ2": "yes",
    "Q1": "yes",
    "Q2a": "no"
}

cauti_prompt_qa_dict[6] = {
    "EQR1": "yes", 
    "EQ1": "yes",
    "EQ2": "yes",
    "Q1": "none",
    "Q2": "yes"
}
cauti_prompt_qa_dict[7] = {
    "EQR1": "yes", 
    "EQ1": "yes",
    "EQ2": "yes",
    "Q1": "none",
    "Q2": "none",
    "Q3": "no"
}


#check to see if urinary catheter is in place
def build_EQR1_prompt(answer):
    catheter_insertion_day = -1
    if answer == "yes":
        catheter_insertion_day = random.randint (1,3)
        EQR1_prompt =f"A catheter was inserted on day {catheter_insertion_day}."
    else:
        EQR1_prompt = f"The record should have no mention of a urinary catheter at all."

    return EQR1_prompt, catheter_insertion_day

#EQ1 Was the urinary catheter in place for more than 2 days prior to obtaining such positive urine specimen
def build_EQ1_prompt(answer, catheter_insertion_day, discharge_day):
    if answer == "yes":
        soonest_day = catheter_insertion_day + 2
        if discharge_day < soonest_day + 3:
            discharge_day = random.randint(soonest_day + 3, soonest_day + 6)
        latest_day = discharge_day
        positive_specimen_day = random.randint(soonest_day, latest_day)
        EQ1_prompt = f"A urine specimen that tested positive for infection was collected on day number {positive_specimen_day}."
    else:
        soonest_day = 1
        latest_day = catheter_insertion_day + 1
        if discharge_day < catheter_insertion_day + 2:
            discharge_day = random.randint(catheter_insertion_day + 2, soonest_day + 5)
        positive_specimen_day = random.randint(soonest_day, latest_day)
        EQ1_prompt = f"A urine specimen that tested positive for infection was collected on day number {positive_specimen_day}."
    return EQ1_prompt, positive_specimen_day, discharge_day

# EQ2 was the positive specimen obtained while catheter in place or the day after removal
def build_EQ2_prompt(answer, catheter_insertion_day, discharge_day, positive_specimen_day):
    if answer == "yes":
            catheter_removal_day = random.randint(positive_specimen_day-1, discharge_day )
            ##catheter_removal_day = any day after catheter_insertion_day but before or on the day of positive specimen day
            EQ2_prompt = f" The catheter was removed on day {catheter_removal_day}."

    # if answer is no, catheter WAS removed at minimum 2 days before positive test
    # at this point in the flowchart, WE CAN ASSUME POSITIVE SPECIMEN DAY IS AT LEAST CATHETER INSERTION DAY +2
    else: 
        catheter_removal_day = random.randint (catheter_insertion_day, positive_specimen_day - 2)
        EQ2_prompt = f"The catheter was removed on day {catheter_removal_day}."
      
    return EQ2_prompt, catheter_removal_day


# multiple choice question
def build_Q1_prompt(answer):
    list_for_Q1 = [
            "Fever (> 38 degrees C)",
            "Suprapubic tenderness",
            "Costovertebral angle pain or tenderness"
        ]
    Q1_prompt = multiple_choice_question(answer, "uti symptoms", list_for_Q1)
    return Q1_prompt

# which if any were noted after the catheter was removed or within 1 day after its removal?
def build_Q2_prompt(answer, catheter_removal_day, discharge_day):
    list_for_Q2 = [
            "Urgency",
            "Frequency",
            "Dysuria"
    ]
    if answer == "yes":
        rand_symptom = random.choice(list_for_Q2)
        if discharge_day <= catheter_removal_day + 1:
            discharge_day = random.randint(catheter_removal_day + 2, catheter_removal_day + 4)
        symptom_day = catheter_removal_day + 1 # for simplicity, the symptoms always happen the day after removal (for yes answer)
        Q2_prompt = f"The record must note that the patient experienced {rand_symptom} on day {symptom_day}."
    else: 
        all_symptom_str = ", ".join(list_for_Q2)
        Q2_prompt = f"The record must not note any of the following on or after day {catheter_removal_day}: {all_symptom_str}."
    return Q2_prompt, discharge_day

#CAUTI.Q2a:Did the symptoms appear within 3 days before or after the positive urine culture?
def build_Q2a_prompt(answer, positive_specimen_day, discharge_day):
    if answer == "yes":
        window_day_list = return_days_inside_3_day_window(positive_specimen_day, discharge_day)
        symptom_start_day = random.choice(window_day_list)
    else:
        window_day_list, discharge_day = get_days_outside_3_day_window(positive_specimen_day, discharge_day)
        symptom_start_day = random.choice(window_day_list)
    Q2a_prompt = f"The symptoms appeared on day number {symptom_start_day}."
    return Q2a_prompt, discharge_day

def build_Q3_prompt(answer, positive_specimen_day, discharge_day):
    if answer == "yes":
        window_day_list = return_days_inside_3_day_window(positive_specimen_day, discharge_day)
        positive_blood_culture_day = random.choice(window_day_list)
        Q3_prompt = f"A blood specimen that cultured positive was collected on day number {positive_blood_culture_day}."
    else:
        Q3_prompt = "The clinical record should make no mention of any positive blood cultures."
    return Q3_prompt

def build_Q4_prompt(answer):
    if answer == "yes":
         Q4_prompt=f"The patient's blood tested positive for the same bacteria that tested positive in the urine."
    else:
        # if the answer is not yes, we exit the algorithm without proceeding to Q5 - just hard code in the bacteria names for simplicity
        Q4_prompt= f"The patient's blood tested positive for Lactobacillus crispatus, a different bacteria than what tested positive in the urine, which was Staphylococcus aureus."
    return Q4_prompt

#was the bacteria a pathogen?
def build_Q5_prompt(answer):
    commensal_list = [
        "Lactobacillus crispatus",
        "Corynebacterium urealyticum"
    ]
    pathogenic_list = [
        "Escherichia coli",
        "Staphylococcus aureus"
    ]
    if answer == "yes":
        matching_bacteria = random.choice(pathogenic_list)
    else:
        matching_bacteria = random.choice(commensal_list)
    Q5_prompt = f"The patient's urine and blood both tested positive for {matching_bacteria}."
    return Q5_prompt, matching_bacteria

#were at least 2 matching blood cultures drawn on separate occasions?
def build_Q6_prompt(answer, matching_bacteria):
    if answer == "yes":
        num_matching_draws = random.randint (2,5)
        Q6_prompt = f"The patient's blood culture tested positive for {matching_bacteria} on {num_matching_draws} separate blood draws. "
    else:
        Q6_prompt=f"The record should not mention more than one blood draw or blood culture."
    return Q6_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(cauti_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(cauti_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    patient_age = random.randint(1, 99)

    # create placeholders for variables that might get set / passed around between functions
    catheter_insertion_day_number = -1
    positive_urine_specimen_day_number = -1
    catheter_removal_day_number = -1
    matching_bacteria = ""

    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(cauti_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQR1" in question_keys:
        ans = cauti_prompt_qa_dict[num]["EQR1"]
        eqr1_prompt, catheter_insertion_day_number = build_EQR1_prompt(ans)
        list_of_prompts.append(eqr1_prompt)
    if "EQ1" in question_keys:
        ans = cauti_prompt_qa_dict[num]["EQ1"]
        eq1_prompt, positive_urine_specimen_day_number, discharge_day_number = build_EQ1_prompt(ans, catheter_insertion_day_number, discharge_day_number)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = cauti_prompt_qa_dict[num]["EQ2"]
        eq2_prompt, catheter_removal_day_number = build_EQ2_prompt(ans, catheter_insertion_day_number, discharge_day_number, positive_urine_specimen_day_number)
        list_of_prompts.append(eq2_prompt)
    if "Q1" in question_keys:
        ans = cauti_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q2" in question_keys:
        ans = cauti_prompt_qa_dict[num]["Q2"]
        q2_prompt, discharge_day_number = build_Q2_prompt(ans, catheter_removal_day_number, discharge_day_number)
        list_of_prompts.append(q2_prompt)
    if "Q2a" in question_keys:
        ans = cauti_prompt_qa_dict[num]["Q2a"]
        q2a_prompt, discharge_day_number = build_Q2a_prompt(ans, positive_urine_specimen_day_number, discharge_day_number)
        list_of_prompts.append(q2a_prompt)
    if "Q3" in question_keys:
        ans = cauti_prompt_qa_dict[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans, positive_urine_specimen_day_number, discharge_day_number)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = cauti_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "Q5" in question_keys:
        ans = cauti_prompt_qa_dict[num]["Q5"]
        q5_prompt, matching_bacteria = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
    if "Q6" in question_keys:
        ans = cauti_prompt_qa_dict[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans, matching_bacteria)
        list_of_prompts.append(q6_prompt)
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