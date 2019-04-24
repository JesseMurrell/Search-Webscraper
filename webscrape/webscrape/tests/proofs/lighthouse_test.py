import sys
import json
import subprocess

string = "lighthouse https://www.google.com --output json --chrome-flags=\"--headless\" --config-path config/lighthouse.json"
call = subprocess.run(string, shell=True, capture_output=True)
std_out = call.stdout

string_data = std_out.decode(sys.stdout.encoding)

json_data = json.loads(string_data)
performance_score = json_data["categories"]["performance"]["score"]


print(performance_score)
