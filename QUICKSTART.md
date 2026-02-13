# SNB - Quick Reference Guide

## Installation

### Windows
```powershell
cd C:\Users\nabie\Downloads\SNB
.\install.bat
# Restart terminal
snb echo "Hello SNB!"
```

### Linux/macOS
```bash
cd ~/Downloads/SNB
chmod +x install.sh
./install.sh
source ~/.bashrc  # or ~/.zshrc
snb echo "Hello SNB!"
```

## Basic Usage

```bash
# Wrap any command
snb <command> [args...]

# Piped input
<command> | snb

# Examples
snb nmap -sV target.com
snb ipconfig /all
cat file.txt | snb
```

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `-t TAG` | Custom tag/filename | `snb -t web-scan nmap target.com` |
| `-f FORMAT` | Output format (txt/json/html/md) | `snb -f html nmap target.com` |
| `-A` | Save all formats | `snb -A nmap target.com` |
| `-s SESSION` | Session/project name | `snb -s pentest nmap target.com` |
| `-g PATTERN` | Filter by regex pattern | `snb -g "open" nmap target.com` |
| `--search PATTERN [TOOL]` | Search saved outputs | `snb --search "VULNERABLE" nmap` |

## Common Patterns

### Security Scanning
```bash
# Initial recon
snb -s target-alpha -t network-discovery nmap -sn 192.168.1.0/24
snb -s target-alpha -t port-scan nmap -p- target.com
snb -s target-alpha -t service-scan nmap -sV target.com

# Web enumeration
snb -s target-alpha -t dir-enum gobuster dir -u http://target.com -w wordlist.txt
snb -s target-alpha -t vuln-scan nikto -h http://target.com

# Filter for findings
snb -s target-alpha -t open-ports -g "open" nmap -p- target.com
snb -s target-alpha -t success-pages -g "200|301" gobuster dir -u http://target.com

# Generate reports
snb -s target-alpha -t final-report -A nmap -A target.com
```

### Search Historical Data
```bash
# Find vulnerabilities
snb --search "VULNERABLE|CVE-"
snb --search "VULNERABLE" nmap

# Find open ports
snb --search "80/tcp|443/tcp|8080/tcp" nmap

# Find successful responses
snb --search "Status: 200" gobuster

# Find admin panels
snb --search "admin|login|dashboard"
```

### Multiple Formats
```bash
# Save as JSON for automation
snb -f json nmap -sV target.com

# Save as HTML for reports
snb -f html -t client-report nmap -A target.com

# Save all formats
snb -A -t comprehensive nmap -A target.com
```

### Combine Everything
```bash
# Ultimate command
snb -s engagement-2025 -t initial-scan -g "open|VULNERABLE" -A nmap -sV -sC target.com

# Then search results
snb --search "VULNERABLE" nmap
snb --search "open.*80" nmap
```

## Environment Variables

```bash
# Custom output directory
export SNB_OUTPUT_DIR="/path/to/scans"  # Linux/macOS
$env:SNB_OUTPUT_DIR = "C:\Scans"        # Windows

# Compression threshold (days)
export SNB_AUTO_COMPRESS_DAYS=14        # Linux/macOS
$env:SNB_AUTO_COMPRESS_DAYS = 14        # Windows
```

## Output Structure

```
snb_outputs/
├── nmap/
│   ├── snb_23.11.2025.txt
│   ├── web-scan_23.11.2025.txt
│   └── old-scan_20.11.2025.txt.gz  # Auto-compressed
│
├── gobuster/
│   ├── dir-enum_23.11.2025.json
│   └── site1_23.11.2025.html
│
└── sessions/
    └── pentest-alpha/
        ├── nmap/
        │   └── snb_23.11.2025.txt
        └── gobuster/
            └── snb_23.11.2025.txt
```

## Tips & Tricks

### Aliases (add to ~/.bashrc or ~/.zshrc)
```bash
alias snmap='snb nmap'
alias sgobuster='snb gobuster'
alias ssnb='sudo env "PATH=$PATH" snb'  # For sudo commands
```

### Real-World Workflows

**Penetration Test**
```bash
# Phase 1: Discovery
snb -s client-2025 -t discovery nmap -sn 10.0.0.0/24

# Phase 2: Port Scanning
snb -s client-2025 -t full-scan -g "open" nmap -p- 10.0.0.50

# Phase 3: Service Detection
snb -s client-2025 -t services nmap -sV -sC 10.0.0.50

# Phase 4: Vulnerability Scanning
snb -s client-2025 -t vulns -g "VULNERABLE" nmap --script vuln 10.0.0.50

# Phase 5: Web Testing
snb -s client-2025 -t web-dirs gobuster dir -u http://10.0.0.50 -w wordlist.txt

# Generate final report
snb -s client-2025 -t final-report -A nmap -A 10.0.0.50

# Search for issues
snb --search "VULNERABLE|LIKELY VULNERABLE" nmap
snb --search "admin|backup" gobuster
```

**Bug Bounty**
```bash
# Subdomain enumeration
snb -s target-bounty -t subdomains sublist3r -d target.com

# Port scanning multiple hosts
snb -s target-bounty -t ports -A masscan -p1-65535 --rate=1000 targets.txt

# Web discovery
snb -s target-bounty -t web-enum -g "200|301" gobuster dir -u https://target.com

# Search across all scans
snb --search "admin|secret|backup|test" gobuster
```

**System Monitoring**
```bash
# Periodic snapshots
snb -s server-prod -t $(date +%Y%m%d) ipconfig /all
snb -s server-prod -t $(date +%Y%m%d) netstat -ano

# Review historical data
snb --search "error|fail" ipconfig
snb --search "LISTENING.*:80" netstat
```

## Troubleshooting

```bash
# Command not found
which snb  # Linux/macOS
where.exe snb  # Windows

# Check PATH
echo $PATH  # Linux/macOS
$env:PATH  # Windows

# Test basic functionality
snb echo "test"
echo "test" | snb

# Verify Python
python3 --version  # Linux/macOS
python --version   # Windows
```

## Quick Examples

```bash
# Basic
snb nmap target.com
snb -t web nmap target.com
snb -f json nmap target.com

# Intermediate
snb -s project -t scan1 nmap target.com
snb -g "open" nmap -p- target.com
snb -A nmap -sV target.com

# Advanced
snb -s pentest-2025 -t initial -g "open|VULNERABLE" -A nmap -A target.com
snb --search "CVE-2024|VULNERABLE" nmap

# Search
snb --search "pattern"               # Search all
snb --search "pattern" tool          # Search specific tool
snb --search "open.*80|443"          # Regex patterns
snb --search "VULNERABLE" nmap       # Find vulnerabilities
```

## Keyboard Shortcuts

- **Ctrl+C**: Gracefully terminate command (output still saved)
- **Ctrl+Z**: Suspend (Linux/macOS)

---

**For more details, see README.md** 📖
