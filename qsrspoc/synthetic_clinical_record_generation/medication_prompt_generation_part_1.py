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

medication_prompt_qa_dict_part_1 = {}

medication_prompt_qa_dict_part_1[1] = {
    "Q1a": "no",
    "Q6": "no"
}

medication_prompt_qa_dict_part_1[2] = {
    "Q1a": "yes",
    "Q2a": "no",
    "Q2b": "yes",
    "Q2c": "yes" # non-branching placeholder
}

medication_prompt_qa_dict_part_1[3] = {
    "Q1a": "yes",
    "Q2a": "no",
    "Q2b": "none"
}

medication_prompt_qa_dict_part_1[4] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "none",
    "R0a": "yes",
    "Q4": "yes",
    "Q5": "yes"
}

medication_prompt_qa_dict_part_1[5] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "none",
    "R0a": "yes",
    "Q4": "yes",
    "Q5": "no"
}

medication_prompt_qa_dict_part_1[6] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "none",
    "R0a": "yes",
    "Q4": "no",
    "Q4a": "no"
}

medication_prompt_qa_dict_part_1[7] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "none",
    "R0a": "yes",
    "Q4": "no",
    "Q4a": "yes",
    "Q4b": "yes" # nonbranching placeholder
}

medication_prompt_qa_dict_part_1[8] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "none",
    "R0a": "no"
}

medication_prompt_qa_dict_part_1[9] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "no"
}

medication_prompt_qa_dict_part_1[10] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "no" # goes to PAGE 8 so end
}

medication_prompt_qa_dict_part_1[11] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "no", # jump to PAGE 4 for q13, q14, q15
    "Q13": "no" # goes to PAGE 6 so end
}

medication_prompt_qa_dict_part_1[12] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "no", # jump to PAGE 4 for q13, q14, q15
    "Q13": "yes",
    "Q14": "yes" # goes to PAGE 5 so end
}

medication_prompt_qa_dict_part_1[13] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "no", # jump to PAGE 4 for q13, q14, q15
    "Q13": "yes",
    "Q14": "no",
    "Q15": "vitk" # answers are vitk, rfvIIa, pcc, none. goes to PAGE 5 SO END
}

medication_prompt_qa_dict_part_1[14] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "no", # jump to PAGE 4 for q13, q14, q15
    "Q13": "yes",
    "Q14": "no",
    "Q15": "rfvIIa" # answers are vitk, rfvIIa, pcc, none. goes to PAGE 5 SO END
}

medication_prompt_qa_dict_part_1[15] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "no", # jump to PAGE 4 for q13, q14, q15
    "Q13": "yes",
    "Q14": "no",
    "Q15": "pcc" # answers are vitk, rfvIIa, pcc, none. goes to PAGE 5 SO END
}

medication_prompt_qa_dict_part_1[16] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "no", # jump to PAGE 4 for q13, q14, q15
    "Q13": "yes",
    "Q14": "no",
    "Q15": "none" # answers are vitk, rfvIIa, pcc, none. goes to R2 (part 2) so END
}

# PAGE 4 IS COMPLETE

medication_prompt_qa_dict_part_1[17] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "no",
    "Q11": "yes"
}

medication_prompt_qa_dict_part_1[18] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "no",
    "Q11": "no",
    "R1": "no"
}

medication_prompt_qa_dict_part_1[19] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "no",
    "Q11": "no",
    "R1": "yes",
    "Q12": "yes"
}

medication_prompt_qa_dict_part_1[20] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "no",
    "Q11": "no",
    "R1": "yes",
    "Q12": "no"
}

medication_prompt_qa_dict_part_1[21] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", #shortest path to PAGE 3
    "Q32": "no",
    "Q33": "yes",
    "Q34": "yes",
    "Q35": "yes"
}

medication_prompt_qa_dict_part_1[22] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", #shortest path to PAGE 3
    "Q32": "no",
    "Q33": "yes",
    "Q34": "yes",
    "Q35": "no"
}

medication_prompt_qa_dict_part_1[23] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", #shortest path to PAGE 3
    "Q32": "no",
    "Q33": "yes",
    "Q34": "none"
}

medication_prompt_qa_dict_part_1[24] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", #shortest path to PAGE 3
    "Q32": "no",
    "Q33": "no"
}

medication_prompt_qa_dict_part_1[25] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", # shortest path to PAGE 3
    "Q32": "yes", # shortest path to Q36
    "Q36": "yes",
    "Q37": "yes",
    "R4": "yes",
    "Q38": "yes"
}

medication_prompt_qa_dict_part_1[26] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", # shortest path to PAGE 3
    "Q32": "yes", # shortest path to Q36
    "Q36": "yes",
    "Q37": "yes",
    "R4": "yes",
    "Q38": "no"
}

medication_prompt_qa_dict_part_1[27] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", # shortest path to PAGE 3
    "Q32": "yes", # shortest path to Q36
    "Q36": "yes",
    "Q37": "yes",
    "R4": "no"
}

medication_prompt_qa_dict_part_1[28] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", # shortest path to PAGE 3
    "Q32": "yes", # shortest path to Q36
    "Q36": "yes",
    "Q37": "no",
    "R4": "no"
}

medication_prompt_qa_dict_part_1[29] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", # shortest path to PAGE 3
    "Q32": "yes", # shortest path to Q36
    "Q36": "no",
    "R4": "no", # shortest path to Q39
    "Q39": "yes",
    "Q41a": "yes", # non-branching placeholder
    "Q41b": "yes", # non-branching placeholder
    "RY": "yes"
}

medication_prompt_qa_dict_part_1[30] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", # shortest path to PAGE 3
    "Q32": "yes", # shortest path to Q36
    "Q36": "no",
    "R4": "no", # shortest path to Q39
    "Q39": "yes",
    "Q41a": "yes", # non-branching placeholder
    "Q41b": "yes", # non-branching placeholder
    "RY": "no"
}

medication_prompt_qa_dict_part_1[31] = {
    "Q1a": "yes",
    "Q2a": "yes", # shortest path to Q3
    "Q3": "yes",
    "R0": "yes",
    "Q3a": "yes", # nonbranching placeholder, shortest path to PAGE 2
    "Q6": "yes",
    "Q9": "yes",
    "Q10": "yes", # shortest path to PAGE 3
    "Q32": "yes", # shortest path to Q36
    "Q36": "no",
    "R4": "no", # shortest path to Q39
    "Q39": "no"
}

def build_Q1a_prompt(answer):
    if answer == "yes":
        Q1a_prompt = "The patient had an adverse drug reaction / allergic response to a drug during their stay."
    else:
        Q1a_prompt = "The record must not mention any adverse drug reaction / allergic response to a drug during the stay."
    return Q1a_prompt

def build_Q2a_prompt(answer):
    if answer == "yes":
        Q2a_prompt = "The patient's record must indicate they had no known allergies (NKA)"
    else:
        Q2a_prompt = "The patient's record must indicate thay have an allergy."
    return Q2a_prompt

def build_Q2b_prompt(answer):
    if answer == "yes":
        allergen_meds = [
            "penicillin",
            "morphine",
            "naproxen"
        ]
        rand_med = random.choice(allergen_meds)
        Q2b_prompt = f"The record must state that the patient had a known allergy to {rand_med}."
    else:
        Q2b_prompt = "The record must not list any medication as something the patient is allergic to."
    return Q2b_prompt

def build_Q2c_prompt(answer):
    if answer == "yes":
        Q2c_prompt = "The record must note that the patient received this medication during their stay."
    else:
        Q2c_prompt = "The record must not say anything about the patient being administered this medication during their stay."
    return Q2c_prompt

# multiple choice question but the yes case is actually determined by R0 currently
def build_Q3_prompt(answer):
    if answer == "yes":
        Q3_prompt = ""
    else:
        adverse_reaction_list = [
            "anaphylaxis documented by provider",
            "hives, welts, or wheals",
            "wheezing, difficulty breathing, or change in respiratory rate",
            "drop in blood pressure",
            "administration of epinephrine, diphenhydramine or steroids"
        ]
        all_reactions_str = ", ".join(adverse_reaction_list)
        Q3_prompt = f"The record must not mention any of the following happening after administration of any medication: {all_reactions_str}."
    return Q3_prompt

def build_R0_prompt(answer):
    if answer == "yes":
        reactions = [
            "hives, welts, or wheals",
            "wheezing, difficulty breathing, or change in respiratory rate",
            "drop in blood pressure",
            "administration of epinephrine, diphenhydramine or steroids"
        ]
        two_reactions = random.sample(reactions, 2)
        rand_reaction = random.choice(["anaphylaxis documented by provider", two_reactions])
        R0_prompt = f"The record must note that the patient experienced the following adverse effects 1 hour after the administration of a medication: {rand_reaction}."
    else:
        R0_prompt = ""
    return R0_prompt

# non-branching placeholder, free text
def build_Q3a_prompt():
    med_list = [
            "penicillin",
            "morphine",
            "naproxen",
            "furosemide"
        ]
    rand_med = random.choice(med_list)
    Q3a_prompt = f"The chart must note that the adverse effects just mentioned occurred 1 hour after being given the medication {rand_med}."
    return Q3a_prompt

def build_R0a_prompt(answer):
    if answer == "yes":
        R0a_prompt = "The record must note that the patient was put on a ventilator during their stay."
    else:
        R0a_prompt = "The record must not say the patient was on a ventilator at any time during their stay."
    return R0a_prompt

def build_Q4_prompt(answer):
    if answer == "yes":
        Q4_prompt = "The patient was put on the ventilator before the medication causing adverse effects was administered."
    else:
        Q4_prompt = "The patient was put on the ventilator after the medication causing adverse effects was administered."
    return Q4_prompt

def build_Q4a_prompt(answer):
    if answer == "yes":
        Q4a_prompt = "The patient was put on the ventilator 1.5 hours after the medication was administered."
    else:
        Q4a_prompt = "The patient was put on the ventilator 6 hours after the medication was administered."
    return Q4a_prompt

# already handled by previous questions
def build_Q4b_prompt():
    Q4b_prompt = ""
    return Q4b_prompt

def build_Q5_prompt(answer):
    if answer == "yes":
        Q5_prompt = "The record must note that, during the stay, flumazepil was administered to the patient."
    else:
        Q5_prompt = "The record should make no mention of either flumazepil or flumazenil."
    return Q5_prompt

def build_Q6_prompt(answer):
    if answer == "yes":
        Q6_prompt = "The record must note that an anticoagulant was administered to the patient on day 3."
    else:
        Q6_prompt = "The record must NOT note that an anticoagulant was administered to the patient."
    return Q6_prompt

def build_Q9_prompt(answer):
    if answer == "yes":
        Q9_prompt = "The record must note that intravenous unfractionated heparin was administered to the patient. The first dose was on day 2."
    else:
        Q9_prompt = "The record must NOT note that intravenous unfractionated heparin was administered to the patient."
    return Q9_prompt

def build_Q10_prompt(answer):
    if answer == "yes":
        Q10_prompt = "The record must note that after the patient's first dose of the IV unfractionated heparin on day 2, they had a PTT value greater than 100 seconds on day 3."
    else:
        Q10_prompt = "The record must NOT note any elevated PTT values (over 100 seconds) after any doses of the IV unfractionated heparin."
    return Q10_prompt

def build_Q11_prompt(answer):
    if answer == "yes":
        Q11_prompt = "The record must note that during the stay, the patient received protamine on day 4 (after the IV unfractionated heparin)."
    else:
        Q11_prompt = "The record must NOT note that during the stay, the patient received protamine after the IV unfractionated heparin."
    return Q11_prompt

def build_R1_prompt(answer):
    if answer == "yes":
        R1_prompt = "The record must note that the patient received fresh frozen plasma during their stay."
    else:
        R1_prompt = "The record must NOT note that the patient received fresh frozen plasma during their stay."
    return R1_prompt

def build_Q12_prompt(answer):
    if answer == "yes":
        Q12_prompt = "The record must specify that the fresh frozen plasma was given to the patient after the unfractionated heparin was administered."
    else:
        Q12_prompt = "The record must specify that the fresh frozen plasma was given to the patient BEFORE ANY of the unfractionated heparin was administered."
    return Q12_prompt

def build_Q32_prompt(answer):
    if answer == "yes":
        Q32_prompt = "The record must note that there was bleeding present on admission."
    else:
        Q32_prompt = "The record must note that there was NOT bleeding present on admission."
    return Q32_prompt

def build_Q33_prompt(answer):
    if answer == "yes":
        Q33_prompt = "The record must note that there was bleeding that developed during the stay, on day 3."
    else:
        Q33_prompt = "The record must NOT note that any bleeding developed during the stay."
    return Q33_prompt

def build_Q34_prompt(answer):
    sites = [
            "gastrointestinal bleeding",
            "genitourinary bleeding",
            "pulmonary bleeding",
            "hematoma",
            "intracranial bleeding"
        ]
    if answer == "yes":
        rand_site = random.choice(sites)
        Q34_prompt = f"The record must note that the type of bleeding that developed was {rand_site}."
    else:
        all_sites_str = ", ".join(sites)
        Q34_prompt = f"The record must not specify at what site the bleeding developed."
    return Q34_prompt

# yes case (story 21) also requires R1 to be "yes" or Q10 to be "yes" - Q10 is yes in story 21: PTT was high on day 3
def build_Q35_prompt(answer):
    if answer == "yes":
        Q35_prompt = "This bleeding developed on day 2."
    else:
        Q35_prompt = "This bleeding developed on day 1."
    return Q35_prompt

def build_Q36_prompt(answer):
    if answer == "yes":
        Q36_prompt = "The record must describe that the patient required emergency measures to sustain life."
    else:
        Q36_prompt = "The record must not mention cardiac arrest, emergency measures to sustain life, or a call for rapid response team."
    return Q36_prompt

# yes case also requires R1 to be "yes" or Q10 to be "yes" - Q10 is yes in all such stories: PTT was high on day 3
def build_Q37_prompt(answer):
    if answer == "yes":
        Q37_prompt = "The patient required emergency measures to sustain life on day 4."
    else:
        Q37_prompt = "The patient required emergency measures to sustain life on day 1."
    return Q37_prompt

def build_R4_prompt(answer):
    if answer == "yes":
        R4_prompt = "The patient's discharge status is died."
    else:
        R4_prompt = "The patient's discharge status must not be died."
    return R4_prompt

def build_Q38_prompt(answer, discharge_day):
    if answer == "yes":
        Q38_prompt = "The patient died on day 4."
    else:
        discharge_day = 6
        Q38_prompt = "The patient died on day 6."
    return Q38_prompt, discharge_day

# After the first 48 hours of admission, did patient have a hemoglobin level reported?
def build_Q39_prompt(answer):
    if answer == "yes":
        Q39_prompt = "On day 3, the patient's hemoglobin level was reported to be 14 g/dL before the anticoagulant was administered."
    else:
        Q39_prompt = "The record must not state the patient's hemoglobin level at any time during the stay."
    return Q39_prompt

# non-branching numerical answer: note that numbers in 41a, 41b, and RY have to fit together
# 39 includes the answer for 41a; RY's answer determines what the answer for 41b should be
# What was hemoglobin level before any anticoagulant administration?
def build_Q41a_prompt():
    Q41a_prompt = ""
    return Q41a_prompt

# non-branching numerical answer: note that numbers in 41a, 41b, and RY have to fit together
# What was the hemoglobin level after anticoagulant administration and within 1 day after high-PTT day?
def build_Q41b_prompt():
    Q41b_prompt = ""
    return Q41b_prompt

# RY's prompt will hold the data from 41a and b to make stories consistent.
# is 41a - 41b >= 5? (did the hemoglobin level decrease by at least 5 g/dL after treatment?)
def build_RY_prompt(answer):
    if answer == "yes":
        RY_prompt = "On day 4, the patient's hemoglobin level was 6."
    else:
        RY_prompt = "On day 4, the patient's hemoglobin level was 12."
    return RY_prompt

def build_Q13_prompt(answer):
    if answer == "yes":
        Q13_prompt = "The record must note that warfarin was administered during the stay."
    else:
        Q13_prompt = "The record must not mention warfarin."
    return Q13_prompt

def build_Q14_prompt(answer):
    if answer == "yes":
        Q14_prompt = "During the stay, after the initial administered warfarin dose, the patient's INR value was 5.2"
    else:
        Q14_prompt = "During the stay, the patient's INR value was 3.0 after the first warfarin dose. The record should not mention INR values after that."
    return Q14_prompt

# answers are vitk, rfvIIa, pcc, none
def build_Q15_prompt(answer):
    if answer == "vitk":
        Q15_prompt = "The patient received vitamin K after the initial dose of warfarin."
    elif answer == "rfvIIa":
        Q15_prompt = "The patient received recombinant factor VIIa after the initial dose of warfarin."
    elif answer == "pcc":
        Q15_prompt = "The patient received prothrombin complex concentrate after the initial dose of warfarin."
    else: # none
        Q15_prompt = "The record must not mention vitamin K, recombinant factor VIIa, or prothrombin complex."
    return Q15_prompt

# use this at the end of the main program to save each full GPT-ready prompt to a json file
# this file name shows what story the resulting PDF is; we'll use that during manual PDF generation
# so we'll store it in the JSON too
def generate_pdf_file_name(algo_str, story_number, prompt_run):
    # dictionaries don't store their key-value pairs in order, but sorting alphabetically will fix that
    sorted_items = sorted(medication_prompt_qa_dict_part_1[story_number].items())
    
    # Correct way to join key-value pairs
    formatted_string = prompt_run + "-" + algo_str + "_story" + str(story_number) + "_" + "_".join(f"{key}_{value}" for key, value in sorted_items)

    return f"{formatted_string}.pdf"

story_numbers = list(medication_prompt_qa_dict_part_1.keys())
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
    question_keys = list(medication_prompt_qa_dict_part_1[num].keys())

    ###### in this section, check if each key is in the question_keys list and, if so, call their function
    # and use the returned value to update list_of_prompts, any other variables.
    if "Q1a" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q1a"]
        q1a_prompt = build_Q1a_prompt(ans)
        list_of_prompts.append(q1a_prompt)
    if "Q2a" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q2a"]
        q2a_prompt = build_Q2a_prompt(ans)
        list_of_prompts.append(q2a_prompt)
    if "Q2b" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q2b"]
        q2b_prompt = build_Q2b_prompt(ans)
        list_of_prompts.append(q2b_prompt)
    if "Q2c" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q2c"]
        q2c_prompt = build_Q2c_prompt(ans)
        list_of_prompts.append(q2c_prompt)
    if "Q3" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q3"]
        q3_prompt = build_Q3_prompt(ans)
        list_of_prompts.append(q3_prompt)
    if "R0" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["R0"]
        r0_prompt = build_R0_prompt(ans)
        list_of_prompts.append(r0_prompt)
    if "Q3a" in question_keys:
        q3a_prompt = build_Q3a_prompt()
        list_of_prompts.append(q3a_prompt)
    if "R0a" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["R0a"]
        r0a_prompt = build_R0a_prompt(ans)
        list_of_prompts.append(r0a_prompt)
    if "Q4" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q4"]
        q4_prompt = build_Q4_prompt(ans)
        list_of_prompts.append(q4_prompt)
    if "Q4a" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q4a"]
        q4a_prompt = build_Q4a_prompt(ans)
        list_of_prompts.append(q4a_prompt)
    if "Q4b" in question_keys:
        q4b_prompt = build_Q4b_prompt()
        list_of_prompts.append(q4b_prompt)
    if "Q5" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q5"]
        q5_prompt = build_Q5_prompt(ans)
        list_of_prompts.append(q5_prompt)
    if "Q6" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q6"]
        q6_prompt = build_Q6_prompt(ans)
        list_of_prompts.append(q6_prompt)
    if "Q9" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q9"]
        q9_prompt = build_Q9_prompt(ans)
        list_of_prompts.append(q9_prompt)
    if "Q10" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q10"]
        q10_prompt = build_Q10_prompt(ans)
        list_of_prompts.append(q10_prompt)
    if "Q11" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q11"]
        q11_prompt = build_Q11_prompt(ans)
        list_of_prompts.append(q11_prompt)
    if "R1" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["R1"]
        r1_prompt = build_R1_prompt(ans)
        list_of_prompts.append(r1_prompt)
    if "Q12" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q12"]
        q12_prompt = build_Q12_prompt(ans)
        list_of_prompts.append(q12_prompt)
    if "Q32" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q32"]
        q32_prompt = build_Q32_prompt(ans)
        list_of_prompts.append(q32_prompt)
    if "Q33" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q33"]
        q33_prompt = build_Q33_prompt(ans)
        list_of_prompts.append(q33_prompt)
    if "Q34" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q34"]
        q34_prompt = build_Q34_prompt(ans)
        list_of_prompts.append(q34_prompt)
    if "Q35" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q35"]
        q35_prompt = build_Q35_prompt(ans)
        list_of_prompts.append(q35_prompt)
    if "Q36" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q36"]
        q36_prompt = build_Q36_prompt(ans)
        list_of_prompts.append(q36_prompt)
    if "Q37" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q37"]
        q37_prompt = build_Q37_prompt(ans)
        list_of_prompts.append(q37_prompt)
    if "R4" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["R4"]
        r4_prompt = build_R4_prompt(ans)
        list_of_prompts.append(r4_prompt)
    if "Q38" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q38"]
        q38_prompt, discharge_day_number = build_Q38_prompt(ans, discharge_day_number)
        list_of_prompts.append(q38_prompt)
    if "Q39" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q39"]
        q39_prompt = build_Q39_prompt(ans)
        list_of_prompts.append(q39_prompt)
    if "Q41a" in question_keys:
        q41a_prompt = build_Q41a_prompt()
        list_of_prompts.append(q41a_prompt)
    if "Q41b" in question_keys:
        q41b_prompt = build_Q41b_prompt()
        list_of_prompts.append(q41b_prompt)
    if "RY" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["RY"]
        ry_prompt = build_RY_prompt(ans)
        list_of_prompts.append(ry_prompt)
    if "Q13" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q13"]
        q13_prompt = build_Q13_prompt(ans)
        list_of_prompts.append(q13_prompt)
    if "Q14" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q14"]
        q14_prompt = build_Q14_prompt(ans)
        list_of_prompts.append(q14_prompt)
    if "Q15" in question_keys:
        ans = medication_prompt_qa_dict_part_1[num]["Q15"]
        q15_prompt = build_Q15_prompt(ans)
        list_of_prompts.append(q15_prompt)
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