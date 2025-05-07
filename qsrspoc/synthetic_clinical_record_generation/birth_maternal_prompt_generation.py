import random
from typing import List, Tuple

birth_maternal_prompt_qa_dict = {}

birth_maternal_prompt_qa_dict[1] = {
    "EQR1": "no"
}

birth_maternal_prompt_qa_dict[2] = {
    "EQR1": "yes",
    "EQ1": "no"
}

birth_maternal_prompt_qa_dict[3] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "injury",
    "Q2": "yes" # nonbranching placeholder value
}

birth_maternal_prompt_qa_dict[4] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "none"
}

birth_maternal_prompt_qa_dict[5] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "atvd" # choices are atvd, vd, csec
}

birth_maternal_prompt_qa_dict[6] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "vd", # choices are atvd, vd, csec
    "Q4": "yes", # non-branching numerical answer dependent on R1
    "R1": "no"
}

birth_maternal_prompt_qa_dict[7] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "vd", # choices are atvd, vd, csec
    "Q4": "yes", # non-branching numerical answer dependent on R1
    "R1": "yes",
    "Q5": "no"
}

birth_maternal_prompt_qa_dict[8] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "vd", # choices are atvd, vd, csec
    "Q4": "yes", # non-branching numerical answer dependent on R1
    "R1": "yes",
    "Q5": "yes",
    "Q6": "no"
}

birth_maternal_prompt_qa_dict[9] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "vd", # choices are atvd, vd, csec
    "Q4": "yes", # non-branching numerical answer dependent on R1
    "R1": "yes",
    "Q5": "yes",
    "Q6": "yes"
}

birth_maternal_prompt_qa_dict[10] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "csec", # choices are atvd, vd, csec
    "Q6a": "yes", # non-branching numerical answer
    "Q7": "yes", # non-branching numerical answer
    "R1a": "no",
    "R2": "no" # only yes if Q1=none or Q6=yes or Q7a=no
}

birth_maternal_prompt_qa_dict[11] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "csec", # choices are atvd, vd, csec
    "Q6a": "yes", # non-branching numerical answer
    "Q7": "yes", # non-branching numerical answer
    "R1a": "yes",
    "Q7a": "no", # no here makes R2 true
}

birth_maternal_prompt_qa_dict[12] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "csec", # choices are atvd, vd, csec
    "Q6a": "yes", # non-branching numerical answer
    "Q7": "yes", # non-branching numerical answer
    "R1a": "yes",
    "Q7a": "yes",
    "Q8": "yes",
    "Q9": "yes", # non-branching number above or below 39
    "Q10": "yes" # non-branching multiple choice
}

birth_maternal_prompt_qa_dict[13] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "atvd", # choices are atvd, vd, csec
    "Q6a": "yes", # non-branching numerical answer
    "Q7": "yes", # non-branching numerical answer
    "R1a": "yes",
    "Q7a": "yes",
    "Q8": "no",
    "R3": "yes",
    "Q11": "yes" # non-branching multiple choice
}

birth_maternal_prompt_qa_dict[14] = {
    "EQR1": "yes",
    "EQ1": "yes",
    "Q1": "yes", # options besides injury or none
    "Q3": "csec", # choices are atvd, vd, csec
    "Q6a": "yes", # non-branching numerical answer
    "Q7": "yes", # non-branching numerical answer
    "R1a": "yes",
    "Q7a": "yes",
    "Q8": "no",
    "R3": "no"
}

def build_EQR1_prompt(answer, patient_age):
    if answer == "yes":
        patient_age = random.randint(10, 65)
        EQR1_prompt = f"Patient is a female."
    else:
        EQR1_prompt = f"Patient is not a female."
    return EQR1_prompt, patient_age

def build_EQ1_prompt(answer):
    if answer == "yes":
        EQ1_prompt = f"The patient delivered during the stay."
    else:
        EQ1_prompt = f"The patient did not deliver during the stay."
    return EQ1_prompt

def build_Q1_prompt(answer):
    outcomes_list = [
        "chorioamnionitis",
        "endometritis",
        "hemorrhage requiring transfusion",
        "eclampsia (pre-eclampsia plus seizures or convulsions)",
        "third-or-fourth-degree perineal laceration"
        ]
    if answer == "injury":
        Q1_prompt = "The maternal outcome that ocurred during the stay was an injury to a body part."
    elif answer == "yes":
        rand_outcome = random.choice(outcomes_list)
        Q1_prompt = f"The maternal outcome that occurred during the stay was {rand_outcome}."
    else: # none
        outcomes_list.append("injury to a body part")
        all_outcomes_str = ", ".join(outcomes_list)
        Q1_prompt = f"The record must not mention any of the following: {all_outcomes_str}."
    return Q1_prompt

def build_Q2_prompt():
    injury_list = ["uterus", "ureter", "bladder", "bowel"]
    injury_loc = random.choice(injury_list)
    Q2_prompt = f"The injury was to the {injury_loc}."
    return Q2_prompt

def build_Q3_prompt(answer):
    if answer == "vd":
        Q3_prompt = f"The patient had a vaginal delivery."
    elif answer == "csec":
        Q3_prompt = f"The patient had a scheduled cesarean section with no attempted vaginal delivery."
    else: # atvd
        Q3_prompt = f"The patient had attempted vaginal delivery which was followed by cesarean section."
    return Q3_prompt

# placeholder, R1 currently determines this
def build_Q4_prompt():
    Q4_prompt = ""
    return Q4_prompt

# what was estimated gestational age and was it >= 39 weeks?
def build_R1_prompt(answer, ega_del):
    if answer == "yes":
        ega_del = random.randint(39,43)
        R1_prompt = f"The patient's gestational age in weeks is {ega_del}."
    else:
        ega_del = random.randint(30,38)
        R1_prompt = f"The patient's gestational age in weeks is {ega_del}."
    return R1_prompt, ega_del

def build_Q5_prompt(answer):
    if answer == "yes":
        common_antibiotics = ["cefazolin", "gentamicin", "clindamycin"]
        rand_abx = random.choice(common_antibiotics)
        Q5_prompt = f"Patient was given {rand_abx}."
    else:
        Q5_prompt = f"Patent was not given an antibiotic."
    return Q5_prompt

def build_Q6_prompt(answer):
    if answer == "yes":
        random_hours = random.randint(25,40)
        Q6_prompt = f"The antibiotic was administered {random_hours} hours following delivery of neonate."
    else:
        random_hours = random.randint(1,23)
        Q6_prompt = f"The antibiotic was administered {random_hours} hours following delivery of neonate."
    return Q6_prompt

def build_Q6a_prompt():
    num_fetuses = random.randint(1,4)
    Q6a_prompt = f"There were {num_fetuses} fetuses delivered."
    return Q6a_prompt, num_fetuses

# Placeholder; this is currently determined by R1a
def build_Q7_prompt():
    Q7_prompt = ""
    return Q7_prompt

def build_R1a_prompt(answer, num_fetuses):
    if answer == "yes":
        if num_fetuses == 1:
            R1a_prompt = "No fetuses were delivered alive."
        else:
            alive_fetuses = random.randint(0, num_fetuses-1) 
            R1a_prompt = f"{alive_fetuses} out of {num_fetuses} fetuses were delivered alive."
    else:
        R1a_prompt = "All fetuses were delivered alive."
    return R1a_prompt

# Placeholder - this is a check based on Q1, !6, Q7a - dicts determine value
def build_R2_prompt():
    R2_prompt = ""
    return R2_prompt

def build_Q7a_prompt(answer):
    if answer == "yes":
        Q7a_prompt = f"The fetal death was expected."
    else:
        Q7a_prompt = f"The fetal death was not expected."
    return Q7a_prompt

def build_Q8_prompt(answer):
    if answer == "yes":
        Q8_prompt = f"Labor was induced."
    else:
        Q8_prompt = f"Labor was not induced."
    return Q8_prompt

# what was ega at time of induction, and was it >= 39? 
# we already have ega at time of delivery, so induction must be <= that too
def build_Q9_prompt(ega_del):
    gestational_induct = random.randint(34, ega_del)
    Q9_prompt = f"The estimated gestational age at time of induction was {gestational_induct}."
    return Q9_prompt

def build_Q10_prompt():
    maternal_conditions = [
        "Diabetes mellitus",
        "Premature rupture of the membranes",
        "Pregnancy induced hypertension, including mild, moderate, or severe pre-eclampsia, or eclampsia", 
        "IUGR (intrauterine growth retardation) or SGA (small for gestational age)",
        "Cardiac disease",
        "Post maturity (41 or more weeks of pregnancy completed)",  
        "Isoimmunization (e.g., Rh disease)",
        "Chorioamnionitis",  
        "Abruptio placentae"
    ]
    rand_condition = random.choice(maternal_conditions)
    Q10_prompt = f"The following condition was present prior to induction: {rand_condition}."
    return Q10_prompt

# placeholder; delivery type is already determined; current story dicts force matches
def build_R3_prompt():
    R3_prompt = f"" 
    return R3_prompt


def build_Q11_prompt():
    instrument_list = ["vaccum", "forceps", "vacuum followed by forceps"]
    rand_instrument = random.choice(instrument_list)
    prompt_list = [
        f"The {rand_instrument} was used to aid in delivery.",
        f"There was not any instrumentation such as vacuum or forceps used during the birth process"
    ]
    Q11_prompt = random.choice(prompt_list)
    return Q11_prompt
