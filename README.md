# SNB - Save 'N' Backup

A cross-platform command-line wrapper tool that automatically saves the output of any command to organized, timestamped files.

## 🎯 Features

- **Cross-platform**: Works on Windows, Linux, and macOS
- **Wrap any command**: Use SNB before any command to capture its output
- **Organized storage**: Automatically creates separate folders for each tool
- **Timestamped files**: Saves output with date format `snb_DD.MM.YYYY.txt`
- **Real-time display**: Shows output in the terminal while saving
- **Pipe support**: Works with piped input from other commands
- **Multiple runs**: Handles multiple runs on the same day with counter suffixes
- **Auto-compression**: Automatically compresses files older than 7 days to save disk space
- **Custom tags**: Add descriptive tags to organize outputs by project or purpose
- **Multiple formats**: Save outputs in TXT, JSON, HTML, or Markdown formats
- **Session management**: Organize scans by project or engagement
- **Time tracking**: Automatic execution time measurement for every command
- **Filter/grep options**: Display and save only matching lines with regex patterns
- **Search functionality**: Query all saved outputs with powerful regex search

## 📦 Installation

### Requirements
- Python 3.6 or higher
- Windows, Linux, or macOS

### Windows Installation

1. **Navigate to SNB folder**
   ```powershell
   cd C:\Users\nabie\Downloads\SNB
   ```

2. **Run the installation script**
   ```powershell
   .\install.bat
   ```

3. **Restart your terminal**

4. **Verify installation**
   ```powershell
   snb echo "Hello, SNB!"
   ```

### Linux/macOS Installation

1. **Navigate to SNB folder**
   ```bash
   cd ~/Downloads/SNB
   ```

2. **Run the installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Apply changes**
   ```bash
   source ~/.bashrc  # or ~/.zshrc for zsh
   # OR restart your terminal
   ```

4. **Verify installation**
   ```bash
   snb echo "Hello, SNB!"
   ```

## 🚀 Usage

### Basic Command Wrapping

Simply prefix your command with `snb`:

#### Security Tools
```bash
# Nmap
snb nmap -sV example.com
snb nmap -A -T4 192.168.1.1

# Gobuster
snb gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt

# Dirsearch
snb dirsearch -u http://example.com -e php,html

# Nikto
snb nikto -h http://example.com

# Masscan
snb masscan -p1-65535 192.168.1.0/24 --rate=1000

# WhatWeb
snb whatweb example.com

# SQLMap
snb sqlmap -u "http://example.com/page?id=1" --batch

# WPScan
snb wpscan --url http://example.com
```

### Custom Tags/Names

Use `-t` or `--tag` to add custom tags to your output filenames:

```bash
# Basic usage
snb -t web-scan nmap -sV example.com
# Saves as: snb_outputs/nmap/web-scan_23.11.2025.txt

snb -t initial-recon gobuster dir -u http://target.com -w wordlist.txt
# Saves as: snb_outputs/gobuster/initial-recon_23.11.2025.txt

snb --tag production-audit nikto -h https://prod.example.com
# Saves as: snb_outputs/nikto/production-audit_23.11.2025.txt

# Multiple scans with different tags
snb -t port-scan nmap -p- target.com
snb -t vuln-scan nmap --script vuln target.com
snb -t service-scan nmap -sV target.com
# Creates: port-scan_23.11.2025.txt, vuln-scan_23.11.2025.txt, service-scan_23.11.2025.txt
```

**Benefits:**
- Organize scans by purpose, client, or phase
- Easy identification without opening files
- Better project management

### Output Formats

SNB supports multiple output formats to suit different needs:

```bash
# Plain text (default)
snb nmap -sV target.com
# Saves as: snb_outputs/nmap/snb_23.11.2025.txt

# JSON format
snb -f json nmap -sV target.com
# Saves as: snb_outputs/nmap/snb_23.11.2025.json
# Perfect for parsing and automation

# HTML format (with styled dark theme)
snb -f html gobuster dir -u http://target.com -w wordlist.txt
# Saves as: snb_outputs/gobuster/snb_23.11.2025.html
# Beautiful reports you can view in a browser

# Markdown format
snb -f md dirsearch -u http://target.com
# Saves as: snb_outputs/dirsearch/snb_23.11.2025.md
# Great for documentation and GitHub

# Combine with custom tags
snb -t production -f html nmap -sV prod-server.com
# Saves as: snb_outputs/nmap/production_23.11.2025.html
```

**Format Details:**

| Format | Extension | Best For |
|--------|-----------|----------|
| `txt` | `.txt` | Default, simple viewing |
| `json` | `.json` | Automation, parsing, APIs |
| `html` | `.html` | Professional reports, presentations |
| `md` | `.md` | Documentation, GitHub, wikis |

**JSON Example:**
```json
{
  "metadata": {
    "tool": "nmap",
    "command": "nmap -sV target.com",
    "timestamp": "2025-11-23 14:30:00",
    "return_code": 0
  },
  "output": "...",
  "output_lines": ["line1", "line2", ...]
}
```

**HTML Features:**
- Dark theme optimized for security professionals
- Syntax highlighting
- Responsive design
- Print-friendly
- Professional styling

### Save All Formats at Once

Use `-A` or `--all` to save output in **all formats simultaneously**:

```bash
# Save in TXT, JSON, HTML, and MD formats at once
snb -A nmap -sV target.com

# Output:
# ✓ snb_outputs/nmap/snb_23.11.2025.txt
# ✓ snb_outputs/nmap/snb_23.11.2025.json
# ✓ snb_outputs/nmap/snb_23.11.2025.html
# ✓ snb_outputs/nmap/snb_23.11.2025.md

# Combine with custom tags
snb -t web-scan -A gobuster dir -u http://target.com -w wordlist.txt

# Output:
# ✓ snb_outputs/gobuster/web-scan_23.11.2025.txt
# ✓ snb_outputs/gobuster/web-scan_23.11.2025.json
# ✓ snb_outputs/gobuster/web-scan_23.11.2025.html
# ✓ snb_outputs/gobuster/web-scan_23.11.2025.md
```

**Benefits of `-A` flag:**
- Maximum flexibility - view output in any format later
- Perfect for generating reports (use HTML)
- Easy automation (use JSON)
- Documentation ready (use MD)
- One command, all formats! 🎯

### Session Management

Organize your scans by project, client, or engagement using sessions:

```bash
# Create a session for a specific project
snb -s pentest-alpha nmap -sV target1.com
snb -s pentest-alpha gobuster dir -u http://target1.com -w wordlist.txt
snb -s pentest-alpha nikto -h target1.com

# All outputs go to: snb_outputs/sessions/pentest-alpha/

# Different project, different session
snb -s client-beta nmap -sV target2.com
snb -s client-beta dirsearch -u http://target2.com

# Outputs go to: snb_outputs/sessions/client-beta/

# Without session (default behavior)
snb nmap -sV target3.com
# Outputs go to: snb_outputs/nmap/
```

**Session Folder Structure:**
```
snb_outputs/
├── sessions/
│   ├── pentest-alpha/
│   │   ├── nmap/
│   │   │   ├── snb_23.11.2025.txt
│   │   │   └── snb_24.11.2025.txt
│   │   ├── gobuster/
│   │   │   └── snb_23.11.2025.txt
│   │   └── nikto/
│   │       └── snb_23.11.2025.txt
│   │
│   └── client-beta/
│       ├── nmap/
│       │   └── snb_23.11.2025.txt
│       └── dirsearch/
│           └── snb_23.11.2025.txt
│
└── nmap/  ← Default (no session)
    └── snb_23.11.2025.txt
```

**Combine Session with Other Features:**
```bash
# Session + Custom Tag + All Formats
snb -s red-team-2025 -t initial-recon -A nmap -sn 192.168.1.0/24

# Session + HTML Report
snb -s client-report -t final-scan -f html nmap -A target.com

# Session + Tag
snb -s webapp-test -t login-page gobuster dir -u http://target.com/login -w wordlist.txt
```

**Benefits:**
- **Project Isolation**: Keep different engagements separate
- **Easy Sharing**: Share entire session folder with team
- **Clean Organization**: All related scans in one place
- **Client Deliverables**: Organize by client for easy handoff
- **Time Management**: Track all work for a specific project

**Real-World Examples:**
```bash
# Bug Bounty Program
snb -s hackerone-target nmap -sV target.com
snb -s hackerone-target ffuf -u https://target.com/FUZZ -w wordlist.txt

# Penetration Testing Engagement
snb -s pentest-2025-11 -t network-scan nmap -A 192.168.1.0/24
snb -s pentest-2025-11 -t web-scan nikto -h https://client.com
snb -s pentest-2025-11 -t directory-enum gobuster dir -u https://client.com -w common.txt

# CTF Challenge
snb -s htb-machine1 nmap -sV 10.10.10.100
snb -s htb-machine1 -t web-enum gobuster dir -u http://10.10.10.100 -w wordlist.txt
```

### Time Tracking

SNB automatically tracks execution time for every command:

```bash
# Run any command - time is tracked automatically
snb nmap -p- target.com

# Console output shows:
# [SNB] Running: nmap -p- target.com
# [SNB] Started at: 2025-11-23 14:30:00
# ... command output ...
# --------------------------------------------------------------------------------
# [SNB] Execution completed in: 0:05:23
# [SNB] Output saved to: snb_outputs/nmap/snb_23.11.2025.txt

# Time is saved in all output formats
```

**Saved Output Includes:**
```
================================================================================
SNB - Command Output Log
================================================================================
Tool: nmap
Command: nmap -p- target.com
Timestamp: 2025-11-23 14:30:00
Return Code: 0
Execution Time: 0:05:23
================================================================================

[command output...]
```

**JSON Format:**
```json
{
  "metadata": {
    "tool": "nmap",
    "command": "nmap -p- target.com",
    "timestamp": "2025-11-23 14:30:00",
    "return_code": 0,
    "execution_time": "0:05:23",
    "execution_time_seconds": 323.45
  },
  "output": "..."
}
```

**Benefits:**
- Track scan duration for billing/reporting
- Identify slow scans that need optimization
- Performance metrics for different tools
- Useful for time management and planning
- Perfect for reports showing work effort

**Examples:**
```bash
# Quick scan
snb nmap -F target.com
# Execution Time: 0:00:12

# Full scan
snb nmap -A -T4 -p- target.com
# Execution Time: 0:15:47

# Directory enumeration
snb gobuster dir -u http://target.com -w big.txt
# Execution Time: 0:08:35
```

### Filter/Grep Options

Filter command output to display and save only matching lines:

```bash
# Basic pattern matching
snb -g "open" nmap -sV target.com
# Only shows/saves lines containing "open"

# Filter for specific ports
snb -g "port 80|port 443" nmap target.com
# Shows only lines with port 80 or 443

# Case-insensitive matching (default)
snb -g "error" gobuster dir -u http://target.com -w wordlist.txt
# Shows lines with "error", "Error", "ERROR", etc.

# Filter successful responses
snb -g "Status: 200" gobuster dir -u http://target.com -w wordlist.txt

# Complex regex patterns
snb -g "^\[.*\].*admin" dirsearch -u http://target.com
# Matches lines starting with brackets containing "admin"

# Look for vulnerabilities
snb -g "VULNERABLE" nmap --script vuln target.com
# Only saves lines mentioning vulnerabilities
```

**How it works:**
1. **Real-time filtering**: Only matching lines displayed in console
2. **Full output saved**: Complete output saved to file (with filter stats)
3. **Filtered section**: Saved file includes both filter info and matched lines
4. **Regex support**: Use full regex patterns for complex filtering

**Saved Output Format:**
```
[SNB Filter Applied: open]
[Matched 15 lines out of 1247 total lines]

22/tcp   open  ssh     OpenSSH 8.2p1
80/tcp   open  http    Apache httpd 2.4.41
443/tcp  open  ssl/http Apache httpd 2.4.41
...
```

**Combine with Other Features:**
```bash
# Filter + Custom Tag + Session
snb -s pentest-alpha -t open-ports -g "open" nmap -p- target.com

# Filter + All Formats
snb -g "200" -A gobuster dir -u http://target.com -w wordlist.txt
# Creates filtered TXT, JSON, HTML, MD files

# Filter + HTML Report
snb -g "VULNERABLE|LIKELY VULNERABLE" -f html nmap --script vuln target.com
# Beautiful HTML report with only vulnerabilities
```

**Use Cases:**
- **Focus on findings**: Only see/save relevant results
- **Reduce noise**: Filter out unimportant information
- **Quick analysis**: Instantly see what matters
- **Clean reports**: Share filtered results with clients
- **Vulnerability hunting**: Extract security issues only

**Examples:**
```bash
# Find open web ports
snb -g "80|443|8080|8443" nmap -p- target.com

# Extract successful directory findings
snb -g "Status: 200|Status: 301|Status: 302" gobuster dir -u http://target.com -w wordlist.txt

# Show only SSL/TLS info
snb -g "ssl|tls" nmap -sV target.com

# Filter error messages
snb -g "error|fail|denied" nikto -h http://target.com

# Find admin panels
snb -g "admin|login|dashboard" dirsearch -u http://target.com
```

**Metadata in JSON:**
```json
{
  "metadata": {
    "tool": "nmap",
    "command": "nmap -sV target.com",
    "filter_pattern": "open",
    ...
  }
}
```

### Search/Query Saved Outputs

Search through all your saved scan outputs to find specific information:

```bash
# Basic search - searches all tools
snb --search "VULNERABLE"
# Searches all saved outputs for "VULNERABLE"

# Search specific tool
snb --search "port 80" nmap
# Only searches nmap outputs

snb --search "admin" gobuster
# Only searches gobuster outputs

# Search for patterns
snb --search "200|301|302" gobuster
# Find all successful HTTP responses in gobuster scans

snb --search "open.*ssh" nmap
# Find open SSH ports in nmap scans

# Case-insensitive by default
snb --search "error"
# Matches: error, Error, ERROR, ErRoR

# Complex regex patterns
snb --search "(\d{1,3}\.){3}\d{1,3}" nmap
# Find all IP addresses in nmap scans

snb --search "CVE-\d{4}-\d{4,7}"
# Find CVE references in any scan
```

**How it works:**
- Searches through `.txt` and `.txt.gz` (compressed) files
- Uses regex pattern matching (case-insensitive)
- Searches in both regular outputs and session folders
- Shows file path, line numbers, and highlighted matches
- Displays up to 5 matches per file (shows total if more)
- Provides summary of total files with matches

**Output Example:**
```
Searching for pattern: VULNERABLE
Searching in: snb_outputs/

File: snb_outputs/nmap/vuln-scan_23.11.2025.txt
  Line 45: |     State: VULNERABLE
  Line 67: |     State: LIKELY VULNERABLE (exploit available)
  Line 89: |   VULNERABLE:
  ... and 3 more matches

File: snb_outputs/sessions/client-alpha/nmap/snb_22.11.2025.txt
  Line 102: | ssl-ccs-injection: VULNERABLE
  Line 156: |   MS17-010: VULNERABLE

Search complete: Found matches in 2 file(s)
```

**Real-World Use Cases:**

```bash
# Find all vulnerabilities across all scans
snb --search "VULNERABLE|CVE-" 

# Find successful directory discoveries
snb --search "Status: 200" gobuster

# Find admin panels across all web scans
snb --search "admin|login|dashboard"

# Find specific ports
snb --search "port 8080|port 8443"

# Search session outputs
snb --search "error" nmap  # Searches in both regular and session folders

# Find SSL/TLS issues
snb --search "ssl|tls|certificate"

# Find specific IP in scans
snb --search "192\.168\.1\.100"

# Extract password findings
snb --search "password|passwd|credentials"
```

**Benefits:**
- **Quick retrieval**: No need to manually search through files
- **Cross-scan analysis**: Find patterns across multiple tool outputs
- **Historical data**: Search weeks/months of saved scans
- **Compressed file support**: Automatically decompresses and searches `.gz` files
- **Regex power**: Use complex patterns for precise searches
- **Session-aware**: Searches both regular and session-organized outputs

**Combine with Other Tools:**
```bash
# Search and save results
snb --search "VULNERABLE" nmap > vulnerabilities.txt

# Search multiple patterns
snb --search "80|443|8080|8443" nmap | grep -i "open"

# Count occurrences
snb --search "error" | wc -l
```

**Performance Tips:**
- Search specific tool instead of all outputs for faster results
- Use more specific patterns to reduce output
- Compressed files take slightly longer to search (automatic decompression)
- Large directories may take time - consider using sessions to organize outputs

#### System Commands
```bash
# Linux/macOS
snb ls -la
snb ps aux
snb netstat -tulpn
snb ifconfig

# Windows
snb ipconfig /all
snb netstat -ano
snb Get-Process
```

#### Any Command
```bash
snb curl -I https://example.com
snb ping -c 4 google.com
snb traceroute google.com
snb dig example.com
```

### Piped Input

You can also pipe output from any command to SNB:

```bash
# Linux/macOS
nmap -sV example.com | snb
cat /etc/passwd | snb
curl https://api.example.com | snb

# Windows
ipconfig | snb
Get-Process | snb
```

## 📁 Output Structure

SNB creates an organized folder structure:

```
snb_outputs/
├── nmap/
│   ├── snb_22.11.2025.txt
│   ├── web-scan_22.11.2025.txt
│   ├── port-scan_23.11.2025.txt
│   └── vuln-scan_23.11.2025.txt
├── gobuster/
│   ├── initial-recon_22.11.2025.txt
│   └── deep-scan_23.11.2025.txt
├── dirsearch/
│   └── snb_22.11.2025.txt
└── piped_input/
    └── snb_22.11.2025.txt
```

### Output File Format

Each saved file contains:
- Tool name
- Full command executed
- Timestamp
- Return code (exit status)
- Complete output

Example:
```
================================================================================
SNB - Command Output Log
================================================================================
Tool: nmap
Command: nmap -sV example.com
Timestamp: 2025-11-22 14:30:45
Return Code: 0
================================================================================

Starting Nmap...
[output continues...]
```

## ⚙️ Configuration

### Custom Output Directory

By default, SNB saves outputs to `snb_outputs/` in the current directory. To change this, set the `SNB_OUTPUT_DIR` environment variable:

#### Linux/macOS
```bash
# Temporary (current session)
export SNB_OUTPUT_DIR="/home/user/scans"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export SNB_OUTPUT_DIR="/home/user/scans"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows
```powershell
# Temporary (current session)
$env:SNB_OUTPUT_DIR = "C:\MyScans"

# Permanent
[Environment]::SetEnvironmentVariable("SNB_OUTPUT_DIR", "C:\MyScans", "User")
```

### Auto-Compression Settings

By default, SNB automatically compresses `.txt` files older than 7 days into `.txt.gz` files to save disk space. You can customize this:

#### Linux/macOS
```bash
# Set custom compression age (in days)
export SNB_AUTO_COMPRESS_DAYS=14  # Compress files older than 14 days

# Disable auto-compression
export SNB_AUTO_COMPRESS_DAYS=999999

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export SNB_AUTO_COMPRESS_DAYS=14' >> ~/.bashrc
```

#### Windows
```powershell
# Set custom compression age
$env:SNB_AUTO_COMPRESS_DAYS = "14"

# Permanent
[Environment]::SetEnvironmentVariable("SNB_AUTO_COMPRESS_DAYS", "14", "User")
```

**How it works:**
- Every time you run SNB, it checks for old files
- Files older than the threshold are automatically compressed with gzip
- Original `.txt` files are replaced with `.txt.gz` files
- Compressed files use ~70-90% less disk space
- You can decompress with: `gunzip filename.txt.gz` or `gzip -d filename.txt.gz`

## 🛠️ Advanced Usage

### Security Scanning Workflow

```bash
# Reconnaissance phase
snb nmap -sn 192.168.1.0/24                    # Host discovery
snb nmap -sV -p- target.com                    # Port scanning
snb whatweb target.com                          # Technology detection

# Web application testing
snb gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
snb nikto -h target.com
snb dirb http://target.com

# Vulnerability scanning
snb nmap --script vuln target.com
```

### Organizing Multiple Scans

```bash
# Set custom output directory for a project
export SNB_OUTPUT_DIR="/home/user/pentest/ProjectAlpha"

# Run multiple tools - all output goes to ProjectAlpha folder
snb nmap -sV target.com
snb whatweb target.com
snb gobuster dir -u http://target.com -w wordlist.txt
```

### Integration with Scripts

```bash
# Scan multiple targets from a file
while read target; do
    snb nmap -sV "$target"
done < targets.txt

# Chain multiple operations
snb nmap -sV target.com && snb gobuster dir -u http://target.com -w wordlist.txt
```

## 📋 Examples

### Example 1: Network Scanning
```bash
snb nmap -p- -A 192.168.1.1
# Output saved to: snb_outputs/nmap/snb_22.11.2025.txt

# With custom tag
snb -t full-scan nmap -p- -A 192.168.1.1
# Output saved to: snb_outputs/nmap/full-scan_22.11.2025.txt
```

### Example 2: Directory Enumeration
```bash
snb gobuster dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt
# Output saved to: snb_outputs/gobuster/snb_22.11.2025.txt

# Organized by target
snb -t site1 gobuster dir -u https://site1.com -w wordlist.txt
snb -t site2 gobuster dir -u https://site2.com -w wordlist.txt
# Creates: site1_22.11.2025.txt, site2_22.11.2025.txt
```

### Example 3: Multiple Runs Same Day
```bash
snb dirsearch -u http://site1.com
# Saved to: snb_outputs/dirsearch/snb_22.11.2025.txt

snb dirsearch -u http://site2.com
# Saved to: snb_outputs/dirsearch/snb_22.11.2025_1.txt

# Better with tags:
snb -t site1 dirsearch -u http://site1.com
snb -t site2 dirsearch -u http://site2.com
# Creates: site1_22.11.2025.txt, site2_22.11.2025.txt
```

### Example 4: Using with Sudo
```bash
# For tools requiring root privileges
sudo env "PATH=$PATH" snb nmap -sS target.com
# or create an alias
alias ssnb='sudo env "PATH=$PATH" snb'
ssnb nmap -sS target.com
```

## 🔧 Troubleshooting

### Command not found (Linux/macOS)
- Make sure you ran `install.sh`
- Run `source ~/.bashrc` (or `~/.zshrc` for zsh)
- Verify the SNB directory is in your PATH: `echo $PATH`
- Check that `snb` script exists and is executable: `ls -la ~/Downloads/SNB/snb`

### Command not found (Windows)
- Make sure you ran `install.bat`
- Restart your terminal after installation
- Verify `snb.bat` exists in the SNB directory
- Check PATH: `$env:PATH`

### Python not found
- **Linux**: `sudo apt install python3` (Ubuntu/Debian) or `sudo yum install python3` (CentOS/RHEL)
- **macOS**: `brew install python3` or download from [python.org](https://www.python.org/downloads/)
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- Verify: `python3 --version` (Linux/macOS) or `python --version` (Windows)

### Permission denied errors
- **Linux/macOS**: Use `sudo` with the command or fix output directory permissions
- **Windows**: Run terminal as Administrator or change output directory

### Output not being saved
- Check write permissions for the current/output directory
- Set a custom output directory with proper permissions
- Check available disk space: `df -h` (Linux/macOS) or `Get-PSDrive` (Windows)

## 📝 Uninstallation

### Linux/macOS
```bash
# Remove from shell configuration
sed -i '/# SNB - Save/d' ~/.bashrc
sed -i '/SNB/d' ~/.bashrc
source ~/.bashrc

# Delete the SNB folder
rm -rf ~/Downloads/SNB
```

### Windows
```powershell
# Remove from PATH (use Environment Variables editor)
rundll32 sysdm.cpl,EditEnvironmentVariables

# Delete the SNB folder
Remove-Item -Recurse -Force "C:\Users\nabie\Downloads\SNB"
```

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available for personal and commercial use.

## 💡 Tips

- Use SNB for penetration testing to maintain organized logs of all scans
- Combine with version control to track scan results over time
- Set project-specific output directories for organized engagements
- Review saved outputs later without re-running time-consuming scans
- Share output files with team members for collaborative analysis
- Use with `tmux` or `screen` for long-running scans
- Create shell aliases for frequently used SNB commands

## 🚀 Quick Reference

### Common Use Cases
```bash
# Quick port scan
snb nmap -F target.com

# Full scan
snb nmap -A -T4 -p- target.com

# Web directory scan
snb gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt -x php,html,txt

# Vulnerability scan
snb nmap --script vuln target.com

# Subdomain enumeration
snb sublist3r -d example.com
```

---

**Happy Scanning!** 🔍🛡️
