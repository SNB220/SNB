#!/bin/bash
# SNB Installation Script for Linux/macOS
# This script sets up SNB to be accessible from anywhere in the command line

echo "========================================"
echo "SNB (Save 'N' Backup) - Installation"
echo "========================================"
echo ""

# Get the directory where this script is located
SNB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "SNB Directory: $SNB_DIR"
echo ""

# Make snb.py executable
chmod +x "$SNB_DIR/snb.py"
echo "[OK] Made snb.py executable"

# Create a wrapper script
WRAPPER_PATH="$SNB_DIR/snb"
cat > "$WRAPPER_PATH" << 'EOF'
#!/bin/bash
# SNB wrapper script
SNB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SNB_DIR/snb.py" "$@"
EOF

chmod +x "$WRAPPER_PATH"
echo "[OK] Created snb wrapper script"

echo ""
echo "========================================"
echo "Adding SNB to PATH"
echo "========================================"
echo ""

# Determine shell configuration file
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.bash_profile"
    fi
    SHELL_NAME="bash"
else
    SHELL_RC="$HOME/.profile"
    SHELL_NAME="shell"
fi

# Check if already in PATH
if echo "$PATH" | grep -q "$SNB_DIR"; then
    echo "[INFO] SNB directory is already in PATH"
else
    # Add to shell configuration
    echo "" >> "$SHELL_RC"
    echo "# SNB - Save 'N' Backup Tool" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:$SNB_DIR\"" >> "$SHELL_RC"
    
    echo "[OK] Added to $SHELL_RC"
    echo ""
    echo "[IMPORTANT] Run one of these commands to apply changes:"
    echo "  source $SHELL_RC"
    echo "  OR restart your terminal"
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Usage:"
echo "  snb nmap -sV example.com"
echo "  snb gobuster dir -u http://example.com -w wordlist.txt"
echo "  echo \"test\" | snb"
echo ""
echo "Output will be saved to: snb_outputs/[tool-name]/snb_DD.MM.YYYY.txt"
echo ""
echo "[!] Remember to run: source $SHELL_RC"
echo "    or restart your terminal!"
echo ""
