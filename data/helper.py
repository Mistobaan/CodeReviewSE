import copy
import json
from pprint import pprint
from bs4 import BeautifulSoup

def load_json_file(file_path:str)-> dict:
    with open(file_path,"r") as f:
        return json.load(f)

def dump_json_file(file_path:str, data:dict)->None:
    with open(file_path,"w") as f:
        json.dump(data,f)



parse_body = lambda x: x


def parse_html_to_str(body:str) -> list:

    html_parsed = BeautifulSoup(body, 'html.parser')
    strings = []
    children = html_parsed.children
    
    for child in children:
        child_text = child.text
        if child.name == "pre": child_text = "<code>" + child_text + "</code>"
        strings.append(child_text)

    return strings

    

def get_accepted_answer(code_review_data:dict):
    """
    Provides the accepted answer of a question, if an accepted answer is available.
    """
    accepted_answer_body = None
    if "AcceptedAnswerId" in code_review_data["meta_data"].keys():
        accepted_answer_index = int(code_review_data["meta_data"]["AcceptedAnswerId"])
        for code_review_answer in code_review_data["answers"]:
            if int(code_review_answer["meta_data"]["Id"]) == accepted_answer_index:
                accepted_answer_body = code_review_answer["body"]
                return parse_body(accepted_answer_body)
    
def duplicate_data(data, is_ans=False, n=10):
    """
    Duplicate the data by n times for subsequent augmentation. If is_ans is True, then key indicates that the answer is to be augmented, else the question is to be augmented.
    """
    for question in list(data.keys()):
        for i in range(n):
            if is_ans:
                key_name = question + '_ans' + str(i)
            else:
                key_name = question + '_q' + str(i)
            data[key_name] = copy.deepcopy(data[question])
    return data

def iter_body(augs, body):
    body_strings = parse_html_to_str(body)
    for i in range(len(body_strings)):
        body_string = body_strings[i]
        # is "<code>" present?
        if "<code>" in body_string.split():
            continue
        # apply augmentation
        body_strings[i] = augs([body_string])[0]
    return ' '.join(body_strings)


if __name__ == "__main__":
    dataset = load_json_file("dataset/CodeReviewSE.json")
    dataset = dataset[list(dataset.keys())[1000]]
    # print(dataset["body"])
    # print("#######")
    #pprint(dataset.keys())
    #pprint(dataset['meta_data'])
    #pprint(get_accepted_answer(dataset))
