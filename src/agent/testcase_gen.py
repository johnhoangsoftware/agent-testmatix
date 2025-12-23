import csv
import subprocess

from src.agent.testcase_prompt import BASE_PROMPT


def call_ollama(prompt, model="phi"):
    # print("[STEP] Sending request to Ollama...")
    # resp = requests.post(
    #     "http://localhost:11434/api/generate",
    #     json={
    #         "model": model,
    #         "prompt": prompt,
    #     },
    #     timeout=60,
    #     stream=True
    # )
    # print("[STEP] Streaming response...")

    # output = ""
    # chunk_count = 0

    # for line in resp.iter_lines():
    #     if not line:
    #         continue

    #     decoded = line.decode("utf-8")
    #     chunk_count += 1
    #     print(f"[CHUNK {chunk_count}] {decoded[:120]}...")  # log 80 ký tự đầu

    #     try:
    #         obj = json.loads(decoded)
    #     except Exception as e:
    #         print("[WARN] JSON decode failed on chunk:", e)
    #         print(decoded)
    #         continue

    #     if "response" in obj:
    #         output += obj["response"]

    # print("[DONE] Streaming complete. Total chunks:", chunk_count)
    # print("[OUTPUT SIZE]", len(output), "characters")

    # return output
    result = subprocess.run(
        ["ollama", "run", model], input=prompt.encode("utf-8"), stdout=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")


def generate_testcases(endpoints):
    rows = []
    for ep in endpoints:
        # prompt = f"""{BASE_PROMPT}
        #         Endpoint:
        #         - URL: {ep['path']}
        #         - Method: {ep['method']}
        #         - Parameters: {ep['params']}
        #         """
        prompt = BASE_PROMPT.format(endpoints=endpoints)
        out = call_ollama(prompt)
        print(out)
        # crude parse: split by lines, pick CSV rows
        for line in out.splitlines():
            if line.count(",") >= 4:
                rows.append(line)

    # write to CSV
    with open("data/testcase_matrix.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["endpoint", "method", "test_type", "input_json", "expected_status_code"]
        )
        for r in rows:
            w.writerow(r.split(","))

    return rows

# Tôi muốn nó chỉ trả lời ra như này thôic ó cần ví dụ trong promt không
# https://example.com/pet,PUT,invalid enum values,,400
# import requests
# import json
# from .testcase_prompt import PROMPT_TEMPLATE, BASE_PROMPT

# def generate_testcases(endpoints, model="phi"):
#     prompt = BASE_PROMPT.format(endpoints=endpoints)

#     print("[STEP] Sending request to Ollama...")
#     resp = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": model,
#             "prompt": prompt,
#         },
#         timeout=60,
#         stream=True
#     )
#     print("[STEP] Streaming response...")

#     output = ""
#     chunk_count = 0

#     for line in resp.iter_lines():
#         if not line:
#             continue

#         decoded = line.decode("utf-8")
#         chunk_count += 1
#         print(f"[CHUNK {chunk_count}] {decoded[:120]}...")  # log 80 ký tự đầu

#         try:
#             obj = json.loads(decoded)
#         except Exception as e:
#             print("[WARN] JSON decode failed on chunk:", e)
#             print(decoded)
#             continue

#         if "response" in obj:
#             output += obj["response"]

#     print("[DONE] Streaming complete. Total chunks:", chunk_count)
#     print("[OUTPUT SIZE]", len(output), "characters")

#     return output


# import requests
# import json
# from .testcase_prompt import PROMPT_TEMPLATE

# def generate_testcases(endpoints, model="phi"):
#     prompt = PROMPT_TEMPLATE.format(endpoints=endpoints)

#     resp = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": model, "prompt": prompt},
#         stream=True
#     )

#     output = ""
#     for line in resp.iter_lines():
#         if line:
#             obj = json.loads(line.decode('utf-8'))
#             if "response" in obj:
#                 output += obj["response"]

#     return output
