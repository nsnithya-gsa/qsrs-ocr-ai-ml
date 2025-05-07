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

surgery_prompt_qa_dict = {}

surgery_prompt_qa_dict[1] = {
    "EQR1": "no",
    "EQ1": "none"
}

surgery_prompt_qa_dict[2] = {
    "EQR1": "yes",
    "EQ1": "none"
}

# case 1: operating room procedure with anesthesia
surgery_prompt_qa_dict[3] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "one", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "yes",
    "Q9": "yes",
    "Q10": "yes",
    "Q11": "yes",
    "R1": "yes",
    "Q12": "no",
    "Q13": "yes",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "not-one" # end
}

surgery_prompt_qa_dict[4] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "one", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "yes",
    "Q9": "yes",
    "Q10": "yes",
    "Q11": "yes",
    "R1": "yes",
    "Q12": "no",
    "Q13": "none",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "one",
    "R6": "no",
    "R7": "yes", # only one OR AND died
    "Q14a": "sooner"
}

surgery_prompt_qa_dict[5] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "one", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "yes",
    "Q9": "yes",
    "Q10": "yes",
    "Q11": "yes",
    "R1": "yes",
    "Q12": "no",
    "Q13": "yes",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "one",
    "R6": "no",
    "R7": "yes", # only one OR AND died
    "Q14a": "later"
}

surgery_prompt_qa_dict[6] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "one", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "yes",
    "Q9": "yes",
    "Q10": "yes",
    "Q11": "yes",
    "R1": "yes",
    "Q12": "yes",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "one",
    "R6": "no",
    "R7": "no", # only one OR (per EQ2) but didn't die
    "R8": "no"
}

surgery_prompt_qa_dict[7] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "two", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "none",
    "Q9": "none",
    "Q10": "none",
    "Q11": "yes",
    "R1": "yes",
    "Q12": "no",
    "Q13": "yes",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "one",
    "R6": "no",
    "R7": "no", # only one OR (per EQ2) but didn't die
    "R8": "no"
} # PAGE 3 AND 4 ARE DONE

surgery_prompt_qa_dict[8] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "two", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "none",
    "Q9": "none",
    "Q10": "none",
    "Q11": "yes",
    "R1": "no",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "one",
    "R6": "yes",
    "Q14b": "one"
}

surgery_prompt_qa_dict[9] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "two", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "none",
    "Q9": "none",
    "Q10": "none",
    "Q11": "yes",
    "R1": "no",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "one",
    "R6": "yes",
    "Q14b": "not-one"
}

surgery_prompt_qa_dict[10] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "three", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "none",
    "Q9": "none",
    "Q10": "none",
    "Q11": "none",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "one",
    "R6": "no",
    "R7": "no",
    "R8": "yes",
    "Q14c": "yes"
}

surgery_prompt_qa_dict[11] = {
    "EQR1": "yes",
    "EQ1": "or-ane",
    "EQR2": "yes",
    "EQ2": "three", # R6-R8 on page 5 have branches for 1, 2, 3
    "Q1": "ane",
    "Q2": "yes", # non-branching placeholder
    "Q3": "none", # come back to cover page 2 Q3a,4,5,6,7
    "Q8": "none",
    "Q9": "none",
    "Q10": "none",
    "Q11": "none",
    "R3": "yes", # this is "no" when EQ1 isn't or-ane
    "Q14": "one",
    "R6": "no",
    "R7": "no",
    "R8": "yes",
    "Q14c": "no"
} # PAGE 5 IS COVERED AND ALL POSSIBLE ANSWERS FOR EQ2. NOW DO EQ1 = OR-PROC, DO PAGE 6

surgery_prompt_qa_dict[12] = {
    "EQR1": "yes",
    "EQ1": "or-proc",
    "EQR2": "yes",
    "EQ2": "one",
    "Q1": "proc",
    "Q3": "return",
    "Q4": "yes"
}

surgery_prompt_qa_dict[13] = {
    "EQR1": "yes",
    "EQ1": "or-proc",
    "EQR2": "yes",
    "EQ2": "one",
    "Q1": "proc",
    "Q3": "object",
    "Q5": "yes"
}

surgery_prompt_qa_dict[14] = {
    "EQR1": "yes",
    "EQ1": "or-proc",
    "EQR2": "yes",
    "EQ2": "one",
    "Q1": "proc",
    "Q3": "incorrect",
    "Q6": "implant",
    "Q7": "yes" # non-branching place-holder
}

surgery_prompt_qa_dict[15] = {
    "EQR1": "yes",
    "EQ1": "or-proc",
    "EQR2": "yes",
    "EQ2": "one",
    "Q1": "proc",
    "Q3": "incorrect",
    "Q6": "not-implant"
}

surgery_prompt_qa_dict[16] = {
    "EQR1": "yes",
    "EQ1": "or-proc",
    "EQR2": "yes",
    "EQ2": "one",
    "Q1": "proc",
    "Q3": "organ",
    "Q3a": "yes" # non-branching place-holder
}

surgery_prompt_qa_dict[17] = {
    "EQR1": "yes",
    "EQ1": "or-proc",
    "EQR2": "yes",
    "EQ2": "one",
    "Q1": "proc",
    "Q3": "none",
    "Q8": "none",
    "Q9": "none",
    "Q10": "none",
    "Q11": "none",
    "R1": "no",
    "R3": "no",
    "R4": "yes",
    "Q15": "yes" # non-branching place-holder
}

surgery_prompt_qa_dict[18] = {
    "EQR1": "yes",
    "EQ1": "or-proc",
    "EQR2": "yes",
    "EQ2": "one",
    "Q1": "proc",
    "Q3": "none",
    "Q8": "none",
    "Q9": "none",
    "Q10": "none",
    "Q11": "none",
    "R1": "no",
    "R3": "no",
    "R4": "yes",
    "Q15": "yes" # non-branching place-holder
}

def build_EQR1_prompt(answer):
    if answer == "yes":
        EQ1_prompt = "The patient had an operating room procedure during the stay."
    else:
        EQ1_prompt = "The record must NOT mention any operating room procedure as part of the patient's stay."
    return EQ1_prompt

def build_EQ1_prompt(answer):
    if answer == "or-ane":
        "The record MUST note that the patient's operating room procedure involved anesthesia - and anesthesia only, no procedural sedation."
    if answer == "or-proc":
        "The record MUST note that the patient's operating room procedure involved procedural sedation - and procedural sedation only, no anesthesia."
    else: # answer is "none"
        EQ1_prompt = "The record must NOT mention anesthesia or procedural sedation as part of the patient's stay."
    return EQ1_prompt

# currently no need to add to prompts or change any values here
def build_EQR2_prompt(answer):
    if answer == "yes":
        EQR2_prompt = ""
    else:
        EQR2_prompt = ""
    return EQR2_prompt

def build_EQ2_prompt(answer):
    if answer == "one":
        EQ2_prompt = "The record MUST note that the patient had ONLY ONE operating room procedure."
    if answer == "two":
        EQ2_prompt = "The record MUST note that the patient had TWO operating room procedures during the stay."
    if answer == "three":
        EQ2_prompt = "The record MUST note that the patient had THREE operating room procedures during the stay."
    return EQ2_prompt

# currently no need to add to prompts or change any values here because of EQ1 and dict stories - no need for both to ever be used
def build_Q1_prompt(answer):
    if answer == "ane":
        Q1_prompt = ""
    if answer == "proc":
        Q1_prompt = ""
    return Q1_prompt

def build_Q2_prompt():
    q2_list = [
        "general",
        "regional - epidural",
        "regional - spinal",
        "regional - peripheral nerve blocks",
        "local",
        "topical"
    ]
    rand_ane_type = random.choice(q2_list)
    Q2_prompt = f"The record must note that the type of anesthesia used was {rand_ane_type}."
    return Q2_prompt

def build_Q3_prompt(answer):
    if answer == "return":
        Q3_prompt = "The record must include that the patient had an unplanned return to the operating room"
    if answer == "object":
        Q3_prompt = "The record must include that after the OR procedure was complete, a retained object was discovered by development of symptoms followed by imaging."
    if answer == "incorrect":
        Q3_prompt = "The record must note that an incorrect OR procedure was performed but must NOT mention an implant."
    if answer == "organ":
        Q3_prompt = "The record must note that during the OR procedure, a normal organ that had been otherwise healthy and functional had to be removed."
    else: # none
        Q3_prompt = "The record must not mention any of the following: unplanned return to OR, discovery of a retained object, an incorrect OR procedure being performed, or an unplanned removal of an organ."
    return Q3_prompt

def build_Q4_prompt():
    reason_list = [
        "bleeding",
        "revision of operative site"
    ]
    rand_reason = random.choice(reason_list)
    Q4_prompt = f"The record must state that the reason for the unplanned return to the OR was {rand_reason}."
    return Q4_prompt

def build_Q5_prompt():
    type_list = [
        "sponge",
        "needle",
        "towel",
        "clamp"
    ]
    rand_type = random.choice(type_list)
    Q5_prompt = f"The record must state that the retained object was a {rand_type}."
    return Q5_prompt

def build_Q6_prompt(answer):
    if answer == "not-implant":
        wrong_list = [
            "incorrect side",
            "incorrect site",
            "incorrect procedure"
        ]
        rand_wrong = random.choice(wrong_list)
        Q6_prompt = f"The record must explain that the incorrect OR procedure involved an {rand_wrong} and provide details."
    else: # implant
        Q6_prompt = "The record must state that the incorrect OR procedure involved an incorrect implant."
        return Q6_prompt
    
def build_Q7_prompt():
    reason_list = [
        "of a mistake",
        "the correct implant was not available"
    ]
    rand_reason = random.choice(reason_list)
    Q7_prompt = f"The reason for the incorrect implant was because {rand_reason}."
    return Q7_prompt

def build_Q3a_prompt():
    reason_list = [
        "due to unintended injury to the organ during the procedure",
        "due to mistaken, unnecessary removal of the organ"
    ]
    rand_reason = random.choice(reason_list)
    Q3a_prompt = f"The record must state that the unplanned organ removal was {rand_reason}."
    return Q3a_prompt

def build_Q8_prompt(answer):
    or_injury_list = [
        "dental injury",
        "ocular injury",
        "injury to spinal cord",
        "unintended laceration"
    ]
    if answer == "yes":
        rand_injury = random.choice(or_injury_list)
        Q8_prompt = f"The following injury occurred during the OR procedure / anesthesia: {rand_injury}."
    else:
        Q8_prompt = f"The record MUST NOT mention any injuries occurring during the OR procedure / anesthesia."
    return Q8_prompt

def build_Q9_prompt(answer):
    or_event_list = [
        "unintended awareness",
        "high spinal requiring intubation and/or assisted ventilation",
        "malignant hyperthermia"
    ]
    if answer == "yes":
        rand_event = random.choice(or_event_list)
        Q9_prompt = f"During the OR procedure / anesthesia, the record MUST note that {rand_event} occurred."
    else:
        or_event_list.append("unplanned conversion to general anesthesia from regional, local, or procedural sedation")
        all_event_str = ", ".join(or_event_list)
        Q9_prompt = f"The record MUST NOT mention any of the following events happening during the OR procedure / anesthesia: {all_event_str}."
    return Q9_prompt

def build_Q10_prompt(answer):
    q10_list = [
        "dehischence, flap or wound failure or disruption, or graft failure",
        "unintended blockage, obstruction, or ligation",
        "post-dural puncture headache",
    ]
    if answer == "yes":
        rand_event = random.choice(q10_list)
        Q10_prompt = f"After the operating room procedure, the following complication happened: {rand_event}."
    else:
        all_str = ", ".join(q10_list)
        Q10_prompt = f"The record MUST NOT mention any of the following happening during the patient's stay: {all_str}."
    return Q10_prompt

def build_Q11_prompt(answer):
    ane_comp_list = [
        "acute myocardial infarction (AMI) during or within 48 hours of operation or administration of anesthesia",
        "cardiac arrest during or within 24 hours of operation or administration of anesthesia",
        "any cardiac or circulatory event during or within 48 hours of operation or administration of anesthesia",
        "central nervous system event (such as CVA, seizures, coma) during or within 48 hours of operation or administration of anesthesia"
    ]
    if answer == "yes":
        rand_event = random.choice(ane_comp_list)
        Q11_prompt = f"The medical record must note that the patient experienced {rand_event}."
    else:
        all_str = ", ".join(ane_comp_list)
        Q11_prompt = f"The medical record MUST NOT state the patient experienced any of the following: {all_str}."
    return Q11_prompt

def build_R1_prompt(answer):
    if answer == "yes":
        R1_prompt = "The record must note that ventilator WAS initiated on day 1 of the stay."
    else:
        R1_prompt = "The record must NOT note that ventilator was initiated during the stay."
    return R1_prompt

def build_Q12_prompt(answer):
    if answer == "yes":
        Q12_prompt = "The record must note that the patient was on ventilator support prior to surgery."
    else:
        Q12_prompt = "The record must not note that ventilator was initiated during the stay."
    return Q12_prompt

def build_Q13_prompt(answer):
    vent_list = [
        "reinstitution of ventilator support following discontinuance after operation",
        "continuous ventilator support for more than 7 days following operation"
    ]
    if answer == "yes":
        # allowing the 7-day option would introduce the only requirement for tracking surgery and discharge day with no benefit
        Q13_prompt = "The record must note that reinstitution of ventilator support following discontinuance after operation occurred."
    else:
        all_vent_str = ", ".join(vent_list)
        Q13_prompt = f"The record must not note either of the following as occurring: {all_vent_str}."
    return Q13_prompt

# currently no need to add to prompts or change any values here - all information is already in prompts
def build_R3_prompt(answer):
    if answer == "yes":
        R3_prompt = ""
    else:
        R3_prompt = ""
    return R3_prompt

def build_Q14_prompt(answer):
    if answer == "one":
        Q14_prompt = "The patient's documented American Society of Anesthesiologiest's (ASA) Physical Classification system class prior to the first / only OR procedure was Class 1."
    else:
        class_list = [
            "Class 2",
            "Class 3",
            "Class 4",
            "Class 5"
        ]
        rand_class = random.choice(class_list)
        Q14_prompt = f"The patient's documented American Society of Anesthesiologiest's (ASA) Physical Classification system class prior to the first / only OR procedure was {rand_class}."
    return Q14_prompt

def build_R6_prompt(answer):
    if answer == "yes":
        R6_prompt = "The patient's discharge status was died."
    else:
        R6_prompt = "" # nothing to add to prompts we already have
    R6_prompt

def build_R7_prompt(answer):
    if answer == "yes":
        R7_prompt = "The patient's discharge status was died."
    else:
        R7_prompt = "" # nothing to add to prompts we already have
    R7_prompt

def build_R8_prompt(answer):
    if answer == "yes":
        R8_prompt = "The patient's discharge status was died."
    else:
        R8_prompt = "" # nothing to add to prompts we already have
    R8_prompt

def build_Q14b_prompt(answer):
    if answer == "one":
        Q14b_prompt = "The patient's documented American Society of Anesthesiologiest's (ASA) Physical Classification system class prior to the SECOND OR procedure was Class 1."
    else:
        class_list = [
            "Class 2",
            "Class 3",
            "Class 4",
            "Class 5"
        ]
        rand_class = random.choice(class_list)
        Q14b_prompt = f"The patient's documented American Society of Anesthesiologiest's (ASA) Physical Classification system class prior to the SECOND OR procedure was {rand_class}."
    return Q14b_prompt

def build_Q14a_prompt(answer):
    if answer == "sooner":
        sooner_list = [
            "following the induction of anesthesia and prior to leaving the operating room",
            "within 24 hours after leaving the operating room for the final time but before discharge"
        ]
        rand_sooner = random.choice(sooner_list)
        Q14a_prompt = "The patient died {rand_sooner}."
    else:
        Q14a_prompt = "The patient died more than 24 hours after leaving the operating room for the final time but before discharge."
    return Q14a_prompt

def build_Q14c_prompt(answer):
    if answer == "yes":
        Q14c_prompt = "For the third OR procedure, the patient was documented as having an ASA Physical Classification System class of Class 1, and death occurred within 24 hours of administration of anasthesia for that surgery."
    else:
        Q14c_prompt = "For the third OR procedure, the patient was documented as having an ASA Physical Classification System class of Class 3."
    return Q14c_prompt

# currently no need to add to prompts or change any values here - all information is already in prompts
def build_R4_prompt(answer):
    if answer == "yes":
        R4_prompt = ""
    else:
        R4_prompt = ""
    return R4_prompt

def build_Q15_prompt(answer):
    if answer == "yes":
        Q15_prompt = "The record must note that the first / only OR procedure WAS done emergently."
    else:
        Q15_prompt = "The record must NOTE note that any OR procedures were done emergently."
    return Q15_prompt


# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(surgery_prompt_qa_dict[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(surgery_prompt_qa_dict.keys())
story_prompts_dict = {} # this will hold the full GPT-ready prompt for each story.

