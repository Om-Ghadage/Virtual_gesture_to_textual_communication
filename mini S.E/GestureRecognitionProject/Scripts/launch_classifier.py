# import os
# import subprocess
# import sys

# # Path to your Python file
# script_path = "Scripts/classify_gestures.py"

# # Build the command
# command = [
#     sys.executable,
#     "-W", "ignore",
#     script_path
# ]

# # Block C++ logs by hiding stderr
# with open(os.devnull, 'w') as devnull:
#     subprocess.run(command, stderr=devnull)
import subprocess
import os
import sys

script_path = os.path.join(os.path.dirname(__file__), "classify_gestures.py")

subprocess.run([sys.executable, script_path])