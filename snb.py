#!/usr/bin/env python3
"""
SNB (Save 'N' Backup) - Command Output Logger
Wraps any command and saves its output to organized folders with timestamps.

Usage:
    snb <command> [args...]
    snb -t <tag> <command> [args...]
    snb -f <format> <command> [args...]
    snb -s <session> <command> [args...]
    snb -g <pattern> <command> [args...]
    snb -A <command> [args...]
    snb -s <session> -t <tag> -g "pattern" -A <command> [args...]
    snb --search <pattern> [tool]
    <command> | snb
    
Formats: txt (default), json, html, md
Use -A or --all to save in all formats simultaneously
Use -s or --session to organize scans by project/engagement
Use -g or --grep to filter output by pattern (regex supported)
Use --search to search through saved outputs
"""

import sys
import os
import subprocess
import datetime
import gzip
import shutil
import json
import re
from pathlib import Path


class SNB:
    def __init__(self, base_dir=None, auto_compress_days=7, custom_tag=None, output_format='txt', save_all_formats=False, session=None, filter_pattern=None):
        """Initialize SNB with a base directory for storing outputs."""
        if base_dir is None:
            # Use SNB_OUTPUT_DIR environment variable or default to current directory
            base_dir = os.environ.get('SNB_OUTPUT_DIR', os.getcwd())
        
        # If session is specified, create session subdirectory
        if session:
            self.base_dir = Path(base_dir) / "snb_outputs" / "sessions" / session
        else:
            self.base_dir = Path(base_dir) / "snb_outputs"
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.auto_compress_days = auto_compress_days
        self.custom_tag = custom_tag
        self.output_format = output_format.lower()
        self.save_all_formats = save_all_formats
        self.session = session
        self.filter_pattern = filter_pattern
        
        # Run auto-compression on initialization
        self.auto_compress_old_files()
    
    def get_tool_name(self, command):
        """Extract the tool name from the command."""
        if not command:
            return "piped_input"
        
        # Get the first part of the command (the actual tool name)
        tool = command[0].split('/')[-1].split('\\')[-1]
        # Remove extension if present
        tool = tool.split('.')[0]
        return tool
    
    def get_output_path(self, tool_name):
        """Create and return the output file path for the tool."""
        # Create tool-specific directory
        tool_dir = self.base_dir / tool_name
        tool_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with current date
        date_str = datetime.datetime.now().strftime("%d.%m.%Y")
        
        # Build base filename with custom tag if provided
        if self.custom_tag:
            # Sanitize tag (remove invalid filename characters)
            safe_tag = "".join(c for c in self.custom_tag if c.isalnum() or c in ('-', '_', ' ')).strip()
            safe_tag = safe_tag.replace(' ', '-')
            base_filename = f"{safe_tag}_{date_str}"
        else:
            base_filename = f"snb_{date_str}"
        
        # Determine file extension based on format
        extension_map = {
            'txt': '.txt',
            'json': '.json',
            'html': '.html',
            'md': '.md',
            'markdown': '.md'
        }
        extension = extension_map.get(self.output_format, '.txt')
        
        # Handle multiple runs on the same day
        counter = 1
        filename = f"{base_filename}{extension}"
        output_path = tool_dir / filename
        
        while output_path.exists():
            filename = f"{base_filename}_{counter}{extension}"
            output_path = tool_dir / filename
            counter += 1
        
        return output_path
    
    def run_command(self, command):
        """Run a command and capture its output."""
        start_time = datetime.datetime.now()
        
        try:
            # Run the command and capture output
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            
            # Print output in real-time and collect it
            print(f"[SNB] Running: {' '.join(command)}")
            print(f"[SNB] Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            if self.filter_pattern:
                print(f"[SNB] Filter: {self.filter_pattern}")
            print("-" * 80)
            
            try:
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        # Always collect the line
                        output_lines.append(line)
                        
                        # Only print if matches filter (or no filter)
                        if self.filter_pattern:
                            if re.search(self.filter_pattern, line, re.IGNORECASE):
                                print(line, end='')
                        else:
                            print(line, end='')
            except KeyboardInterrupt:
                print("\n[SNB] Interrupted by user")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            
            process.wait()
            
            end_time = datetime.datetime.now()
            execution_time = end_time - start_time
            
            return ''.join(output_lines), process.returncode, execution_time
            
        except FileNotFoundError:
            end_time = datetime.datetime.now()
            execution_time = end_time - start_time
            error_msg = f"Error: Command '{command[0]}' not found.\n"
            print(error_msg, file=sys.stderr)
            return error_msg, 1, execution_time
        except Exception as e:
            end_time = datetime.datetime.now()
            execution_time = end_time - start_time
            error_msg = f"Error executing command: {str(e)}\n"
            print(error_msg, file=sys.stderr)
            return error_msg, 1, execution_time
    
    def detect_tool_from_pipe(self):
        """Detect the tool name from the parent process when piped."""
        try:
            import psutil
            # Get the parent process
            parent = psutil.Process(os.getppid())
            
            # Get the command line of the parent
            cmdline = parent.cmdline()
            if cmdline:
                # Extract the tool name (first command in the pipeline)
                tool = cmdline[0].split('/')[-1].split('\\')[-1]
                tool = tool.split('.')[0]
                # Filter out common shells
                if tool not in ['bash', 'zsh', 'sh', 'dash', 'fish', 'ksh', 'tcsh']:
                    return tool
        except:
            pass
        
        return "piped_input"
    
    def read_piped_input(self):
        """Read input from a pipe."""
        print("[SNB] Reading from pipe...")
        print("-" * 80)
        
        output_lines = []
        try:
            for line in sys.stdin:
                print(line, end='')
                output_lines.append(line)
        except KeyboardInterrupt:
            print("\n[SNB] Interrupted by user")
        
        return ''.join(output_lines)
    
    def save_output(self, tool_name, command, output, return_code=None, execution_time=None):
        """Save the command output to a file."""
        # Apply filter to output if specified (only save matching lines)
        if self.filter_pattern:
            output_lines = output.split('\n')
            filtered_lines = [line for line in output_lines if re.search(self.filter_pattern, line, re.IGNORECASE)]
            filtered_output = '\n'.join(filtered_lines)
            
            # Add filter info to saved output
            filter_note = f"\n[SNB Filter Applied: {self.filter_pattern}]\n[Matched {len(filtered_lines)} lines out of {len(output_lines)} total lines]\n\n"
            output_to_save = filter_note + filtered_output
        else:
            output_to_save = output
        
        # Prepare metadata
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata = {
            'tool': tool_name,
            'command': ' '.join(command) if command else 'piped input',
            'timestamp': timestamp,
            'return_code': return_code,
            'execution_time': None,
            'execution_time_seconds': None,
            'filter_pattern': self.filter_pattern if self.filter_pattern else None
        }
        
        # Add execution time if available
        if execution_time:
            metadata['execution_time'] = str(execution_time).split('.')[0]  # Remove microseconds
            metadata['execution_time_seconds'] = execution_time.total_seconds()
        
        # If save_all_formats is enabled, save in all formats
        if self.save_all_formats:
            formats = ['txt', 'json', 'html', 'md']
            saved_files = []
            
            for fmt in formats:
                # Temporarily change format
                original_format = self.output_format
                self.output_format = fmt
                
                # Get output path and content for this format
                output_path = self.get_output_path(tool_name)
                content = self._get_formatted_content(fmt, metadata, output_to_save)
                
                # Write to file
                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    saved_files.append(str(output_path))
                except Exception as e:
                    print(f"[SNB] Error saving {fmt} format: {str(e)}", file=sys.stderr)
                
                # Restore format
                self.output_format = original_format
            
            print("-" * 80)
            if self.filter_pattern:
                print(f"[SNB] Filtered output saved in all formats:")
            else:
                print(f"[SNB] Output saved in all formats:")
            for file in saved_files:
                print(f"  - {file}")
            return True
        else:
            # Single format save
            output_path = self.get_output_path(tool_name)
            content = self._get_formatted_content(self.output_format, metadata, output_to_save)
            
            # Write to file
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("-" * 80)
                print(f"[SNB] Output saved to: {output_path}")
                return True
            except Exception as e:
                print(f"[SNB] Error saving output: {str(e)}", file=sys.stderr)
                return False
    
    def _get_formatted_content(self, format_type, metadata, output):
        """Get formatted content based on format type."""
        if format_type == 'json':
            return self._format_json(metadata, output)
        elif format_type == 'html':
            return self._format_html(metadata, output)
        elif format_type in ['md', 'markdown']:
            return self._format_markdown(metadata, output)
        else:  # Default to txt
            return self._format_txt(metadata, output)
    
    def _format_txt(self, metadata, output):
        """Format output as plain text."""
        content = f"""{'=' * 80}
SNB - Command Output Log
{'=' * 80}
Tool: {metadata['tool']}
Command: {metadata['command']}
Timestamp: {metadata['timestamp']}
"""
        if metadata['return_code'] is not None:
            content += f"Return Code: {metadata['return_code']}\n"
        
        if metadata['execution_time']:
            content += f"Execution Time: {metadata['execution_time']}\n"
        
        content += f"""{'=' * 80}

{output}
"""
        return content
    
    def _format_json(self, metadata, output):
        """Format output as JSON."""
        data = {
            'metadata': metadata,
            'output': output.strip(),
            'output_lines': output.strip().split('\n') if output.strip() else []
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _format_html(self, metadata, output):
        """Format output as HTML."""
        escaped_output = output.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SNB Output - {metadata['tool']}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: #252526;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            color: #4ec9b0;
            border-bottom: 2px solid #4ec9b0;
            padding-bottom: 10px;
        }}
        .metadata {{
            background-color: #2d2d30;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #007acc;
        }}
        .metadata-item {{
            margin: 8px 0;
        }}
        .metadata-label {{
            color: #569cd6;
            font-weight: bold;
        }}
        .output {{
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 5px;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-x: auto;
            border: 1px solid #3e3e42;
        }}
        .timestamp {{
            color: #6a9955;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 SNB Command Output Log</h1>
        
        <div class="metadata">
            <div class="metadata-item">
                <span class="metadata-label">Tool:</span> {metadata['tool']}
            </div>
            <div class="metadata-item">
                <span class="metadata-label">Command:</span> {metadata['command']}
            </div>
            <div class="metadata-item">
                <span class="metadata-label">Timestamp:</span> <span class="timestamp">{metadata['timestamp']}</span>
            </div>
            {f'<div class="metadata-item"><span class="metadata-label">Return Code:</span> {metadata["return_code"]}</div>' if metadata['return_code'] is not None else ''}
            {f'<div class="metadata-item"><span class="metadata-label">Execution Time:</span> {metadata["execution_time"]}</div>' if metadata['execution_time'] else ''}
        </div>
        
        <h2>Output:</h2>
        <div class="output">{escaped_output}</div>
    </div>
</body>
</html>
"""
        return html
    
    def _format_markdown(self, metadata, output):
        """Format output as Markdown."""
        md = f"""# SNB - Command Output Log

## Metadata

- **Tool:** `{metadata['tool']}`
- **Command:** `{metadata['command']}`
- **Timestamp:** {metadata['timestamp']}
"""
        if metadata['return_code'] is not None:
            md += f"- **Return Code:** {metadata['return_code']}\n"
        
        if metadata['execution_time']:
            md += f"- **Execution Time:** {metadata['execution_time']}\n"
        
        md += f"""
---

## Output

```
{output}
```
"""
        return md
    
    def auto_compress_old_files(self):
        """Automatically compress files older than specified days."""
        try:
            current_time = datetime.datetime.now()
            compressed_count = 0
            
            # Walk through all tool directories
            for tool_dir in self.base_dir.iterdir():
                if not tool_dir.is_dir():
                    continue
                
                # Check each .txt file in the tool directory
                for file_path in tool_dir.glob("*.txt"):
                    # Get file modification time
                    file_mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                    file_age_days = (current_time - file_mtime).days
                    
                    # Compress if older than threshold
                    if file_age_days >= self.auto_compress_days:
                        gz_path = file_path.with_suffix('.txt.gz')
                        
                        # Skip if already compressed
                        if gz_path.exists():
                            continue
                        
                        # Compress the file
                        with open(file_path, 'rb') as f_in:
                            with gzip.open(gz_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        # Remove original file after successful compression
                        file_path.unlink()
                        compressed_count += 1
            
            if compressed_count > 0:
                print(f"[SNB] Auto-compressed {compressed_count} old file(s)")
        
        except Exception as e:
            # Silently fail - don't interrupt the main operation
            pass
    
    def search_outputs(self, pattern, tool_name=None):
        """Search through saved outputs for a pattern."""
        print(f"[SNB] Searching for: {pattern}")
        if tool_name:
            print(f"[SNB] Tool filter: {tool_name}")
        print("=" * 80)
        
        results = []
        search_regex = re.compile(pattern, re.IGNORECASE)
        
        # Determine search scope
        if tool_name:
            # Search specific tool directory
            tool_dirs = [self.base_dir / tool_name]
        else:
            # Search all tool directories
            tool_dirs = [d for d in self.base_dir.iterdir() if d.is_dir()]
        
        # Search through files
        for tool_dir in tool_dirs:
            if not tool_dir.exists():
                continue
            
            # Search .txt files (and .txt.gz)
            for file_path in list(tool_dir.glob("*.txt")) + list(tool_dir.glob("*.txt.gz")):
                try:
                    # Read file (handle both txt and gz)
                    if file_path.suffix == '.gz':
                        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                            content = f.read()
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    
                    # Search for pattern
                    matches = []
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if search_regex.search(line):
                            matches.append((line_num, line.strip()))
                    
                    if matches:
                        results.append({
                            'file': file_path,
                            'matches': matches
                        })
                
                except Exception as e:
                    continue
        
        # Display results
        if not results:
            print(f"No matches found for '{pattern}'")
            return
        
        print(f"Found matches in {len(results)} file(s):\n")
        
        for result in results:
            file_path = result['file']
            matches = result['matches']
            
            print(f"\n📄 {file_path}")
            print(f"   {len(matches)} match(es):")
            
            # Show first 5 matches per file
            for line_num, line in matches[:5]:
                # Highlight the match
                highlighted = search_regex.sub(lambda m: f">>>{m.group()}<<<", line)
                print(f"   Line {line_num}: {highlighted}")
            
            if len(matches) > 5:
                print(f"   ... and {len(matches) - 5} more match(es)")
        
        print("\n" + "=" * 80)
        print(f"Total: {len(results)} file(s) with matches")
    
    def execute(self, command):
        """Main execution method."""
        # Determine if input is piped
        is_piped = not sys.stdin.isatty()
        execution_time = None
        
        if is_piped:
            # Read from pipe and try to detect tool name
            output = self.read_piped_input()
            tool_name = self.detect_tool_from_pipe()
            return_code = 0
        elif not command:
            print("Usage: snb <command> [args...]", file=sys.stderr)
            print("   or: <command> | snb", file=sys.stderr)
            return 1
        else:
            # Run command
            tool_name = self.get_tool_name(command)
            output, return_code, execution_time = self.run_command(command)
            
            # Print execution time
            print("-" * 80)
            print(f"[SNB] Execution completed in: {str(execution_time).split('.')[0]}")
        
        # Save output
        self.save_output(tool_name, command if not is_piped else [], output, return_code, execution_time)
        
        return return_code


def main():
    # Parse arguments
    command = []
    custom_tag = None
    output_format = 'txt'
    save_all_formats = False
    session = None
    filter_pattern = None
    search_mode = False
    search_pattern = None
    search_tool = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == '--search':
            # Search mode: --search <pattern> [tool]
            search_mode = True
            if i + 1 < len(sys.argv):
                search_pattern = sys.argv[i + 1]
                # Check if tool name is provided
                if i + 2 < len(sys.argv):
                    search_tool = sys.argv[i + 2]
                i += 3 if search_tool else 2
            else:
                print("Error: --search requires a search pattern", file=sys.stderr)
                sys.exit(1)
            break  # No more arguments needed in search mode
        elif arg in ['-t', '--tag']:
            # Next argument is the tag
            if i + 1 < len(sys.argv):
                custom_tag = sys.argv[i + 1]
                i += 2
            else:
                print("Error: -t/--tag requires a tag name", file=sys.stderr)
                sys.exit(1)
        elif arg in ['-f', '--format']:
            # Next argument is the format
            if i + 1 < len(sys.argv):
                output_format = sys.argv[i + 1].lower()
                if output_format not in ['txt', 'json', 'html', 'md', 'markdown']:
                    print(f"Error: Invalid format '{output_format}'. Use: txt, json, html, md", file=sys.stderr)
                    sys.exit(1)
                i += 2
            else:
                print("Error: -f/--format requires a format (txt, json, html, md)", file=sys.stderr)
                sys.exit(1)
        elif arg in ['-A', '--all']:
            # Save in all formats
            save_all_formats = True
            i += 1
        elif arg in ['-s', '--session']:
            # Next argument is the session name
            if i + 1 < len(sys.argv):
                session = sys.argv[i + 1]
                # Sanitize session name
                session = "".join(c for c in session if c.isalnum() or c in ('-', '_', ' ')).strip()
                session = session.replace(' ', '-')
                i += 2
            else:
                print("Error: -s/--session requires a session name", file=sys.stderr)
                sys.exit(1)
        elif arg in ['-g', '--grep']:
            # Next argument is the filter pattern
            if i + 1 < len(sys.argv):
                filter_pattern = sys.argv[i + 1]
                i += 2
            else:
                print("Error: -g/--grep requires a pattern", file=sys.stderr)
                sys.exit(1)
        else:
            # Rest are command arguments
            command = sys.argv[i:]
            break
    
    # Get auto-compress days from environment variable (default: 7 days)
    auto_compress_days = int(os.environ.get('SNB_AUTO_COMPRESS_DAYS', '7'))
    
    # Initialize SNB
    snb = SNB(auto_compress_days=auto_compress_days, custom_tag=custom_tag, 
              output_format=output_format, save_all_formats=save_all_formats, 
              session=session, filter_pattern=filter_pattern)
    
    # Handle search mode or execution mode
    if search_mode:
        snb.search_outputs(search_pattern, search_tool)
        sys.exit(0)
    else:
        exit_code = snb.execute(command)
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
