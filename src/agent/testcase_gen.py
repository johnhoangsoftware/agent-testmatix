import os
import csv
import subprocess
from google import genai

from src.agent.testcase_prompt import BASE_PROMPT 
# ======================
# Gemini API key
# ======================
os.environ["GEMINI_API_KEY"] = "AIzaSyD9NGH-xVqtHALUy3m7FlrX7s6Fxx_V6iU"
client = genai.Client()
 
# ======================
# LLM CALLS (ONLY CALL)
# ======================
def call_ollama(prompt, model="phi"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8")
 
 
def call_gemini(prompt, model="gemini-2.5-flash"):
    return '''
    /user/john_doe,GET,positive valid input,null,200
    /user/,GET,missing required fields,null,400
    /user/user@name,GET,wrong data types,null,400
    /user/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa,GET,boundary values,null,400
    /user/john_doe,GET,unauthorized,null,401
    /user/nonexistentuser123,GET,invalid enum values,null,404
    /user/john_doe,GET,unauthorized,null,401
    '''
    # response = client.models.generate_content(
    #     model=model,
    #     contents=prompt,
    # )
    # return response.text 
    # raise NotImplementedError("Gemini not configured")
 
 
def call_llm(prompt, llm="gemini"):
    if llm == "ollama":
        return call_ollama(prompt)
    elif llm == "gemini":
        return call_gemini(prompt)
    else:
        raise ValueError("Unsupported LLM")
 
def parse_csv_from_llm_output(output: str):
    """
    Parse CSV rows from LLM output
    Expected format:
    endpoint,method,test_type,input_json,expected_status_code
    """
    rows = []
 
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
 
        # crude CSV detection
        if line.count(",") >= 4:
            rows.append(line.split(","))
 
    return rows
 
def write_testcase_csv(rows, path="data/testcase_matrix.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["endpoint", "method", "test_type", "input_json", "expected_status_code"]
        )
        writer.writerows(rows)

def generate_csv_string(rows):
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        ["endpoint", "method", "test_type", "input_json", "expected_status_code"]
    )
    writer.writerows(rows)
    return output.getvalue()

def generate_testcases(endpoints, llm="ollama"):
    prompt = BASE_PROMPT.format(endpoints=endpoints)
 
    # call model
    raw_output = call_llm(prompt, llm=llm)
    print("=== RAW LLM OUTPUT ===")
    print(raw_output)
 
    # parse
    rows = parse_csv_from_llm_output(raw_output)

    # return CSV string
    csv_string = generate_csv_string(rows)

    return csv_string