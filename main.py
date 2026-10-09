from pathlib import Path
import json
BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
import re
import pandas as pd
examples = [
("ERROR connection timeout while contacting server", "network"),
("WARN packet loss above threshold", "network"),
("ERROR database query failed", "database"),
("INFO database backup completed", "database"),
("WARN GPU frame time increased", "performance"),
("ERROR rendering frame drop detected", "performance"),
("ERROR authentication token expired", "security"),
("WARN invalid password attempt", "security"),
("INFO session log exported to csv", "data"),
("WARN missing sensor value in data record", "data"),
("INFO application started successfully", "uncategorized"),
("INFO user pressed the pause button", "uncategorized"),
("ERROR network timeout during database query", "network"),
("INFO SERVER   CONNECTION restored", "network")]
rules = [("network", r"\b(network|connection|timeout|packet)\b"), ("database", r"\b(database|query|backup)\b"), ("performance", r"\b(gpu|cpu|rendering|frame)\b"), ("security", r"\b(authentication|password|token)\b"), ("data", r"\b(csv|sensor|data)\b")]
def normalize(message): return re.sub(r"\s+", " ", message.lower()).strip()
def classify(message):
    text = normalize(message)
    for label, pattern in rules:
        if re.search(pattern, text): return label
    return "uncategorized"
def severity(message):
    match = re.search(r"\b(ERROR|WARN|INFO)\b", message, flags=re.IGNORECASE)
    return match.group(1).upper() if match else "UNKNOWN"
frame = pd.DataFrame(examples, columns=["message", "expected_category"])
frame["normalized"] = frame.message.map(normalize)
frame["category"] = frame.message.map(classify)
frame["severity"] = frame.message.map(severity)
assert classify("unfamiliar event") == "uncategorized"
assert classify("DATABASE backup") == "database"
assert severity("unlabelled message") == "UNKNOWN"
assert normalize("  A   B  ") == "a b"
frame.to_csv(OUT / "triaged_logs.csv", index=False)
frame.groupby(["category", "severity"]).size().rename("count").reset_index().to_csv(OUT / "category_summary.csv", index=False)
metrics = {"toy_messages": len(frame), "toy_expected_label_accuracy": float((frame.category == frame.expected_category).mean()), "uncategorized_count": int((frame.category == "uncategorized").sum()), "method": "ordered regex rules; no learned model"}
(OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
print(json.dumps(metrics, indent=2))
