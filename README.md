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