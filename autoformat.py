import os
import subprocess
import sys

# Set the path to your C++ files
SOURCE_DIR = "."  # Adjust to your project root

CPP_EXTENSIONS = (".cpp", ".h", ".hpp", ".cc", ".cxx")

# Set LAB_PART if provided as an argument (otherwise use default value)
LAB_PART = os.environ.get("LAB_PART", "default_lab_part")  # Modify default as needed

def get_cpp_files():
    """Finds all C++ files in the project directory."""
    cpp_files = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(CPP_EXTENSIONS):
                cpp_files.append(os.path.join(root, file))
    return cpp_files

def format_files():
    """Formats all C++ files using clang-format."""
    cpp_files = get_cpp_files()
    
    if not cpp_files:
        print("No C++ files found.")
        return
    
    for file in cpp_files:
        print(f"Formatting: {file}")
        subprocess.run(["clang-format", "-i", "--style=Google", file], check=True)

def check_format():
    """Runs the existing check script before formatting."""
    result = subprocess.run(["python3", SOURCE_DIR + "/../.action/checks.py", "format", LAB_PART], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    return result.returncode == 0  # Return True if no errors

if __name__ == "__main__":
    if len(sys.argv) > 1:
        SOURCE_DIR = sys.argv[1]
        if "--check" in sys.argv:
            if check_format():
                print("Code is already correctly formatted.")
                sys.exit(0)
            else:
                print("Formatting issues detected, applying fixes...")
    else:
        print("Missing checkpath arguement")
        sys.exit(0)
    format_files()
    print("Formatting complete.")

if len(sys.argv) > 2:
    print(sys.argv[2])
