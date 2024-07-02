import json
import os

def getBadLandlordsFromProblemProperties():
    current_file = os.path.abspath(__file__)
    directory = os.path.dirname(current_file)
    file_path = os.path.join(directory, "official-problem-properties.json")
    with open(file_path, 'r') as f:
        problem_properties_json = json.load(f)
        return problem_properties_json