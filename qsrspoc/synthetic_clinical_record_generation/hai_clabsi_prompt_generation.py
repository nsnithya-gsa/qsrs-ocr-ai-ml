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
algo_str = "clabsi"
prompt_run = "1" # to generate a larger set of pdfs, increase this number and re-run. They'll be saved in a separate file instead of overwriting the first set.


clabsi_prompt_qa_dict = {}
clabsi_prompt_qa_dict[1] = {
    "EQR1": "no"
}
clabsi_prompt_qa_dict[2] = {
    "EQR1": "yes", # if yes, set insertion day to day 2 or 3, (saving 1 for if Q2=no) ensure discharge day is at least insertion + 3
    "EQ1": "no" # if no, set removal day to insertion day + 1
}
# PAGE 1 IS COVERED
clabsi_prompt_qa_dict[3] = {
    "EQR1": "yes", # if yes, set insertion day to day 2 or 3, (saving 1 for if Q2=no), ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "no"
}
clabsi_prompt_qa_dict[4] = {
    "EQR1": "yes", # if yes, set insertion day to day 2 or 3, (saving 1 for if Q2=no), ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "no" # if no, set pos blood day to day 1
}
clabsi_prompt_qa_dict[5] = {
    "EQR1": "yes", # if yes, set insertion day to day 2 or 3, (saving 1 for if Q2=no), ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "no" # if no, reset pos blood day to removal day + 2, update discharge day if needed
}
clabsi_prompt_qa_dict[6] = {
    "EQR1": "yes", # if yes, set insertion day to day 2 or 3, (saving 1 for if Q2=no), ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "yes", # JUMP TO PAGE 5
    "R2": "no", # SOME FLOWS SKIP R1; CODE R2 ACCORDINGLY
    "Q10": "yes" # prompt should say nec entercolitis documented on pos blood day - 1
}
# PAGE 2 IS COVERED
clabsi_prompt_qa_dict[7] = {
    "EQR1": "yes", # if yes, set insertion day to day 2 or 3, (saving 1 for if Q2=no), ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "yes", # JUMP TO PAGE 5
    "R2": "no", # SOME FLOWS SKIP R1; CODE R2 ACCORDINGLY
    "Q10": "no" # prompt should say record shouldn't mention nec entercolitis at all
}
clabsi_prompt_qa_dict[8] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "yes", # JUMP TO PAGE 5
    "R2": "yes", # SOME FLOWS SKIP R1; CODE R2 ACCORDINGLY
    "Q9": "no" # prompt should say record shouldn't mention postive cultures from any other body sites besides blood
}
clabsi_prompt_qa_dict[9] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "yes", # JUMP TO PAGE 5
    "R2": "yes", # SOME FLOWS SKIP R1; CODE R2 ACCORDINGLY
    "Q9": "yes", # prompt should say a positive culture from a different body site (unspecified) was collected on pos blood day
    "Q11": "yes", 
    "Q12": "no"
}
clabsi_prompt_qa_dict[10] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "yes", # JUMP TO PAGE 5
    "R2": "yes", # SOME FLOWS SKIP R1; CODE R2 ACCORDINGLY
    "Q9": "yes", # prompt should say a positive culture from a different body site (unspecified) was collected on pos blood day
    "Q11": "yes", 
    "Q12": "yes"
}
# PAGE 5 IS COVERED
clabsi_prompt_qa_dict[11] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "yes", # JUMP TO PAGE 5
    "R2": "yes", # SOME FLOWS SKIP R1; CODE R2 ACCORDINGLY
    "Q9": "yes", # prompt should say a positive culture from a different body site (unspecified) was collected on pos blood day
    "Q11": "no", 
    "Q13": "no"
}
clabsi_prompt_qa_dict[12] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "yes", # JUMP TO PAGE 5
    "R2": "yes", # SOME FLOWS SKIP R1; CODE R2 ACCORDINGLY
    "Q9": "yes", # prompt should say a positive culture from a different body site (unspecified) was collected on pos blood day
    "Q11": "no", 
    "Q13": "yes", # prompt that imaging study performed on pos blood day documented presence of infection at different body site
    "Q14": "no" # specify site location (for stories that don't reach Q14, let GPT generate info)
}
clabsi_prompt_qa_dict[13] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "yes", # JUMP TO PAGE 5
    "R2": "yes", # SOME FLOWS SKIP R1; CODE R2 ACCORDINGLY
    "Q9": "yes", # prompt should say a positive culture from a different body site (unspecified) was collected on pos blood day
    "Q11": "no", 
    "Q13": "yes", # prompt that imaging study performed on pos blood day documented presence of infection at different body site
    "Q14": "yes" # specify site location (for stories that don't reach Q14, let GPT generate info)
}
# PAGE 6 IS COVERED
clabsi_prompt_qa_dict[14] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "no",
    "Q5": "no"
}
clabsi_prompt_qa_dict[15] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "no",
    "Q5": "yes",
    "R1": "yes",
    "Q6": "none"
}
clabsi_prompt_qa_dict[16] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "no",
    "Q5": "yes",
    "R1": "yes",
    "Q6": "yes"
}
clabsi_prompt_qa_dict[17] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "no",
    "Q5": "yes",
    "R1": "no",
    "Q7": "none"
}
clabsi_prompt_qa_dict[18] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "no",
    "Q5": "yes",
    "R1": "no",
    "Q7": "yes",
    "Q8": "no"
}
clabsi_prompt_qa_dict[19] = {
    "EQR1": "yes", # if yes, set insertion day to day 1,2, or 3, ensure discharge day is at least insertion + 3
    "EQ1": "yes", # if yes, set removal day to insertion day + 3, ensure discharge day is at >= removal day
    "Q1": "yes",
    "Q2": "yes", # if yes, set pos blood day to insertion day + 3
    "Q3": "yes", # if yes, make no changes and return an empty string as prompt
    "Q4": "no",
    "Q5": "yes",
    "R1": "no",
    "Q7": "yes",
    "Q8": "yes"
}

def build_EQR1_prompt(answer):
    if answer == "yes":
        catheter_insertion_day = random.choice([2, 3])
        EQR1_prompt = f"Patient had a central venous catheter inserted on day number {catheter_insertion_day}."
    else:
        catheter_insertion_day = -1
        EQR1_prompt = f"The clinical record should make no mention of a central venous catheter." 
    return EQR1_prompt, catheter_insertion_day

# catheter insertion day is set in main program; this function sets removal day
def build_EQ1_prompt(answer, catheter_insertion_day, discharge_day):
    if answer == "yes":
        # last possible removal day is discharge day so there's a dependency between the variables
        catheter_removal_day = catheter_insertion_day + 3
        EQ1_prompt = f"The central line was removed on day number {catheter_removal_day}."
    else:
        catheter_removal_day = catheter_insertion_day + 1
        EQ1_prompt = f"The central line was removed on day number {catheter_removal_day}."
    # lastly, check to see if discharge day needs updating
    if discharge_day < catheter_removal_day:
        discharge_day = random.randint(catheter_removal_day, catheter_removal_day+5)
    return EQ1_prompt, catheter_removal_day, discharge_day

def build_Q1_prompt(answer):
    if answer == "yes":
        Q1_prompt = f"There was a blood culture drawn from the central line that resulted positive."
    else: 
        random_count = random.randint(1,4)
        variance = [
             f"{random_count} blood culture(s) were drawn from the central line and resulted negative."
             "There were no blood cultures taken from the central line."
        ]
        Q1_prompt = random.choice(variance)
    return Q1_prompt

# was positive culture drawn after catheter was in place for more than 2 days?
def build_Q2_prompt(answer, catheter_insertion_day, discharge_day):
    if answer == "yes":
        positive_culture_day = catheter_insertion_day + 3
        if discharge_day < positive_culture_day:
            discharge_day = random.randint(positive_culture_day+2, positive_culture_day+5)
        Q2_prompt = "" # if yes, we'll trigger Q2 and might need to update positive culture day so say nothing now
    else:
        positive_culture_day = 1 # at this point in the flowchart, we know cath was inserted on day 2 or 3
        # if no, we exit, so it's time to say what day the positive blood culture was drawn on
        Q2_prompt = f"The positive blood culture was drawn on day {positive_culture_day}."
    return Q2_prompt, positive_culture_day, discharge_day

#Was positive culture drawn while the central line catheter was in place OR within one day of the catheter removal? 
def build_Q3_prompt(answer, positive_culture_day, catheter_removal_day, discharge_day):
    if answer == "yes": # now declare what positive culture day is
        Q3_prompt = f"The positive blood culture was drawn on day {positive_culture_day}."
    else: 
        positive_culture_day = catheter_removal_day + 2
        if discharge_day < positive_culture_day:
            discharge_day = random.randint(positive_culture_day + 2, positive_culture_day + 7)
        Q3_prompt = f"The positive blood culture was drawn on day {positive_culture_day}."

    return Q3_prompt, positive_culture_day, discharge_day


def build_Q4_prompt(answer):
    pathogenic_bacteria = [
    "Streptococcus pneumoniae",
    "Neisseria meningitidis",
    "Yersinia pestis"
]
    commensal_bacteria = [
    "Staphylococcus epidermidis",
    "Corynebacterium spp.",
    "Propionibacterium acnes"    
    ]

    if answer == "yes":
        bacteria = random.choice(pathogenic_bacteria)
        Q4_prompt = f"The positive blood culture grew a recgonized pathogen named {bacteria}."
    else:
        bacteria = random.choice(commensal_bacteria)
        Q4_prompt = f"The positive blood culture did not grow a recgonized pathogen, instead growing common commensal named {bacteria}."
    return Q4_prompt


def build_Q5_prompt(answer, positive_culture_day):
    # either both on day positive_culture_day or two on day positive_culture_day and positive_culture_day + 1
    yes_prompts = [
        f"A second positive blood culture was also grown later on day {positive_culture_day}",
        f"A second positive blood culture was also grown on day {positive_culture_day+1}"
    ]
    if answer == "yes":
        Q5_prompt = random.choice(yes_prompts)
    else:
        Q5_prompt = "The record should not mention more than one positive blood cultures"
    return Q5_prompt

# max age for an umbilical catheter is 14 days; forcing minimum age of 1 month simplifies to only CVCs
# current story dicts only call R1 OR R2 (same question), never both, sometimes neither
def build_R1_prompt(answer):
    if answer == "yes":
        patient_age = random.randint(1, 11)
        age_type = "months"
    else:
        patient_age = random.randint(1,60)
        age_type = "years"
    R1_prompt = f"The patient is {patient_age} {age_type} old."
    return R1_prompt, patient_age, age_type

def build_Q6_prompt(answer):
    clabsi_inf_symptoms = [
        "Fever > 38°C",
        "Chills",
        "Hypotension",
        "Apnea",
        "Bradycardia"
    ]
    if answer == "yes":
        Q6_prompt = multiple_choice_question(answer, "CLABSI infection symptoms", clabsi_inf_symptoms)
    else:
        symptom_str = ", ".join(clabsi_inf_symptoms)
        Q6_prompt = f"The clinical record should NOT mention any of the following symptoms: {symptom_str}."
    return Q6_prompt


def build_Q7_prompt(answer):
    clabsi_adult_symptoms = [
        "Fever > 38°C",
        "Chills",
        "Hypotension"
    ]
    if answer == "yes":
        Q7_prompt = multiple_choice_question(answer, "adult CLABSI symptoms", clabsi_adult_symptoms)
    else:
        symptom_str = ", ".join(clabsi_adult_symptoms)
        Q7_prompt = f"The clinical record should NOT mention any of the following symptoms: {symptom_str}."
    return Q7_prompt

def build_Q8_prompt(answer, positive_culture_day, discharge_day):
    if answer == "yes":
        symptom_window_days = return_days_inside_3_day_window(positive_culture_day, discharge_day)
        symptom_day = random.choice(symptom_window_days)
        Q8_prompt = f"The clinical record should note those CLABSI symptoms on day number {symptom_day}."
    else:
        symptom_window_days, discharge_day = get_days_outside_3_day_window(positive_culture_day, discharge_day)
        symptom_day = random.choice(symptom_window_days)
        Q8_prompt = f"The clinical record should note those CLABSI symptoms on day number {symptom_day}."
    
    return Q8_prompt

# max age for an umbilical catheter is 14 days; forcing minimum age of 1 month simplifies to only CVCs
# current story dicts only call R1 OR R2 (same question), never both, sometimes neither
def build_R2_prompt(answer):
    if answer == "yes":
        patient_age = random.randint(1, 11)
        age_type = "months"
    else:
        patient_age = random.randint(1,60)
        age_type = "years"
    R2_prompt = f"The patient is {patient_age} {age_type} old."
    return R2_prompt, patient_age, age_type


def build_Q10_prompt(answer, positive_culture_day):
    if answer == "yes":
        # NEC could have occurred on or before the positive culture day
        nec_day = positive_culture_day - 1
        Q10_prompt = f"Necrotizing enterocolitis (NEC) was noted on day {nec_day}"
    else:
        Q10_prompt = "The clinical record should NOT mention necrotizing enterocolitis (NEC)."
    
    return Q10_prompt


def build_Q9_prompt(answer, positive_culture_day):
    if answer == "yes":
        Q9_prompt = f"A positive culture from a site other than blood was obtained on day {positive_culture_day}."
    else:
        Q9_prompt = "No positive culture from a body site other than blood was obtained during the patient's stay."
    return Q9_prompt


def build_Q11_prompt(answer):
    if answer == "yes":
        Q11_prompt = f"The culture that was not taken from the blood was positive for the same microorganism as the blood culture."
    else:
         Q11_prompt = "The culture that was not taken from the blood was not positive for the same bacteria as the blood culture."
    return Q11_prompt

# for simplicity, don't allow urine
def build_Q12_prompt(answer):
    # List of common culture sites
    yes_culture_sites = [
        "wound",
        "throat",
        "nose",
        "stool",
        "ear",
        "vaginal",
        "sinus"
    ]

    if answer == "yes":
        yes_culture = random.choice(yes_culture_sites)
        Q12_prompt = f"The matching culture material is from the patient's {yes_culture} specimen site."
    
    else:
        Q12_prompt = f"The matching culture material is from the patient's sputum."

    return Q12_prompt

def build_Q13_prompt(answer, positive_culture_day):
    if answer == "yes":
        imaging_day = positive_culture_day
        Q13_prompt = f"An imaging study documented the presence of infection on day {imaging_day}."
    else:
        Q13_prompt = "The record should not document any imaging studies."
    return Q13_prompt


def build_Q14_prompt(answer):
    # List of **EXCLUDED** body sites that **DO NOT QUALIFY** for a yes answer to Q14
    excluded_sites = [
        "Eye", "Ear", "Mastoid", "Oral cavity", "Sinus", "Pharynx", "Larynx",
        "Epiglottis", "Lung", "Endometrium", "Breast", "Burn site",
        "Circumcision", "Skin/soft tissue"
    ]
    # List of **INCLUDED** body sites that **QUALIFY** for a yes answer to Q14
    included_sites = [
        "Bone", "Joint", "Intracerebral disc", "Spinal abscess", "Endocarditis",
        "Gastrointestinal tract (excluding appendicitis, gastroenteritis, and C. difficile)",
        "Gallbladder", "Biliary ducts", "Liver", "Spleen", "Pancreas",
        "Peritoneum", "Sub-diaphragmatic space", "Urinary system"
    ]
    # there are no coded stories where Q14 is yes but Q9 is no, so this won't introduce contradictions
    if answer == "yes":
        yes_location = random.choice(included_sites)
        Q14_prompt = f"The imaging study documented infection at the following qualifying body site: {yes_location}."
    else:
        no_location = random.choice(excluded_sites)
        Q14_prompt = f"The imaging study documented infection at {no_location}."
    return Q14_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(clabsi_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

# for clabsi this will be numbers 1 through 19
story_numbers = list(clabsi_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(4, 8)
    # If R1 / R2 answer = "no" this changes to months old, from 1 to 11 (this avoids umbilical catheter complexity)
    patient_age = random.randint(2, 99) # R1 and R2 both check if >= 365 days
    age_type = "years"

    # create placeholders for variables that might get set / passed around between functions

    # to avoid excess complexity, we assume the catheter is both inserted and removed during the stay
    catheter_insertion_day_number = -1 # DO NOT USE IF EQR1 = "no"
    catheter_removal_day_number = -1 # to avoid excess complexity, we assume the catheter is removed during the stay
    positive_culture_day_number = -1 # DO NOT USE IF EQR1 = "no"

    # for story 1, prompts will be ["EQR1"], for 2 ["EQR1", "EQ1"], for 3 ["EQR1, "EQ1", "Q1"], etc
    question_keys = list(clabsi_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "EQR1" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["EQR1"]
        eqr1_prompt, catheter_insertion_day_number = build_EQR1_prompt(ans)
        list_of_prompts.append(eqr1_prompt)
    if "EQ1" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["EQ1"]
        eq1_prompt, catheter_removal_day_number, discharge_day_number = build_EQ1_prompt(ans, catheter_insertion_day_number, discharge_day_number)
        list_of_prompts.append(eq1_prompt) # list_of_prompts looks like ["Patient had a CVC in place", "The central line was in place for 4 days]
    if "Q1" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q1"]
        q1_prompt = build_Q1_prompt(ans)
        list_of_prompts.append(q1_prompt)
        # list_of_prompts looks like ["Patient had a CVC in place", "The central line was in place for 4 days", "There were no blood cultures taken from the central line."]
    if "Q2" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q2"] 
        q2_prompt, positive_culture_day_number, discharge_day_number = build_Q2_prompt(ans, catheter_insertion_day_number, discharge_day_number)
        list_of_prompts.append(q2_prompt)
    if "Q3" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q3"]
        q3_prompt, positive_culture_day_number, discharge_day_number = build_Q3_prompt(ans, positive_culture_day_number, catheter_removal_day_number, discharge_day_number)
        list_of_prompts.append(q3_prompt)
    if "Q4" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "Q5" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans, positive_culture_day_number)
        list_of_prompts.append(q5_prompt)
    if "R1" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["R1"]
        r1_prompt, patient_age, age_type = build_R1_prompt(ans)
        list_of_prompts.append(r1_prompt)
    if "Q6" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans)
        list_of_prompts.append(q6_prompt)
    if "Q7" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q7"]
        q7_prompt = build_Q7_prompt(ans)
        list_of_prompts.append(q7_prompt)
    if "Q8" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q8"]
        q8_prompt = build_Q8_prompt(ans, positive_culture_day_number, discharge_day_number)
        list_of_prompts.append(q8_prompt)
    if "R2" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["R2"]
        r2_prompt, patient_age, age_type = build_R2_prompt(ans)
        list_of_prompts.append(r2_prompt)
    if "Q10" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q10"]
        q10_prompt = build_Q9_prompt(ans, positive_culture_day_number)
        list_of_prompts.append(q10_prompt)
    if "Q9" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q9"]
        q9_prompt = build_Q10_prompt(ans, positive_culture_day_number)
        list_of_prompts.append(q9_prompt)
    if "Q11" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q11"]
        q11_prompt = build_Q11_prompt(ans)
        list_of_prompts.append(q11_prompt)
    if "Q12" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q12"]
        q12_prompt = build_Q12_prompt(ans)
        list_of_prompts.append(q12_prompt)
    if "Q13" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q13"]
        q13_prompt = build_Q13_prompt(ans, positive_culture_day_number)
        list_of_prompts.append(q13_prompt)
    if "Q14" in question_keys:
        ans = clabsi_prompt_qa_dict[num]["Q14"]
        q14_prompt = build_Q14_prompt(ans)
        list_of_prompts.append(q14_prompt)
    #######


    # after all build prompt functions that should be called are, add general prompts about the stay that might
    # not have been stated yet (remove duplicates at the end)
    list_of_prompts.append(f"Patient is {patient_age} {age_type} old.")
    list_of_prompts.append(f"Patient was discharged on day number {discharge_day_number}.")
    cath_was_in_place = clabsi_prompt_qa_dict[num]["EQR1"]
    if cath_was_in_place == True:
        list_of_prompts.append("The central venous catheter was inserted on day number {catheter_insertion_day_number}")
        list_of_prompts.append("The central venous catheter was removed on day number {catheter_removal_day_number}")

    # list_of_prompts looks like ["Patient had a CVC in place", "The central line was in place for 4 days", "There were no blood cultures taken from the central line."]
    prompt_string = " ".join(list_of_prompts)
    # now prompt_string is "Patient had a CVC in place. The central line was in place for 4 days. There were no blood cultures taken from the central line. Patient is 8 years old."
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
