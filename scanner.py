import os
import re
import sys
import argparse

# Define patterns to search for
patterns = {
    "AWS Access Key": {
        "regex": r"AKIA[0-9A-Z]{16}",
        "severity": "HIGH"
    },
    "Generic API Key": {
        "regex": r"(api_key|token|secret)[=: ]+[A-Za-z0-9]+",
        "severity": "MEDIUM"
    },
    "Email": {
        "regex": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
        "severity": "LOW"
    }
}

def scan_file(filepath):
    findings = []

    try:
        with open(filepath, "r", errors="ignore") as file:
            for line_number, line in enumerate(file, 1):
                for name, details in patterns.items():
                    matches = re.findall(details["regex"], line)
                    if matches:
                        findings.append({
                            "type": name,
                            "severity": details["severity"],
                            "line": line_number,
                            "content": line.strip()
                        })
    except Exception:
        pass

    return findings


def scan_directory(directory):
    all_findings = []

    for root, dirs, files in os.walk(directory):
        # Exclude .git directory
        dirs[:] = [d for d in dirs if d != ".git"]
        for file in files:
            filepath = os.path.join(root, file)
            results = scan_file(filepath)
            for result in results:
                result["file"] = filepath
                all_findings.append(result)

    return all_findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Secret Scanner")

    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Directory to scan"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="findings.txt",
        help="Output file name"
    )

    args = parser.parse_args()

    print(f"🔍 Scanning for secrets in: {args.path}\n")

    findings = scan_directory(args.path)

    if findings:
        with open(args.output, "w") as output:
            for f in findings:
                line = f"[{f['severity']}] {f['type']} found in {f['file']} (Line {f['line']}): {f['content']}\n"
                print(line)
                output.write(line)

        print(f"\n📄 Findings saved to {args.output}")
    else:
        print("✅ No secrets found.")
