import json
import csv
from collections import Counter

# Load  Bandit report
with open("bandit_report.json") as file:
    data = json.load(file)

# issue types and names
issues = [
    (
        issue["test_id"],
        issue["issue_text"],
        issue["issue_severity"],
        issue["filename"],
        issue["line_number"],
    )
    for issue in data["results"]
]


# Count occurrences of each issue type
# issue_counts = Counter(issues)
# sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)


# Write to CSV
with open("Security Weaknesses.csv", mode="w") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["ID", "Issue Text", "Severity", "File Name", "Line Number"]
    )
    for (
        issue_id,
        issue_text,
        issue_severity,
        filename,
        line_number,
    ) in issues:
        writer.writerow(
            [
                issue_id.strip(),
                issue_text.strip(),
                issue_severity.strip(),
                filename.strip(),
                line_number,
            ]
        )

print("CSV has been generated.")
