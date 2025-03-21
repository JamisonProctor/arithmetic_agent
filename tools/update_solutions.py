import os
import re
import glob
import sys

# Get the absolute path to the project root directory
# Assuming the script is in the tools folder
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)  # Go one level up from tools folder

def extract_solution(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the "## Solution" section
    match = re.search(r'## Solution\s*([\s\S]*?)$', content)
    if match:
        return match.group(1).strip()
    return None

def update_log_files(problem_number, solution_content):
    # Find all log files with matching problem number
    log_path = os.path.join(project_root, 'logs', f'*__{problem_number}.md')
    log_files = glob.glob(log_path)
    
    for log_file in log_files:
        with open(log_file, 'r') as file:
            content = file.read()
        
        # Replace the "## Ground Truth Solution" section
        updated_content = re.sub(
            r'## Ground Truth Solution\s*[\s\S]*?$',
            f'## Ground Truth Solution\n\n{solution_content}',
            content
        )
        
        with open(log_file, 'w') as file:
            file.write(updated_content)
        
        print(f"Updated {log_file}")

def main():
    # Get all problem files
    problem_path = os.path.join(project_root, 'word_problems', 'problem_*.md')
    problem_files = glob.glob(problem_path)
    
    for problem_file in problem_files:
        # Extract problem number (e.g., "001" from "problem_001.md")
        problem_number = os.path.basename(problem_file).split('_')[1].split('.')[0]
        
        # Extract solution content
        solution_content = extract_solution(problem_file)
        
        if solution_content:
            print(f"Processing problem {problem_number}")
            update_log_files(problem_number, solution_content)
        else:
            print(f"No solution found in {problem_file}")

if __name__ == "__main__":
    main()
