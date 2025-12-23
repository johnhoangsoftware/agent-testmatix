from src.ingest.spec_loader import load_spec # sprint 1 output
from src.ingest.spec_parser import parse_endpoints
from src.agent.testcase_gen import generate_testcases
from src.agent.save_csv import save_csv

spec = load_spec()
ends = parse_endpoints(spec)
csv_text = generate_testcases(ends[:1])
print(csv_text)
# save_csv(csv_text)

print(">>> Sprint 2 completed. test_matrix saved.")
