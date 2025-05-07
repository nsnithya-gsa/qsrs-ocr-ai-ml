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

uti_prompt_qa_dict = {}
uti_prompt_qa_dict[1] = {
    "EQ1": "no"
}
uti_prompt_qa_dict[2] = {
	"EQ1": "yes",
    "EQ2": "no"
}
uti_prompt_qa_dict[3] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "yes"
}
uti_prompt_qa_dict[4] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "no",
	"Q1": "none",
	"Q4": "no"
}
uti_prompt_qa_dict[5] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "no",
	"Q1": "none",
	"Q4": "yes",
	"Q5": "no"
	
}
uti_prompt_qa_dict[6] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "no",
	"Q1": "none",
	"Q4": "yes",
	"Q5": "yes",
	"Q6": "yes"

}
uti_prompt_qa_dict[7] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "no",
	"Q1": "none",
	"Q4": "yes",
	"Q5": "yes",
	"Q6": "no",
	"Q7": "yes"
}
uti_prompt_qa_dict[8] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "no",
	"Q1": "none",
	"Q4": "yes",
	"Q5": "yes",
	"Q6": "no",
	"Q7": "no"
	
}
uti_prompt_qa_dict[9] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "no",
	"Q1": "yes",
	"Q3": "no"
}
uti_prompt_qa_dict[10] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "no",
	"Q1": "yes",
	"Q3": "yes"
}
uti_prompt_qa_dict[11] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "yes",
	"Q2": "none"
	
}
uti_prompt_qa_dict[12] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "no",
	"EQR1": "no",
	"R1": "yes",
	"Q2": "yes"

}
uti_prompt_qa_dict[13] = {
	"EQ1": "yes",
	"EQ2": "yes",
	"EQ3": "yes"
}
#was a urine culture done?
def build_EQ1_prompt(answer):
	if answer == "yes":
		EQ1_prompt = f"The patient had a urine culture performed."
	else:
		EQ1_prompt = f"The patient did not have a urine culture performed."
	return EQ1_prompt


def build_EQ2_prompt(answer):
	list_eq2 = [
        "The urine culture was positive, identifying 1 species of bacteria with ≥ 10^5 CFU/ml.",
        "The urine culture was positive, identifying 2 species of bacteria, one of which had ≥ 10^5 CFU/ml.",
        "The urine culture was positive, identifying 2 species of bacteria, both of which had ≥ 10^5 CFU/ml."
	]
	if answer == "yes":
		EQ2_prompt = random.choice(list_eq2)   
	else:
		EQ2_prompt = "The clinical record should NOT note any positive urine cultures."
	return EQ2_prompt


def build_EQ3_prompt(answer, dis_day):
    if dis_day <=3:
        dis_day = random.randint(4, 8)
    if answer == "yes":
        day_taken = random.randint(1,2)
        EQ3_prompt = f"The positive urine specimen was obtained on day {day_taken}."
    else:        
        day_taken = random.randint(3, dis_day)
        EQ3_prompt = f"The positive urine specimen was obtained on day {day_taken}."
    return EQ3_prompt, day_taken, dis_day

def build_EQR1_prompt(answer):
	if answer == "yes":
		EQR1_prompt = f"Patient had a urinary catheter present during time urine specimen was taken."
	else:
		EQR1_prompt = f"Patient did not have a urinary catheter present during time urine specimen was taken."
	return EQR1_prompt

def build_R1_prompt(answer):
	if answer == "yes":
		patient_age_days = random.randint(20,365)
		R1_prompt = f"Patient is {patient_age_days} days old."
	else:
		patient_age_adult = random.randint(1,70)
		R1_prompt = f"Patient is {patient_age_adult} years old."
	return R1_prompt

def build_Q1_prompt(answer):
    list_for_Q1 = [
           "Fever (> 38 degrees C)",
            "Supranubic tenderness",
            "Costovertebral angle pain or tenderness",
            "Dysuria",
            "Urgency",
            "Frequency"
	]
    Q1_prompt = multiple_choice_question(answer, "UTI symptoms", list_for_Q1)
    return Q1_prompt

def build_Q2_prompt(answer):
    list_for_Q2 = [
          "Fever (> 38 degrees C)",
            "Hypothermia (< 36 degrees C)",
            "Apnea",
            "Bradycardia",
            "Lethargy",
            "Vomiting"
	]
    Q2_prompt = multiple_choice_question(answer, "UTI symptoms", list_for_Q2)
    return Q2_prompt

def build_Q3_prompt(answer, day_taken, dis_day):
    if answer == "yes":
        valid_days = return_days_inside_3_day_window(day_taken, dis_day)
        symptom_day = random.choice(valid_days)
    else:
        valid_days, dis_day = get_days_outside_3_day_window(day_taken, dis_day)
        symptom_day = random.choice(valid_days)
    Q3_prompt = f"Symptoms were noted on day {symptom_day}."
    return Q3_prompt, dis_day



def build_Q4_prompt(answer, day_taken, dis_day):
    if answer == "yes":
        valid_days = return_days_inside_3_day_window(day_taken, dis_day)
        blood_culture_day = random.choice(valid_days)
        Q4_prompt = f"A positive blood culture was obtained on day {blood_culture_day}."
    else:
        valid_days, dis_day = get_days_outside_3_day_window(day_taken, dis_day)
        blood_culture_day = random.choice(valid_days)
    Q4_prompt = f"A positive blood culture was obtained on day {blood_culture_day}."
    return Q4_prompt, blood_culture_day, dis_day


def build_Q5_prompt(answer, blood_culture_day):
    if answer == "yes":
        # Randomly determine if one or both bacteria are the same
        match_type = random.choice(["one", "both"])
        Q5_prompt = (
            f"The blood culture obtained on day {blood_culture_day} contained {match_type} of "
            f"the same bacteria as identified in the urine culture."
        )
    else:
        Q5_prompt = (
            f"The blood culture obtained on day {blood_culture_day} did not contain the same bacteria "
            f"as identified in the urine culture."
        )
    return Q5_prompt

def build_Q6_prompt(answer):
    if answer == "yes":
        pathogenic_bacteria = ["Escherichia coli", "Klebsiella pneumoniae", "Pseudomonas aeruginosa"]
        # Randomly select a pathogenic bacterium
        matching_bacterium = random.choice(pathogenic_bacteria)
        Q6_prompt = f"The matching bacterium identified was {matching_bacterium}, which is considered a pathogen."
    else:
        common_commensals = ["Staphylococcus epidermidis", "Corynebacterium species", "Micrococcus species"]
        # Randomly select a common commensal
        matching_bacterium = random.choice(common_commensals)
        Q6_prompt = f"The matching bacterium identified was {matching_bacterium}, which is considered a common commensal."
    return Q6_prompt


def build_Q7_prompt(answer):
    if answer == "yes":
        # Randomly determine the number of matching cultures (at least 2)
        num_matching_cultures = random.randint(2, 4)
        Q7_prompt = f"The patient had {num_matching_cultures} matching blood cultures drawn on separate occasions."
    else:
        Q7_prompt = "The patient did not have at least 2 matching blood cultures drawn on separate occasions."
    return Q7_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(uti_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(uti_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    # patient_age = random.randint(1, 99)

    # create placeholders for variables that might get set / passed around between functions
    urine_sample_taken_day_number = -1
    blood_culture_day = -1

    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(uti_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQ1" in question_keys:
        ans = uti_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "EQ2" in question_keys:
        ans = uti_prompt_qa_dict[num]["EQ2"]
        eq2_prompt = build_EQ2_prompt(ans)
        list_of_prompts.append(eq2_prompt)
    if "EQ3" in question_keys:
        ans = uti_prompt_qa_dict[num]["EQ3"]
        eq3_prompt, urine_sample_taken_day_number, discharge_day_number = build_EQ3_prompt(ans, discharge_day_number)
        list_of_prompts.append(eq3_prompt)
    if "EQR1" in question_keys:
        ans = uti_prompt_qa_dict[num]["EQR1"]
        eqr1_prompt = build_EQR1_prompt(ans)
        list_of_prompts.append(eqr1_prompt)
    if "R1" in question_keys:
        ans = uti_prompt_qa_dict[num]["R1"]
        r1_prompt = build_R1_prompt(ans)
        list_of_prompts.append(r1_prompt)
    if "Q1" in question_keys:
        ans = uti_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
    if "Q2" in question_keys:
        ans = uti_prompt_qa_dict[num]["Q2"]
        q2_prompt = build_Q2_prompt(ans)
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        ans = uti_prompt_qa_dict[num]["Q3"]
        q3_prompt, discharge_day_number = build_Q3_prompt(ans, urine_sample_taken_day_number, discharge_day_number)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = uti_prompt_qa_dict[num]["Q4"]
        q4_prompt, blood_culture_day, discharge_day_number = build_Q4_prompt(ans, urine_sample_taken_day_number, discharge_day_number)
        list_of_prompts.append(q4_prompt)
    if "Q5" in question_keys:
        ans = uti_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans, blood_culture_day)
        list_of_prompts.append(q5_prompt)
    if "Q6" in question_keys:
        ans = uti_prompt_qa_dict[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans)
        list_of_prompts.append(q6_prompt)
    if "Q7" in question_keys:
        ans = uti_prompt_qa_dict[num]["Q7"]
        q7_prompt = build_Q7_prompt(ans)
        list_of_prompts.append(q7_prompt)
    #######


    # after all build prompt functions that should be called are, add general prompts about the stay that might
    # not have been stated yet (remove duplicates at the end)
    #list_of_prompts.append(f"Patient is {patient_age} years old.")
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


