## 🔍 How the Scanner Works

This tool scans files in the current directory to identify potential sensitive data exposure using regex pattern matching.

### Functionality

1. Recursively walks through all files in the directory
2. Reads each file line by line
3. Applies regex patterns to detect:
   - AWS Access Keys
   - Generic API keys (tokens, secrets)
   - Email addresses
4. Prints findings with:
   - File name
   - Line number
   - Matched content

---

## ⚠️ Initial Limitation

The first version of the scanner also scanned the `.git` directory, which resulted in false positives from internal Git files.

---

## 🔧 Improvement

The scanner was updated to exclude the `.git` directory from scanning.

This significantly reduced noise and improved the accuracy of results, aligning with real-world security tool behavior.

## 📊 Output and Severity Levels

The scanner categorizes findings based on severity:

- HIGH → Critical secrets (e.g., AWS keys)
- MEDIUM → Potential sensitive data (API keys, tokens)
- LOW → Informational (emails)

Results are printed to the terminal and saved to `findings.txt` for further analysis.

## Upgraded into specifying a folder to scan

can specify the folder the scan on the CLI in the following format 
python3 scanner.py <folder-to-scan>

## 🛠️ Usage

Run the scanner with:

```bash
python3 scanner.py --path <directory> --output <file>