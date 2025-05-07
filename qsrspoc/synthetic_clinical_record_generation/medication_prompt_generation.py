# split into 4 parts (matching the split in AWS)
# these were built manually; chatGPT borked.
# double-check them at some point for tail repetition. 

# so there are four dictionaries, _part_1, _part_2, _part_3, _part_4
# remember - they don't need to be for prompts/pdfs. There will be 4 groups of PDFs.

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





# dicts for part 2

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
    "Q24": "none",
    "R3": "no"
}

medication_prompt_qa_dict_part_2[17] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "no",
    "R8": "no",
    "Q59": "no"
}

medication_prompt_qa_dict_part_2[18] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "no",
    "Q53": "no"
}

medication_prompt_qa_dict_part_2[19] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "no",
    "Q53": "yes",
    "Q54": "none"
}

medication_prompt_qa_dict_part_2[20] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "no",
    "Q53": "yes",
    "Q54": "yes",
    "Q55": "yes"
}

medication_prompt_qa_dict_part_2[21] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "no",
    "Q53": "yes",
    "Q54": "yes",
    "Q55": "no"
}

medication_prompt_qa_dict_part_2[22] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "no",
    "R8": "yes",
    "Q58": "yes"
}

medication_prompt_qa_dict_part_2[23] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "no",
    "R8": "yes",
    "Q58": "no"
}

medication_prompt_qa_dict_part_2[24] = {
    "R2": "no",
    "Q23": "yes",
    "Q24": "yes",
    "Q52": "yes",
    "Q56": "yes",
    "Q57": "yes"
}

medication_prompt_qa_dict_part_2[25] = {
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
    "Q61b": "yes"
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
    "Q61b": "no"
}


# dicts for part 3, pages 8 and 9 - very straightforward compared to parts 1 & 2
medication_prompt_qa_dict_part_3 = {}

medication_prompt_qa_dict_part_3[1] = {
    "Q7": "no",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[2] = {
    "Q7": "yes",
    "Q62": "no",
    "Q63a": "no",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[3] = {
    "Q7": "yes",
    "Q62": "yes",
    "Q63": "yes",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[4] = {
    "Q7": "yes",
    "Q62": "no",
    "Q63a": "yes",
    "Q63b": "yes",
    "Q63c": "yes",
    "Q63d": "yes",
    "Q8": "no"
}

# value isn't in logical order; this was a dupe of 2
# so I moved the very last value up here
medication_prompt_qa_dict_part_3[5] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "yes",
    "Q74": "yes"
}

medication_prompt_qa_dict_part_3[6] = {
    "Q7": "yes",
    "Q62": "no",
    "Q63a": "yes",
    "Q63b": "no",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[7] = {
    "Q7": "yes",
    "Q62": "no",
    "Q63a": "yes",
    "Q63b": "yes",
    "Q63c": "yes",
    "Q63d": "no",
    "Q8": "no"
}

medication_prompt_qa_dict_part_3[8] = {
	"Q7": "no",
    "Q8": "yes",
    "Q64a": "yes",
    "Q64b": "yes",
    "Q64c": "yes",
    "Q64d": "yes",
    "Q64": "no",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[9] = {
	"Q7": "no",
    "Q8": "yes",
    "Q64a": "yes",
    "Q64b": "yes",
    "Q64c": "yes",
    "Q64d": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[10] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "yes",
    "Q64b": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[11] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[12] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "yes",
    "Q65": "no",
    "Q66": "no",
    "Q67": "no"
}

medication_prompt_qa_dict_part_3[13] = {
	"Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "yes",
    "Q65": "no",
    "Q66": "no",
    "Q67": "yes",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[14] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "yes",
    "Q65": "no",
    "Q66": "yes",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[15] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "yes",
    "Q65": "yes",
    "Q68": "no",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[16] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "yes",
    "Q69": "no",
    "Q72": "no"
}

medication_prompt_qa_dict_part_3[17] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "yes",
    "Q69": "no",
    "Q72": "yes",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[18] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "yes",
    "Q69": "yes",
    "Q73": "no"
}

medication_prompt_qa_dict_part_3[19] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "yes",
    "Q74": "no",
    "Q75": "no"
}

medication_prompt_qa_dict_part_3[20] = {
    "Q7": "no",
    "Q8": "yes",
    "Q64a": "no",
    "Q64": "no",
    "Q68": "no",
    "Q73": "yes",
    "Q74": "no",
    "Q75": "yes"
}


# dicts for part 4, page 10 and 11 (only a few questions, but the step function has fancy structure to check)
# might need to change this - we need to generate a variety of prompt conversations for 78 / 79 / 80 across 7 medications

medication_prompt_qa_dict_part_4 = {}

medication_prompt_qa_dict_part_4[1] = {
    "Q76": "no",
    "Q8a": "no"
}

medication_prompt_qa_dict_part_4[2] = {
    "Q76": "yes",
    "Q77": "yes",
    "Q78": "yes",
    "Q79": "yes",
    "Q80": "yes",
    "Q8a": "no"
}

medication_prompt_qa_dict_part_4[3] = {
	"Q76": "no",
    "Q8a": "yes",
    "Q70": "yes",
    "Q71": "yes"
}


