import os
import argparse
import fnmatch
from pathlib import Path

# --- Configuration ---

# Add or remove file extensions you want to include in the bundle.
# This list is used if no specific file types are provided via command line.
DEFAULT_INCLUDE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss', '.json',
    '.md', '.java', '.c', '.h', '.cpp', '.hpp', '.cs', '.go', '.rs', '.php',
    '.rb', '.swift', '.kt', '.kts', '.sh', '.yml', '.yaml', '.toml', '.ini',
    '.cfg', '.sql', '.dockerfile', 'Dockerfile'
}

# Add file or directory names to always ignore, in addition to .gitignore.
# Uses glob patterns (e.g., 'node_modules', '*.log').
DEFAULT_EXCLUDE_PATTERNS = [
    '.git', '.idea', '.vscode', 'venv', '.venv', '__pycache__', 'node_modules',
    'dist', 'build', 'target', '*.pyc', '*.log', '*.swp', '*.swo'
]

# Mapping of file extensions to Markdown language identifiers for syntax highlighting.
# Add more as needed.
LANGUAGE_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.jsx': 'jsx',
    '.tsx': 'tsx',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.json': 'json',
    '.md': 'markdown',
    '.java': 'java',
    '.c': 'c',
    '.h': 'c',
    '.cpp': 'cpp',
    '.hpp': 'cpp',
    '.cs': 'csharp',
    '.go': 'go',
    '.rs': 'rust',
    '.php': 'php',
    '.rb': 'ruby',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.kts': 'kotlin',
    '.sh': 'shell',
    '.yml': 'yaml',
    '.yaml': 'yaml',
    '.sql': 'sql',
    '.dockerfile': 'dockerfile',
    'Dockerfile': 'dockerfile'
}

# --- Script Logic ---

def get_gitignore_patterns(project_root):
    """Reads .gitignore from the project root and returns a list of patterns."""
    gitignore_path = os.path.join(project_root, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def is_ignored(path, project_root, all_ignore_patterns):
    """
    Checks if a file or directory path should be ignored based on the combined
    .gitignore rules and default exclude patterns.
    """
    relative_path = os.path.relpath(path, project_root).replace('\\', '/')
    
    # Check against each pattern
    for pattern in all_ignore_patterns:
        # Handle directory patterns (e.g., 'node_modules/')
        if pattern.endswith('/'):
            # If the path is a directory or is inside a directory matching the pattern
            if os.path.isdir(path) and fnmatch.fnmatch(relative_path + '/', pattern):
                return True
            if relative_path.startswith(pattern.rstrip('/')):
                 return True
        # Handle file/wildcard patterns
        elif fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
            
    return False

def create_bundle(project_root, output_file, include_exts, exclude_patterns):
    """
    Walks the project directory, collects files, and writes them to the output bundle.
    """
    project_root = os.path.abspath(project_root)
    output_file = os.path.abspath(output_file)
    
    gitignore_patterns = get_gitignore_patterns(project_root)
    all_ignore_patterns = exclude_patterns + gitignore_patterns

    print(f"Starting project bundling...")
    print(f"Project Root: {project_root}")
    print(f"Output File: {output_file}")
    print(f"Including extensions: {', '.join(include_exts)}")
    print(f"Ignoring patterns: {', '.join(all_ignore_patterns)}\n")

    file_count = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# Project Bundle: {os.path.basename(project_root)}\n\n")
        outfile.write("This file contains a bundle of all relevant code files from the project, formatted for use with an AI.\n")
        outfile.write("Each file's content is enclosed in a Markdown code block, with its original path specified.\n\n")
        
        for root, dirs, files in os.walk(project_root, topdown=True):
            # Filter directories to ignore in-place to prevent walking them
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), project_root, all_ignore_patterns)]

            for filename in files:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, project_root).replace('\\', '/')

                # 1. Check if the file itself should be ignored
                if is_ignored(file_path, project_root, all_ignore_patterns):
                    continue

                # 2. Check if it's the output file itself
                if file_path == output_file:
                    continue

                # 3. Check file extension
                file_ext = os.path.splitext(filename)[1]
                if filename not in include_exts and file_ext not in include_exts:
                    continue

                # If all checks pass, add the file to the bundle
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                    
                    outfile.write(f'---\n\n')
                    outfile.write(f'**File:** `{relative_path}`\n\n')
                    
                    lang = LANGUAGE_MAP.get(file_ext, LANGUAGE_MAP.get(filename, ''))
                    outfile.write(f'```{lang}\n')
                    outfile.write(content.strip())
                    outfile.write(f'\n```\n\n')
                    
                    print(f"  [+] Bundled: {relative_path}")
                    file_count += 1

                except Exception as e:
                    print(f"  [!] Error reading {relative_path}: {e}")

    print(f"\n✅ Success! Bundled {file_count} files into '{os.path.basename(output_file)}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Bundle project code files into a single Markdown file for AI prompts.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--root',
        default='.',
        help="The root directory of the project to bundle. (default: current directory)"
    )
    parser.add_argument(
        '--output',
        default='project_bundle.md',
        help="The name of the output Markdown file. (default: project_bundle.md)"
    )
    parser.add_argument(
        '--include',
        nargs='+',
        help=f"Space-separated list of file extensions to include (e.g., .py .js .html).\n"
             f"If not provided, defaults to a predefined list."
    )
    args = parser.parse_args()

    include_extensions = set(args.include) if args.include else DEFAULT_INCLUDE_EXTENSIONS
    
    create_bundle(args.root, args.output, include_extensions, DEFAULT_EXCLUDE_PATTERNS)


if __name__ == "__main__":
    main()
    