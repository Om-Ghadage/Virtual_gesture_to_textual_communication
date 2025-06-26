import os
import shutil

# Define the folder structure
project_root = "GestureRecognitionProject"
subfolders = ["Data", "Models", "Scripts"]

# Create the main project directory
if not os.path.exists(project_root):
    os.makedirs(project_root)

# Create subdirectories
for subfolder in subfolders:
    path = os.path.join(project_root, subfolder)
    if not os.path.exists(path):
        os.makedirs(path)

print("Project folder setup complete!")
