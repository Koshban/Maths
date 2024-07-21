from common.config import question_answer
# Create 15 dictionaries
for n in range(1, 17):
    new_dict = {}
    for i in range(14):
        question_index = n + i * 14
        if question_index - 1 < len(question_answer):  # check to avoid IndexError
            question_key = list(question_answer.keys())[question_index - 1]
            new_dict[question_key] = question_answer[question_key]
    globals()[f"question_answer_{n}"] = new_dict

# logging.debug each dictionary in a dictionary format
for n in range(1, 17):
    logging.debug(f"question_answer_{n} = {{")
    for key, value in globals()[f"question_answer_{n}"].items():
        logging.debug(f'    "{key}": "{value}",')
    logging.debug("}\n")
