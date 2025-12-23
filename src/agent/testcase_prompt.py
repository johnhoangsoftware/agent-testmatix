PROMPT_TEMPLATE = """
You are an API QA generator.
Given a list of API endpoints with HTTP method and input parameters,
generate a CSV table of test scenarios.

Columns:
Endpoint, Method, Scenario, Input, Expected, StatusCode, Category

Rules:
- For each endpoint generate at least 4 scenarios
- 2 Positive
- 2 Negative
- Include missing parameter scenario if required fields exist
- Include wrong type scenario if fields are numeric
- Include boundary scenario if numeric ranges exist
- Category must be Positive or Negative
- Return CSV rows only, no commentary, no quotes.

Endpoints:
{endpoints}
"""

BASE_PROMPT = """
You must output ONLY a CSV table and nothing else.
Follow these rules strictly:

- The entire response must be wrapped in triple backticks.
- Inside the triple backticks, you must print multiple CSV lines.
- Each CSV row MUST be on a separate physical line ending with a newline.
- You are not allowed to place multiple rows on a single line.
- You are not allowed to output explanations, comments, or reasoning.
- You are not allowed to output code in any programming language.
- The CSV must contain ONLY the following columns in this order:
endpoint,method,test_type,input_json,expected_status_code

Generate rows for one endpoint: {endpoints}

Include exactly these test types:
- positive valid input
- missing required fields
- wrong data types
- boundary values
- unauthorized
- invalid enum values

Output only CSV rows. No English sentences outside the CSV. No markdown except the fence.
"""
