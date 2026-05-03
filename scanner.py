import os
import re

# Define patterns to search for
patterns = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Generic API Key": r"(api_key|token|secret)[=: ]+[A-Za-z0-9]+",
    "Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}"
}

def scan_file(filepath):
    findings = []

    try:
        with open(filepath, "r", errors="ignore") as file:
            for line_number, line in enumerate(file, 1):
                for name, pattern in patterns.items():
                    matches = re.findall(pattern, line)
                    if matches:
                        findings.append({
                            "type": name,
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
    print("🔍 Scanning for secrets...\n")
    findings = scan_directory(".")

    if findings:
        for f in findings:
            print(f"[{f['type']}] Found in {f['file']} (Line {f['line']}):")
            print(f"    {f['content']}\n")
    else:
        print("✅ No secrets found.")
