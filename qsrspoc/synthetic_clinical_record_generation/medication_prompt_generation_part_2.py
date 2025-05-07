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

medication_prompt_qa_dict_part_2 = {}

medication_prompt_qa_dict_part_2[1] = {
    "R2": "no",
    "Q23": "no"
}

medication_prompt_qa_dict_part_2[2] = {
    "R2": "yes",
    "Q16": "no"
}

medication_prompt_qa_dict_part_2[3] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "no",
    "Q43": "yes",
    "Q44": "yes",
    "Q45": "yes",
    "Q46": "no",
    "R6": "no",
    "Q49": "no"
}

medication_prompt_qa_dict_part_2[4] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "no",
    "Q43": "yes",
    "Q44": "yes",
    "Q45": "no"
}

medication_prompt_qa_dict_part_2[5] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "no",
    "Q43": "yes",
    "Q44": "none"
}

medication_prompt_qa_dict_part_2[6] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "no",
    "Q43": "no"
}

medication_prompt_qa_dict_part_2[7] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "yes"
}

medication_prompt_qa_dict_part_2[8] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "yes",
    "Q46": "no",
    "R6": "yes",
    "Q48": "yes"
}

medication_prompt_qa_dict_part_2[9] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "yes",
    "Q46": "no",
    "R6": "yes",
    "Q48": "no"
}

medication_prompt_qa_dict_part_2[10] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "yes",
    "Q46": "yes",
    "Q47": "yes"
    "R6": "no"
}

medication_prompt_qa_dict_part_2[11] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "yes",
    "Q46": "yes",
    "Q47": "no"
}

medication_prompt_qa_dict_part_2[12] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "yes",
    "Q46": "no",
    "R6": "no",
    "Q49": "yes",
    "Q51a": "yes",
    "Q51b": "yes"
}

medication_prompt_qa_dict_part_2[13] = {
    "R2": "yes",
    "Q16": "yes",
    "Q42": "yes",
    "Q46": "no",
    "R6": "no",
    "Q49": "yes",
    "Q51a": "yes",
    "Q51b": "no"
}

medication_prompt_qa_dict_part_2[14] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "none",
    "R3": "yes",
    "Q25": "yes"
}

medication_prompt_qa_dict_part_2[15] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "none",
    "R3": "yes",
    "Q25": "no"
}

medication_prompt_qa_dict_part_2[16] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "no",
    "R8": "no",
    "Q59": "no"
}

medication_prompt_qa_dict_part_2[17] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "no",
    "Q53": "no"
}

medication_prompt_qa_dict_part_2[18] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "no",
    "Q53": "yes",
    "Q54": "none"
}

medication_prompt_qa_dict_part_2[19] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "no",
    "Q53": "yes",
    "Q54": "yes",
    "Q55": "yes"
}

medication_prompt_qa_dict_part_2[20] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "no",
    "Q53": "yes",
    "Q54": "yes",
    "Q55": "no"
}

medication_prompt_qa_dict_part_2[21] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "no",
    "R8": "yes",
    "Q58": "yes"
}

medication_prompt_qa_dict_part_2[22] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "no",
    "R8": "yes",
    "Q58": "no"
}

medication_prompt_qa_dict_part_2[23] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "yes",
    "Q57": "yes"
}

medication_prompt_qa_dict_part_2[24] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "yes",
    "Q57": "no"
}

medication_prompt_qa_dict_part_2[25] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "no",
    "R8": "no",
    "Q59": "yes",
    "Q61a": "yes",
    "Q61b": "yes",
    "RZ": "yes"
}

medication_prompt_qa_dict_part_2[26] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "no",
    "R8": "no",
    "Q59": "yes",
    "Q61a": "yes",
    "Q61b": "yes",
    "RZ": "no"
}

# if this is no, we skip to Q23 (if it's yes, we eventually get to Q23 too)
def build_R2_prompt(answer):
    if answer == "yes":
        R2_prompt = "The patient received fresh frozen plasma during the stay. They did not have an operating room procedure during the stay."
    else:
        R2_prompt = "The record should make no mention of the patient receiving fresh frozen plasma or whole blood or red blood cell infusion."
    return R2_prompt

# we already know: warfarin was given on day 3; fresh frozen plasma was given
def build_Q16_prompt(answer):
    if answer == "yes":
        Q16_prompt = "The patient received the fresh frozen plasma on day 3 BEFORE the initial dose of warfarin, which also occurred on day 3."
    else:
        Q16_prompt = "The patient received the fresh frozen plasma on day 1."
    return Q16_prompt

def build_Q42_prompt(answer):
    if answer == "yes":
        Q42_prompt = "There was bleeding present on admission."
    else:
        Q42_prompt = "There was no bleeding present on admission."
    return Q42_prompt

def build_Q43_prompt(answer):
    if answer == "yes":
        Q43_prompt = "There was bleeding that began during the stay, after the dose of warfarin on day 3."
    else:
        Q43_prompt = "The record shouldn't note any bleeding that began during the stay."
    return Q43_prompt

def build_Q44_prompt(answer):
    site_list = [
        "gastrointestinal bleeding",
        "genitourinary bleeding",
        "pulmonary bleeding",
        "hematoma",
        "intracranial bleeding"
    ]
    if answer == "yes":
        rand_site = random.choice(site_list)
        Q44_prompt = f"The bleeding that developed was {rand_site}."
    else:
        all_sites = ", ".join(site_list)
        Q44_prompt = f"The record must not mention bleeding of any of the following types: {all_sites}."
    return Q44_prompt

# we already know: fresh frozen plasma was given on day 3
def build_Q45_prompt(answer):
    if answer == "yes":
        Q45_prompt = "This bleeding developed on day 3."
    else:
        Q45_prompt = "This bleeding developed on day 1."
    return Q45_prompt

def build_Q46_prompt(answer):
    if answer == "yes":
        Q46_prompt = "The record must describe that the patient required emergency measures to sustain life."
    else:
        Q46_prompt = "The record must not mention cardiac arrest, emergency measures to sustain life, or a call to a rapid response team for the patient's stay."
    return Q46_prompt

def build_Q47_prompt(answer, discharge_day):
    if answer == "yes":
        Q47_prompt = "Emergency measures to sustain life were required on day 4."
    else:
        discharge_day = random.randint(7, 10)
        Q47_prompt = "Emergency measures to sustain life were required on day 6."
    return Q47_prompt, discharge_day

def build_R6_prompt(answer):
    if answer == "yes":
        R6_prompt = "The patient's discharge status is died."
    else:
        R6_prompt = "The patient's discharge status was NOT died."
    return R6_prompt

def build_Q48_prompt(answer, discharge_day):
    if answer == "yes":
        Q48_prompt = "The patient's death occurred on day 4."
    else:
        discharge_day = 6
        Q48_prompt = "The patient's death occurred on day 6."
    return Q48_prompt, discharge_day

def build_Q49_prompt(answer):
    if answer == "yes":
        Q49_prompt = "The patient's hemoglobin level was reported to be 14 on day 2 before the initial dose of warfarin was administered."
    else:
        Q49_prompt = "The record should not note that the patient's hemoglobin levels were checked at all during the stay."
    return Q49_prompt

# The value for this is currently part of the yes case prompt from Q49
def build_Q51a_prompt():
    Q51a_prompt = ""
    return Q51a_prompt

# we already know: fresh frozen plasma was given on day 3
# the value for this is determined by the answer for RX
def build_Q51b_prompt():
    Q51b_prompt = ""
    return Q51b_prompt

# yes means that hemoglobin measured on day 4 was at least 5 g/dL lower than the level on day 2 from Q49
def build_RX_prompt(answer):
    if answer == "yes":
        RX_prompt = "The patient's hemoglobin level was reported to be 6 g/dL on day 4."
    else:
        RX_prompt = "The patient's hemoglobin level was reported to be 15 g/dL on day 4."
    return RX_prompt

def build_Q23_prompt(answer):
    if answer == "yes":
        Q23_prompt = "Low molecular weight heparin (LMWH) was administered to the patient."
    else:
        Q23_prompt = "The record must not mention Low molecular weight heparin (LMWH), bivalent or univalent thrombin inhibiotir, or direct or inderect Xa inhibitor."
    return Q23_prompt

def build_Q24_prompt(answer):
    if answer == "yes":
        Q24_prompt = "The patient received protamine after the initial dose of low molecular weight heparin."
    else:
        Q24_prompt = "The record must not mention desmopressin acetate, recombinant factor VIIa, antifibrionlytic therapy, or protamine."
    return Q24_prompt

# placeholder - this is a check that will currently always be true, because fresh frozen plasma was administered
def build_R3_prompt():
    R3_prompt = ""
    return R3_prompt

# we already know: fresh frozen plasma was given on day 3
# this asks: did the low molecular weight heparin happen before that?
def build_Q25_prompt(answer):
    if answer == "yes":
        Q25_prompt = "The low molecular weight heparin (LMWH) was administered on day 2."
    else:
        Q25_prompt = "The low molecular weight heparin (LMWH) was administered on day 4." # goes to page 8 / part 3 - so exits part 2
    return Q25_prompt

def build_Q52_prompt(answer):
    if answer == "yes":
        Q52_prompt = "The record must note bleeding was present on admission."
    else:
        Q52_prompt = "The record must NOT note bleeding was present on admission."
    return Q52_prompt

# we already know: low molecular weight heparin dose was given on day 2
def build_Q53_prompt(answer):
    if answer == "yes":
        Q53_prompt = "The record must note that bleeding began on day 3."
    else:
        Q53_prompt = "The record should not note bleeding at any point in the stay."
    return Q53_prompt

def build_Q54_prompt(answer):
    site_list = [
        "gastrointestinal bleeding",
        "genitourinary bleeding",
        "pulmonary bleeding",
        "hematoma",
        "intracranial bleeding"
    ]
    if answer == "yes":
        rand_site = random.choice(site_list)
        Q54_prompt = f"The bleeding that began on day 3 was {rand_site}."
    else:
        all_sites = ", ".join(site_list)
        Q54_prompt = f"The record must not mention any of the following: {all_sites}."
    return Q54_prompt

# we already know: fresh frozen plasma was given on day 3
# question asks: did bleeding develop within 1 day before or after (a list of things including FFP)
# yes case is taken care of in Q53 prompt
def build_Q55_prompt(answer):
    if answer == "yes":
        Q55_prompt = ""
    else:
        Q55_prompt = "This bleeding developed on day 1, after admission."
    return Q55_prompt

def build_Q56_prompt(answer):
    if answer == "yes":
        Q56_prompt = "The record must describe that the patient required emergency measures to sustain life."
    else:
        Q56_prompt = "The record must not mention cardiac arrest, emergency measures to sustain life, or a call to a rapid response team for the patient's stay."
    return Q56_prompt

# we already know: fresh frozen plasma was given on day 3
def build_Q57_prompt(answer, discharge_day):
    if answer == "yes":
        Q57_prompt = "The patient required these emergency measures on day 4."
    else:
        discharge_day = random.randint(8, 12)
        Q57_prompt = "The patient required these emergency measures on day 6."
    return Q57_prompt, discharge_day

def build_R8_prompt(answer):
    if answer == "yes":
        R8_prompt = "The patient died during their stay. The discharge status is died."
    else:
        R8_prompt = "The patient's discharge status in the record cannot be died."
    return R8_prompt

# we already know: fresh frozen plasma was given on day 3
def build_Q58_prompt(answer, discharge_day):
    if answer == "yes":
        Q58_prompt = "The patient died on day 4."
    else:
        discharge_day = 6
        Q58_prompt = "The patient died on day 6."
    return Q58_prompt, discharge_day

# we already know: warfarin was given on day 3
def build_Q59_prompt(answer):
    if answer == "yes":
        Q59_prompt = "The patient's hemoglobin level was measured at 14 g/dL on day 3, before the initial dose of warfarin later on day 3."
    else:
        Q59_prompt = "The record should NOT mention the patient's hemoblobin levels at all."
    return Q59_prompt

def build_Q61a_prompt():
    Q61a_prompt = "" # this data is handled by yes prompt from Q59
    return Q61a_prompt

# The value here is determined by the answer to RZ
def build_Q61b_prompt():
    Q61b_prompt = ""
    return Q61b_prompt

# we already know: fresh frozen plasma was given on day 3
def build_RZ_prompt(answer):
    if answer == "yes":
        RZ_prompt = "The patient's hemoglobin level was measured at 8 g/dL on day 4."
    else:
        RZ_prompt = "The patient's hemoglobin level was measured at 21 g/dL on day 4."
    return RZ_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(medication_prompt_qa_dict_part_2[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(medication_prompt_qa_dict_part_2.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

for num in story_numbers:

    list_of_prompts = [] # you can't change strings, so we'll buid a list of prompts based
    # on what question keys are in the story dictionary, add some basics about age, etc, 
    # and at the very end, join them together into a string and save it in the story_prompts_dict[num].

    # set up basic data about the stay that might be changed by functions
    discharge_day_number = random.randint(5, 8)
    patient_age = random.randint(1, 99)

    # create placeholders for variables that might get set / passed around between functions

    # collect into a list the questions that are part of this story by their key (EQR1, Q3, etc)
    question_keys = list(medication_prompt_qa_dict_part_2[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.

    # prime the prompt list with data from part 1
    list_of_prompts.append("Warfarin was administered to the patient on day 3 of the stay. The patient's INR values stayed below 5.0 for the entire stay.")
    list_of_prompts.append("The record should NOT mention vitamin K or prothrombin complex concentrate.")


    if "R2" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["R2"]
        r2_prompt = build_R2_prompt(ans)
        list_of_prompts.append(r2_prompt)
    if "Q16" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q16"]
        q16_prompt = build_Q16_prompt(ans)
        list_of_prompts.append(q16_prompt)
    if "Q42" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q42"]
        q42_prompt = build_Q42_prompt(ans)
        list_of_prompts.append(q42_prompt)
    if "Q43" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q43"]
        q43_prompt = build_Q43_prompt(ans)
        list_of_prompts.append(q43_prompt)
    if "Q44" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q44"]
        q44_prompt = build_Q44_prompt(ans)
        list_of_prompts.append(q44_prompt)
    if "Q45" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q45"]
        q45_prompt = build_Q45_prompt(ans)
        list_of_prompts.append(q45_prompt)
    if "Q46" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q46"]
        q46_prompt = build_Q46_prompt(ans)
        list_of_prompts.append(q46_prompt)
    if "Q47" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q47"]
        q47_prompt, discharge_day_number = build_Q47_prompt(ans, discharge_day_number)
        list_of_prompts.append(q47_prompt)
    if "R6" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["R6"]
        r6_prompt = build_R6_prompt(ans)
        list_of_prompts.append(r6_prompt)
    if "Q48" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q48"]
        q48_prompt, discharge_day_number = build_Q48_prompt(ans, discharge_day_number)
        list_of_prompts.append(q48_prompt)
    if "Q49" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q49"]
        q49_prompt = build_Q49_prompt(ans)
        list_of_prompts.append(q49_prompt)
    if "Q51a" in question_keys:
        q51a_prompt = build_Q51a_prompt()
        list_of_prompts.append(q51a_prompt)
    if "Q51b" in question_keys:
        q51b_prompt = build_Q51b_prompt()
        list_of_prompts.append(q51b_prompt)
    if "RX" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["RX"]
        rx_prompt = build_RX_prompt(ans)
        list_of_prompts.append(rx_prompt)
    if "Q23" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q23"]
        q23_prompt = build_Q23_prompt(ans)
        list_of_prompts.append(q23_prompt)
    if "Q24" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q24"]
        q24_prompt = build_Q24_prompt(ans)
        list_of_prompts.append(q24_prompt)
    if "R3" in question_keys:
        r3_prompt = build_R3_prompt()
        list_of_prompts.append(r3_prompt)
    if "Q25" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q25"]
        q25_prompt = build_Q25_prompt(ans)
        list_of_prompts.append(q25_prompt)
    if "Q52" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q52"]
        q52_prompt = build_Q52_prompt(ans)
        list_of_prompts.append(q52_prompt)
    if "Q53" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q53"]
        q53_prompt = build_Q53_prompt(ans)
        list_of_prompts.append(q53_prompt)
    if "Q54" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q54"]
        q54_prompt = build_Q54_prompt(ans)
        list_of_prompts.append(q54_prompt)
    if "Q55" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q55"]
        q55_prompt = build_Q55_prompt(ans)
        list_of_prompts.append(q55_prompt)
    if "Q56" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q56"]
        q56_prompt = build_Q56_prompt(ans)
        list_of_prompts.append(q56_prompt)
    if "Q57" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q57"]
        q57_prompt, discharge_day_number = build_Q57_prompt(ans, discharge_day_number)
        list_of_prompts.append(q57_prompt)
    if "R8" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["R8"]
        r8_prompt = build_R8_prompt(ans)
        list_of_prompts.append(r8_prompt)
    if "Q58" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q58"]
        q58_prompt, discharge_day_number = build_Q58_prompt(ans, discharge_day_number)
        list_of_prompts.append(q58_prompt)
    if "Q59" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["Q59"]
        q59_prompt = build_Q59_prompt(ans)
        list_of_prompts.append(q59_prompt)
    if "Q61a" in question_keys:
        q61a_prompt = build_Q61a_prompt()
        list_of_prompts.append(q61a_prompt)
    if "Q61b" in question_keys:
        q61b_prompt = build_Q61b_prompt()
        list_of_prompts.append(q61b_prompt)
    if "RZ" in question_keys:
        ans = medication_prompt_qa_dict_part_2[num]["RZ"]
        rz_prompt = build_RZ_prompt(ans)
        list_of_prompts.append(rz_prompt)
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