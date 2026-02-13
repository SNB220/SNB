# SNB - Complete Feature List

## ✅ Implemented Features

### 1. Core Functionality
- ✅ **Command Wrapping**: Wrap any command to save its output
- ✅ **Real-time Display**: Shows output in terminal while saving
- ✅ **Organized Storage**: Separate folders for each tool
- ✅ **Timestamped Files**: Format: `DD.MM.YYYY`
- ✅ **Multiple Runs**: Counter suffixes for same-day runs
- ✅ **Cross-platform**: Windows, Linux, macOS
- ✅ **Piped Input**: Works with `command | snb`

### 2. Installation
- ✅ **Windows**: `install.bat` with PATH setup
- ✅ **Linux/macOS**: `install.sh` with shell integration
- ✅ **System-wide**: Accessible from any directory

### 3. Custom Tags/Filenames (`-t`, `--tag`)
- ✅ Add descriptive tags to output files
- ✅ Organize scans by purpose, client, or phase
- ✅ Example: `snb -t web-scan nmap target.com`
- ✅ Output: `web-scan_23.11.2025.txt`

### 4. Output Formats (`-f`, `--format`)
- ✅ **TXT**: Plain text (default)
- ✅ **JSON**: Structured data with metadata
- ✅ **HTML**: Styled dark theme reports
- ✅ **Markdown**: Documentation-ready format
- ✅ Example: `snb -f html nmap target.com`

### 5. Save All Formats (`-A`, `--all`)
- ✅ Save in TXT, JSON, HTML, MD simultaneously
- ✅ One command, all formats
- ✅ Example: `snb -A nmap target.com`
- ✅ Creates: `.txt`, `.json`, `.html`, `.md` files

### 6. Auto-Compression
- ✅ Automatically compresses old files (7+ days default)
- ✅ `.txt` → `.txt.gz` with gzip
- ✅ 70-90% disk space savings
- ✅ Configurable via `SNB_AUTO_COMPRESS_DAYS` environment variable
- ✅ Runs automatically on each SNB execution

### 7. Session Management (`-s`, `--session`)
- ✅ Organize scans by project/engagement
- ✅ Folder structure: `snb_outputs/sessions/[session-name]/[tool]/`
- ✅ Example: `snb -s pentest-alpha nmap target.com`
- ✅ Perfect for multi-target projects
- ✅ Easy sharing and organization

### 8. Time Tracking
- ✅ Automatic execution time measurement
- ✅ Displayed in console output
- ✅ Saved in all output formats
- ✅ Format: `HH:MM:SS`
- ✅ JSON includes: `execution_time` and `execution_time_seconds`

### 9. Filter/Grep Options (`-g`, `--grep`)
- ✅ Filter output by regex pattern
- ✅ Real-time filtering in console
- ✅ Filtered content saved to file
- ✅ Case-insensitive matching
- ✅ Example: `snb -g "open" nmap target.com`
- ✅ Shows match statistics in output

### 10. Search/Query Functionality (`--search`)
- ✅ Search through all saved outputs
- ✅ Regex pattern matching
- ✅ Search all tools or specific tool
- ✅ Handles compressed `.txt.gz` files automatically
- ✅ Highlights matches with `>>>match<<<`
- ✅ Shows line numbers and context
- ✅ Example: `snb --search "VULNERABLE" nmap`
- ✅ Searches both regular and session outputs

### 11. Configuration
- ✅ **Custom Output Directory**: `SNB_OUTPUT_DIR` environment variable
- ✅ **Compression Threshold**: `SNB_AUTO_COMPRESS_DAYS` environment variable
- ✅ Works across all platforms

### 12. Error Handling
- ✅ Graceful Ctrl+C (KeyboardInterrupt) handling
- ✅ Command not found errors
- ✅ File permission errors
- ✅ Exit code preservation
- ✅ Error messages in saved output

### 13. Metadata Tracking
- ✅ Tool name
- ✅ Full command executed
- ✅ Timestamp (start time)
- ✅ Return code
- ✅ Execution time
- ✅ Filter pattern (if used)
- ✅ All metadata in JSON format

## 📊 Feature Combinations

All features work together seamlessly:

```bash
# Session + Tag + Filter + All Formats
snb -s project-alpha -t web-scan -g "200" -A gobuster dir -u http://target.com

# Session + Tag + Custom Format
snb -s pentest-2025 -t recon -f html nmap -A target.com

# Filter + Search
snb -g "VULNERABLE" nmap --script vuln target.com
snb --search "VULNERABLE" nmap

# All features combined
snb -s client-engagement -t initial-scan -g "open" -A nmap -sV target.com
```

## 🎯 Use Case Examples

### Penetration Testing
```bash
# Organize by engagement
snb -s client-2025 -t network-scan nmap -sV 192.168.1.0/24
snb -s client-2025 -t web-enum gobuster dir -u http://target.com

# Search for vulnerabilities
snb --search "VULNERABLE|CVE-" nmap
```

### Bug Bounty
```bash
# Track different programs
snb -s hackerone-target1 -t subdomain-enum sublist3r -d target.com
snb -s bugcrowd-target2 -t port-scan nmap target.com

# Find interesting findings
snb --search "admin|login" gobuster
```

### Security Research
```bash
# Save comprehensive reports
snb -A -t research-scan nmap --script vuln target.com

# Filter for specific issues
snb -g "SSL|TLS" nikto -h https://target.com

# Query historical data
snb --search "CVE-2024" nmap
```

### System Administration
```bash
# Track system states
snb -s production-server -t health-check ipconfig /all
snb -s production-server -t process-check Get-Process

# Review past outputs
snb --search "error" ipconfig
```

## 📈 Statistics

- **Total Features**: 13 major features
- **Command-line Flags**: 7 flags (`-t`, `-f`, `-A`, `-s`, `-g`, `--search`, `--`)
- **Output Formats**: 4 formats (TXT, JSON, HTML, MD)
- **Platforms**: 3 platforms (Windows, Linux, macOS)
- **File Types Handled**: 2 types (`.txt`, `.txt.gz`)
- **Environment Variables**: 2 variables
- **Lines of Code**: ~689 lines

## 🔄 Workflow Integration

SNB fits perfectly into security workflows:

1. **Reconnaissance**: Use sessions to organize
2. **Scanning**: Use filters to focus on findings
3. **Enumeration**: Use tags for different targets
4. **Reporting**: Use HTML format for clients
5. **Analysis**: Use search to query historical data
6. **Automation**: Use JSON for parsing
7. **Documentation**: Use Markdown for wikis

## 🚀 Performance

- **Real-time output**: No delay in command execution
- **Compression**: Automatic background compression
- **Search**: Fast regex search across thousands of files
- **Filtering**: Real-time pattern matching
- **No overhead**: Minimal performance impact

## 📝 Output Quality

All saved files include:
- Professional headers with metadata
- Execution statistics
- Proper formatting for each format
- Filter information (when used)
- Complete command output
- Return code and error handling

---

**SNB is production-ready and feature-complete!** 🎉
