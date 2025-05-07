
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

covid_prompt_qa_dict = {}
covid_prompt_qa_dict[1] = {
    "EQ1": "no"
}
covid_prompt_qa_dict[2] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "no",
    "Q1c": "no",
    "Q1d": "no",
    "LC1": "no"
}
covid_prompt_qa_dict[3] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "no",
    "Q1c": "no",
    "Q1d": "no",
    "LC1": "yes",
    "Q4a": "no"
}
covid_prompt_qa_dict[4] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "no",
    "Q1c": "no",
    "Q1d": "no",
    "LC1": "yes",
    "Q4a": "yes"
}
covid_prompt_qa_dict[5] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "no",
    "Q1c": "no",
    "Q1d": "yes",
    "Q2a": "no",
    "Q3b": "yes"
}
covid_prompt_qa_dict[6] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "no",
    "Q1c": "no",
    "Q1d": "yes",
    "Q2a": "no",
    "Q3b": "no"
}
covid_prompt_qa_dict[7] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "no",
    "Q1c": "no",
    "Q1d": "yes",
    "Q2a": "yes",
    "Q3a": "no"
}
covid_prompt_qa_dict[8] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "no",
    "Q1c": "no",
    "Q1d": "yes",
    "Q2a": "yes",
    "Q3a": "yes"
}
covid_prompt_qa_dict[9] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "no",
    "Q1c": "yes"
}
covid_prompt_qa_dict[10] = {
    "EQ1": "yes",
    "Q1a":"no",
    "Q1b": "yes"
}
covid_prompt_qa_dict[11] = {
    "EQ1": "yes",
    "Q1a": "yes"
}

# Is the patient chart from this time period? -> On or after January 20, 2020
def build_EQ1_prompt(answer):
    if answer == "yes":
        # requirement: (chart_year > 2020) or (chart_year == 2020 and chart_month >= 1 and chart_day >= 20):
        chart_year = random.randint(2020, 2024)
        chart_month = random.randint(2, 12) # skip January altogether to avoid the complexity of before-or-after January 20, but only if the year is 2020
        chart_day = random.randint(1, 28) # avoid month length issues and stick to days 1-28
    else:
        chart_year = random.randint(2017, 2019)
        chart_month = random.randint(1, 12)
        chart_day = random.randint(1, 28) # avoid month lenght issues and stick to days 1-28

    chart_date = f"{chart_month:02}/{chart_day:02}/{chart_year}"
    EQ1_prompt = f"The discharge day for this record must be {chart_date}."
    return EQ1_prompt

#Did the patient have a positive viral COVID-19 test result during the admission process (in the ED or as an outpatient)?
def build_Q1a_prompt(answer):
    list_for_Q1a = [
        "Patient tested positive for covid in the ED prior to admission.",
        "Patient tested positive for covid in an outpatient facility, then was sent to the hospital."
     ]
    if answer == "yes":
        Q1a_prompt = random.choice(list_for_Q1a)
    else:
        Q1a_prompt = "Patient did not test positive for covid in the admission process (in the ED, or outpatient before admission)."
    return Q1a_prompt

# Did the patient have a documented positive viral COVID-19 test result within 30 days prior to admission?
def build_Q1b_prompt(answer):
    if answer == "yes":
        within_thirty_before_pos_prior = random.randint(1, 30)  # Randomly select a day within 30 days before admission
        Q1b_prompt = f"Patient had a documented positive COVID-19 test result {within_thirty_before_pos_prior} days prior to admission."
    else:
        Q1b_prompt = "There patient reported no positive COVID-19 at-home test result within 30 days prior to admission."
    return Q1b_prompt

# Did the patient have a documented positive viral COVID-19 test result during the first 14 days of their inpatient stay?
def build_Q1c_prompt(answer, discharge_day):
    inp_cov_test_fourteen = -1
    if answer == "yes":
        # Randomly select a day within first 13 inpatient days (day 14 shows up in too many questions;
        # let's not allow it and save the headache) - also, if the stay is short, we've got to reduce the possibilities with min()
        inp_cov_test_fourteen = random.randint(1, min(13, discharge_day))  
        Q1c_prompt = f"Patient tested positive for COVID-19 on inpatient day {inp_cov_test_fourteen}."
    else:
        Q1c_prompt = "No positive COVID-19 test result was recorded during the first 14 days of inpatient stay."
    
    return Q1c_prompt

# Was the patient admitted for a scheduled surgery after a positive viral COVID-19 test result?
# This is only triggered if Q1a,b,c or d is yes (meaning the positive test result is already documented.)
def build_Q2a_prompt(answer):
    # Scheduled surgery examples
    list_for_Q2a = [
        "Laparoscopic Cholecystectomy",
        "Inguinal Hernia Repair",
        "Total Knee Replacement"
    ]
    if answer == "yes":
        surgery_name = random.choice(list_for_Q2a)
        Q2a_prompt = (
            f"The patient was admitted for a scheduled surgery: {surgery_name}, performed on a day after the already noted positive covid-19 test result."
        )
    else:
        Q2a_prompt = "The patient's reason for admission was NOT a scheduled surgery."
    return Q2a_prompt



# Did the Emergency Department notes or admission history refer to a positive viral COVID-19 test result during the 30 days prior to admission?
def build_Q1d_prompt(answer):
    if answer == "yes":
        days_prior = random.randint(1, 30)  # Randomly select a day within 30 days before admission
        Q1d_prompt = f"Emergency Department notes or admission history referenced a positive COVID-19 test result {days_prior} days prior to admission."
    else:
        Q1d_prompt = "There was no mention of a positive COVID-19 test result in Emergency Department notes or admission history within 30 days prior to admission."
    return Q1d_prompt



# Q3b: Did the patient test negative for COVID-19 in their most recent viral test before or during the admission process?
# Assumption: Q1a's answer was no. This is safe based on the dictionaries.
def build_Q3b_prompt(answer):
    if answer == "yes":
        Q3b_prompt = "The patient had a negative covid test during admission."
    else:
        Q3b_prompt = "There is no record of a negative COVID-19 test taken prior to or during admission."
    return Q3b_prompt


# Length of stay: Is the patient's stay 14 days or more?
# All this function needs to do is make sure the discharge day matches the answer and doesn't contradict previous answers
def build_LC1_prompt(answer):
    if answer == "yes":
        # length_of_stay must >= 14, so discharge day should be at least 15
        discharge_day = random.randint(15, 25)
    else:
        discharge_day = random.randint(1, 13)
    return discharge_day


# Q3a: Did the patient test negative for COVID-19 in their most recent viral test prior to scheduled surgery?
def build_Q3a_prompt(answer):
    if answer == "yes":
        # Ensure the test happens at least 1 day before surgery - no story dicts have Q1c AND Q3a == yes, so this is simple
        Q3a_prompt = "The record must note an additional COVID-19 test performed immediately before the scheduled surgery that was positive."
    else:
        Q3a_prompt = "There is no record of a negative COVID-19 test before the scheduled surgery."
    return Q3a_prompt

# Did the patient have a first positive inpatient COVID-19 viral test result on day 15 or later of this stay?
# only triggered if LC1 = yes (discharge day is at least 15)
def build_Q4a_prompt(answer, discharge_day):
    if answer == "yes": # safe to assume discharge day is at least 15
        # random.int has been cranky if both parameters are the same number
        if discharge_day == 15:
            first_inpatient_pos = discharge_day 
        else:
            first_inpatient_pos = random.randint(15, discharge_day)
        Q4a_prompt = f"The patient had their first positive inpatient COVID-19 test on day number {first_inpatient_pos}"
    else:
        # If no, the positive test is already covered by Q1c so we don't need to add anything to the prompt
        Q4a_prompt = ""
    
    return Q4a_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(covid_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(covid_prompt_qa_dict.keys())
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
    question_keys = list(covid_prompt_qa_dict[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "LC1" in question_keys: # this question is almost last in flowchart, but if it's in a story, it should set discharge_day_number from the start
        ans = covid_prompt_qa_dict[num]["LC1"]
        discharge_day_number = build_LC1_prompt(ans)
    if "EQ1" in question_keys:
        ans = covid_prompt_qa_dict[num]["EQ1"]
        eq1_prompt = build_EQ1_prompt(ans)
        list_of_prompts.append(eq1_prompt)
    if "Q1a" in question_keys:
        q1a_prompt = build_Q1a_prompt(ans)
        list_of_prompts.append(q1a_prompt)
    if "Q1b" in question_keys: 
        ans = covid_prompt_qa_dict[num]["Q1b"]
        q1b_prompt = build_Q1b_prompt(ans)
        list_of_prompts.append(q1b_prompt)
    if "Q1c" in question_keys:
        ans = covid_prompt_qa_dict[num]["Q1c"]
        q1c_prompt = build_Q1c_prompt(ans, discharge_day_number)
        list_of_prompts.append(q1c_prompt)
    if "Q1d" in question_keys:
        ans = covid_prompt_qa_dict[num]["Q1d"]
        q1d_prompt = build_Q1d_prompt(ans)
        list_of_prompts.append(q1d_prompt)
    if "Q2a" in question_keys:
        ans = covid_prompt_qa_dict[num]["Q2a"]
        q2a_prompt = build_Q2a_prompt(ans)
        list_of_prompts.append(q2a_prompt)
    if "Q3a" in question_keys:
        ans = covid_prompt_qa_dict[num]["Q3a"]
        q3a_prompt = build_Q3a_prompt(ans)
        list_of_prompts.append(q3a_prompt)
    if "Q3b" in question_keys:
        ans = covid_prompt_qa_dict[num]["Q3b"]
        q3b_prompt = build_Q3b_prompt(ans)
        list_of_prompts.append(q3b_prompt)
    if "Q4a" in question_keys:
        ans = covid_prompt_qa_dict[num]["Q4a"]
        q4a_prompt = build_Q4a_prompt(ans, discharge_day_number)
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